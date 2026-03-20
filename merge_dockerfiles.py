#!/usr/bin/env python3
"""
ODH & RHOAI Dockerfile Merge Tool

Parses Konflux gitops YAMLs for ODH and RHOAI, correlates components by repo name,
downloads Dockerfiles, merges them into a single parameterized Dockerfile.Konflux
using BUILD_MODE ARG, and generates documentation.
"""

import os
import re
import ssl
import sys
import difflib
import textwrap
import urllib.request
import urllib.error
from pathlib import Path
from collections import defaultdict
from dataclasses import dataclass, field

import yaml

# Work around macOS Python SSL certificate issue
SSL_CTX = ssl.create_default_context()
try:
    import certifi
    SSL_CTX.load_verify_locations(certifi.where())
except Exception:
    SSL_CTX.check_hostname = False
    SSL_CTX.verify_mode = ssl.CERT_NONE

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

ODH_YAML = os.path.expanduser(
    "~/RHODS/DevOps/konflux-release-data/tenants-config/cluster/"
    "stone-prd-rh01/tenants/open-data-hub-tenant/opendatahub-ci-components.yaml"
)
RHOAI_YAML = os.path.expanduser(
    "~/RHODS/DevOps/konflux-release-data/tenants-config/cluster/"
    "stone-prod-p02/tenants/rhoai-tenant/v3.4/ProjectDevelopmentStream-v3.4.yaml"
)

WORKSPACE = Path(__file__).resolve().parent
OUTPUT_DIR = WORKSPACE / "Dockerfiles"

# RHOAI template variable values (extracted from ProjectDevelopmentStream)
RHOAI_TEMPLATE_VARS = {
    "version": "v3.4",
    "versionName": "v3-4",
    "branch": "rhoai-3.4",
}

RAW_GH = "https://raw.githubusercontent.com"
DOWNLOAD_TIMEOUT = 30  # seconds


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class ComponentInfo:
    name: str            # metadata.name (raw)
    component_name: str  # spec.componentName
    url: str             # spec.source.git.url
    revision: str        # spec.source.git.revision
    context: str         # spec.source.git.context (default ".")
    dockerfile_url: str  # spec.source.git.dockerfileUrl
    org: str = ""        # github org extracted from url
    repo_name: str = ""  # repo name extracted from url
    norm_name: str = ""  # normalized component name for matching


@dataclass
class MatchedPair:
    repo_name: str
    odh: ComponentInfo
    rhoai: ComponentInfo
    dir_path: Path = None
    strategy: str = ""
    odh_content: str = ""
    rhoai_content: str = ""
    merged_content: str = ""
    error: str = ""
    warnings: list = field(default_factory=list)
    extra_args: list = field(default_factory=list)


# ---------------------------------------------------------------------------
# Phase 1: Parse YAMLs
# ---------------------------------------------------------------------------

def parse_odh_yaml(path: str) -> list[ComponentInfo]:
    """Parse ODH gitops YAML – direct multi-doc with kind=Component."""
    with open(path) as f:
        docs = list(yaml.safe_load_all(f))

    components = []
    for doc in docs:
        if not doc or doc.get("kind") != "Component":
            continue
        meta = doc.get("metadata", {})
        spec = doc.get("spec", {})
        git = spec.get("source", {}).get("git", {})
        if not git.get("url"):
            continue
        ci = ComponentInfo(
            name=meta.get("name", ""),
            component_name=spec.get("componentName", meta.get("name", "")),
            url=git.get("url", ""),
            revision=git.get("revision", "main"),
            context=git.get("context", "."),
            dockerfile_url=git.get("dockerfileUrl", "Dockerfile"),
        )
        _enrich(ci)
        components.append(ci)
    return components


def _resolve_go_template(text: str, vars_: dict) -> str:
    """Replace Go-template placeholders like {{.branch}} with values."""
    for k, v in vars_.items():
        text = text.replace("{{.%s}}" % k, v)
        # Also handle the hyphenize helper used for versionName default
        text = text.replace("{{hyphenize .%s}}" % k, v)
    return text


def parse_rhoai_yaml(path: str) -> list[ComponentInfo]:
    """Parse RHOAI gitops YAML – ProjectDevelopmentStreamTemplate with Go templates."""
    with open(path) as f:
        raw = f.read()

    # Resolve Go templates before YAML parsing so that {{...}} don't confuse the parser
    resolved = _resolve_go_template(raw, RHOAI_TEMPLATE_VARS)
    docs = list(yaml.safe_load_all(resolved))

    components = []
    for doc in docs:
        if not doc:
            continue
        kind = doc.get("kind", "")

        if kind == "Component":
            # Shouldn't appear at top level in this file, but handle anyway
            components.append(_extract_component(doc))
        elif kind == "ProjectDevelopmentStreamTemplate":
            for res in doc.get("spec", {}).get("resources", []):
                if res.get("kind") == "Component":
                    c = _extract_component(res)
                    if c:
                        components.append(c)
    return components


def _extract_component(doc: dict) -> ComponentInfo | None:
    meta = doc.get("metadata", {})
    spec = doc.get("spec", {})
    git = spec.get("source", {}).get("git", {})
    if not git.get("url"):
        return None
    ci = ComponentInfo(
        name=meta.get("name", ""),
        component_name=spec.get("componentName", meta.get("name", "")),
        url=git.get("url", ""),
        revision=git.get("revision", "main"),
        context=git.get("context", "."),
        dockerfile_url=git.get("dockerfileUrl", "Dockerfile"),
    )
    _enrich(ci)
    return ci


def _enrich(ci: ComponentInfo):
    """Populate org, repo_name, and norm_name from the raw fields."""
    url = ci.url.rstrip("/")
    if url.endswith(".git"):
        url = url[:-4]
    parts = url.split("/")
    ci.repo_name = parts[-1] if parts else ""
    ci.org = parts[-2] if len(parts) >= 2 else ""
    # Normalize component name: strip -ci suffix (ODH) or -v3-4 suffix (RHOAI)
    n = ci.component_name
    if n.endswith("-ci"):
        n = n[:-3]
    # Strip version suffix like -v3-4
    n = re.sub(r"-v\d+-\d+$", "", n)
    ci.norm_name = n


# ---------------------------------------------------------------------------
# Phase 2: Correlate components
# ---------------------------------------------------------------------------

def correlate(
    odh_list: list[ComponentInfo], rhoai_list: list[ComponentInfo]
) -> tuple[list[MatchedPair], list[ComponentInfo], list[ComponentInfo]]:
    """Match ODH ↔ RHOAI components. Returns (matched, odh_only, rhoai_only)."""

    # Build lookup: (repo_name, norm_name) → component
    odh_by_key: dict[tuple[str, str], ComponentInfo] = {}
    for c in odh_list:
        odh_by_key[(c.repo_name, c.norm_name)] = c

    rhoai_by_key: dict[tuple[str, str], ComponentInfo] = {}
    for c in rhoai_list:
        rhoai_by_key[(c.repo_name, c.norm_name)] = c

    matched = []
    matched_odh_keys = set()
    matched_rhoai_keys = set()

    # --- Primary match: exact (repo_name, norm_name) ---
    for key, odh_c in odh_by_key.items():
        if key in rhoai_by_key:
            matched.append(MatchedPair(
                repo_name=key[0], odh=odh_c, rhoai=rhoai_by_key[key],
            ))
            matched_odh_keys.add(key)
            matched_rhoai_keys.add(key)

    # --- Fallback match: same repo, dockerfile-path similarity ---
    odh_remaining = {k: v for k, v in odh_by_key.items() if k not in matched_odh_keys}
    rhoai_remaining = {k: v for k, v in rhoai_by_key.items() if k not in matched_rhoai_keys}

    # Group remaining by repo_name
    odh_by_repo: dict[str, list[tuple]] = defaultdict(list)
    for k, v in odh_remaining.items():
        odh_by_repo[k[0]].append((k, v))
    rhoai_by_repo: dict[str, list[tuple]] = defaultdict(list)
    for k, v in rhoai_remaining.items():
        rhoai_by_repo[k[0]].append((k, v))

    for repo in set(odh_by_repo) & set(rhoai_by_repo):
        odh_items = list(odh_by_repo[repo])
        rhoai_items = list(rhoai_by_repo[repo])
        used_rhoai = set()
        for o_key, o_comp in odh_items:
            best_score = 0.0
            best_r = None
            o_path = _norm_dockerfile_path(o_comp.dockerfile_url)
            for r_key, r_comp in rhoai_items:
                if r_key in used_rhoai:
                    continue
                r_path = _norm_dockerfile_path(r_comp.dockerfile_url)
                score = difflib.SequenceMatcher(None, o_path, r_path).ratio()
                if score > best_score:
                    best_score = score
                    best_r = (r_key, r_comp)
            if best_r and best_score > 0.4:
                matched.append(MatchedPair(
                    repo_name=repo, odh=o_comp, rhoai=best_r[1],
                ))
                matched_odh_keys.add(o_key)
                matched_rhoai_keys.add(best_r[0])
                used_rhoai.add(best_r[0])

    odh_only = [v for k, v in odh_by_key.items() if k not in matched_odh_keys]
    rhoai_only = [v for k, v in rhoai_by_key.items() if k not in matched_rhoai_keys]

    return matched, odh_only, rhoai_only


def _norm_dockerfile_path(p: str) -> str:
    """Normalize a dockerfile path for comparison: lowercase, strip common prefixes."""
    p = p.lower().strip("./")
    p = re.sub(r"\.konflux", "", p)
    return p


# ---------------------------------------------------------------------------
# Phase 3: Download Dockerfiles
# ---------------------------------------------------------------------------

def _build_raw_url(comp: ComponentInfo) -> str:
    """Build a raw.githubusercontent.com URL for the Dockerfile."""
    url = comp.url.rstrip("/")
    if url.endswith(".git"):
        url = url[:-4]
    # Extract org/repo from https://github.com/{org}/{repo}
    parts = url.replace("https://github.com/", "").split("/")
    org_repo = "/".join(parts[:2])

    context = comp.context.strip("./") if comp.context else ""
    dfile = comp.dockerfile_url.strip("./") if comp.dockerfile_url else "Dockerfile"

    # Determine full path: if dockerfileUrl already contains the context prefix, use it directly
    if context and not dfile.startswith(context):
        full_path = f"{context}/{dfile}" if context else dfile
    else:
        full_path = dfile

    return f"{RAW_GH}/{org_repo}/{comp.revision}/{full_path}"


def download_dockerfile(comp: ComponentInfo) -> str:
    """Download a Dockerfile and return its content. Raises on failure."""
    url = _build_raw_url(comp)
    req = urllib.request.Request(url, headers={"User-Agent": "dockerfile-merge-tool/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=DOWNLOAD_TIMEOUT, context=SSL_CTX) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP {e.code} downloading {url}") from e
    except Exception as e:
        raise RuntimeError(f"Failed to download {url}: {e}") from e


def download_pair(pair: MatchedPair):
    """Download both Dockerfiles for a matched pair."""
    try:
        pair.odh_content = download_dockerfile(pair.odh)
    except RuntimeError as e:
        pair.error = f"ODH download failed: {e}"
        return
    try:
        pair.rhoai_content = download_dockerfile(pair.rhoai)
    except RuntimeError as e:
        pair.error = f"RHOAI download failed: {e}"
        return


# ---------------------------------------------------------------------------
# Phase 4: Merge engine
# ---------------------------------------------------------------------------

def _similarity(a: str, b: str) -> float:
    return difflib.SequenceMatcher(None, a.splitlines(), b.splitlines()).ratio()


def _extract_from_lines(content: str) -> list[str]:
    """Extract FROM image references from a Dockerfile."""
    froms = []
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.upper().startswith("FROM "):
            froms.append(stripped)
    return froms


def _check_digest_warnings(content: str, label: str) -> list[str]:
    """Warn about FROM lines using tags instead of digests."""
    warnings = []
    for line in _extract_from_lines(content):
        # FROM image@sha256:... is fine, FROM image:tag or FROM image (no tag) is not
        img_part = line.split()[1] if len(line.split()) > 1 else ""
        if "@sha256:" not in img_part and img_part != "scratch":
            warnings.append(f"{label}: base image uses tag, not digest: `{img_part}`")
    return warnings


def merge_dockerfiles(pair: MatchedPair):
    """Produce the merged Dockerfile.Konflux for a matched pair."""
    if pair.error:
        return

    odh = pair.odh_content
    rhoai = pair.rhoai_content

    pair.warnings.extend(_check_digest_warnings(odh, "ODH"))
    pair.warnings.extend(_check_digest_warnings(rhoai, "RHOAI"))

    ratio = _similarity(odh, rhoai)

    if ratio > 0.95:
        pair.strategy = "A"
        pair.merged_content = _merge_strategy_a(odh)
    elif ratio > 0.5:
        pair.strategy = "B/C"
        pair.merged_content = _merge_strategy_bc(odh, rhoai, pair)
    else:
        pair.strategy = "D"
        pair.merged_content = _merge_strategy_d(odh, rhoai, pair)


def _merge_strategy_a(odh: str) -> str:
    """Strategy A: near-identical files. Just prepend BUILD_MODE ARG."""
    header = "ARG BUILD_MODE=ODH\n\n"
    return header + odh


_DOCKERFILE_INSTRUCTIONS = frozenset({
    "FROM", "RUN", "CMD", "LABEL", "MAINTAINER", "EXPOSE", "ENV", "ADD",
    "COPY", "ENTRYPOINT", "VOLUME", "USER", "WORKDIR", "ARG", "ONBUILD",
    "STOPSIGNAL", "HEALTHCHECK", "SHELL",
})


def _is_runnable_block(lines: list[str]) -> bool:
    """Return True if ALL non-blank/comment lines in the block are RUN instructions
    or continuations (backslash-continued lines), making them safe to wrap in shell conditionals."""
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        keyword = stripped.split()[0].upper() if stripped.split() else ""
        if keyword in _DOCKERFILE_INSTRUCTIONS and keyword != "RUN":
            return False
    return True


def _strip_run_prefix(line: str) -> str:
    """Strip the 'RUN ' prefix from a Dockerfile line so it can be used inside a shell conditional."""
    stripped = line.rstrip("\n").strip()
    if stripped.upper().startswith("RUN "):
        return stripped[4:]
    return stripped


def _emit_conditional_block(merged: list[str], odh_block: list[str] | None,
                            rhoai_block: list[str] | None):
    """Emit a diff block. Uses shell conditionals for RUN-only blocks,
    or comment-delimited sections for blocks containing non-RUN instructions."""
    blocks = {"ODH": odh_block or [], "RHOAI": rhoai_block or []}
    all_lines = (odh_block or []) + (rhoai_block or [])
    runnable = _is_runnable_block(all_lines)

    if runnable and odh_block and rhoai_block:
        merged.append('RUN if [ "$BUILD_MODE" = "RHOAI" ]; then \\\n')
        for line in rhoai_block:
            merged.append(f"      {_strip_run_prefix(line)} ; \\\n")
        merged.append("    else \\\n")
        for line in odh_block:
            merged.append(f"      {_strip_run_prefix(line)} ; \\\n")
        merged.append("    fi\n")
    elif runnable and odh_block and not rhoai_block:
        merged.append('RUN if [ "$BUILD_MODE" = "ODH" ]; then \\\n')
        for line in odh_block:
            merged.append(f"      {_strip_run_prefix(line)} ; \\\n")
        merged.append("    fi\n")
    elif runnable and rhoai_block and not odh_block:
        merged.append('RUN if [ "$BUILD_MODE" = "RHOAI" ]; then \\\n')
        for line in rhoai_block:
            merged.append(f"      {_strip_run_prefix(line)} ; \\\n")
        merged.append("    fi\n")
    else:
        # Non-RUN instructions: use comment-delimited sections
        if odh_block:
            merged.append("# >>> [ODH] <<<\n")
            merged.extend(odh_block)
            merged.append("# >>> [END ODH] <<<\n")
        if rhoai_block:
            merged.append("# >>> [RHOAI] <<<\n")
            merged.extend(rhoai_block)
            merged.append("# >>> [END RHOAI] <<<\n")


def _merge_strategy_bc(odh: str, rhoai: str, pair: MatchedPair) -> str:
    """Strategy B/C: moderately different. Line-by-line merge with conditionals."""
    odh_lines = odh.splitlines(keepends=True)
    rhoai_lines = rhoai.splitlines(keepends=True)

    merged = ["ARG BUILD_MODE=ODH\n", "\n"]

    # Identify if base images differ – parameterize FROM lines
    odh_froms = _extract_from_lines(odh)
    rhoai_froms = _extract_from_lines(rhoai)

    from_pairs = list(zip(odh_froms, rhoai_froms))
    extra_args = []
    from_replacements = {}
    for i, (of, rf) in enumerate(from_pairs):
        if of != rf:
            odh_img = of.split()[1]
            rhoai_img = rf.split()[1]
            odh_parts = of.split()
            rhoai_parts = rf.split()
            alias = ""
            if len(odh_parts) >= 4 and odh_parts[2].upper() == "AS":
                alias = f" AS {odh_parts[3]}"
            elif len(rhoai_parts) >= 4 and rhoai_parts[2].upper() == "AS":
                alias = f" AS {rhoai_parts[3]}"
            arg_name = f"BASE_IMAGE_{i}" if i > 0 else "BASE_IMAGE"
            extra_args.append(arg_name)
            from_replacements[of.strip()] = (arg_name, odh_img, rhoai_img, alias)
            from_replacements[rf.strip()] = (arg_name, odh_img, rhoai_img, alias)

    pair.extra_args = extra_args

    sm = difflib.SequenceMatcher(None, odh_lines, rhoai_lines)
    opcodes = sm.get_opcodes()

    for tag, i1, i2, j1, j2 in opcodes:
        if tag == "equal":
            for line in odh_lines[i1:i2]:
                stripped = line.strip()
                if stripped in from_replacements:
                    arg_name, odh_img, rhoai_img, alias = from_replacements[stripped]
                    merged.append(f"ARG {arg_name}_ODH={odh_img}\n")
                    merged.append(f"ARG {arg_name}_RHOAI={rhoai_img}\n")
                    merged.append(f"ARG {arg_name}=${{{arg_name}_${{BUILD_MODE}}}}\n")
                    merged.append(f"FROM ${{{arg_name}}}{alias}\n")
                else:
                    merged.append(line)
        elif tag == "replace":
            odh_block = odh_lines[i1:i2]
            rhoai_block = rhoai_lines[j1:j2]
            # Check for FROM line replacements
            from_handled = False
            for line in odh_block + rhoai_block:
                stripped = line.strip()
                if stripped in from_replacements:
                    arg_name, odh_img, rhoai_img, alias = from_replacements[stripped]
                    merged.append(f"ARG {arg_name}_ODH={odh_img}\n")
                    merged.append(f"ARG {arg_name}_RHOAI={rhoai_img}\n")
                    merged.append(f"ARG {arg_name}=${{{arg_name}_${{BUILD_MODE}}}}\n")
                    merged.append(f"FROM ${{{arg_name}}}{alias}\n")
                    from_handled = True
                    break
            if not from_handled:
                _emit_conditional_block(merged, odh_block, rhoai_block)
        elif tag == "insert":
            _emit_conditional_block(merged, None, rhoai_lines[j1:j2])
        elif tag == "delete":
            _emit_conditional_block(merged, odh_lines[i1:i2], None)

    return "".join(merged)


def _merge_strategy_d(odh: str, rhoai: str, pair: MatchedPair) -> str:
    """Strategy D: radically different files. Multi-stage conditional build."""
    # Rename all stages in ODH and RHOAI to avoid conflicts, then select final
    odh_stages = _rename_stages(odh, "odh")
    rhoai_stages = _rename_stages(rhoai, "rhoai")

    header = textwrap.dedent("""\
        # Unified Dockerfile – select build mode via BUILD_MODE arg
        ARG BUILD_MODE=ODH

        # ============================================================
        # ODH Build
        # ============================================================
    """)

    footer_bridge = textwrap.dedent("""
        # ============================================================
        # RHOAI Build
        # ============================================================
    """)

    # Determine last stage names
    odh_last = _last_stage_name(odh_stages, "odh-final")
    rhoai_last = _last_stage_name(rhoai_stages, "rhoai-final")

    selector = textwrap.dedent(f"""
        # ============================================================
        # Stage selector – picks the build based on BUILD_MODE
        # ============================================================
        FROM ${{{odh_last}}} AS odh-output
        FROM ${{{rhoai_last}}} AS rhoai-output

        ARG BUILD_MODE=ODH
        FROM ${{BUILD_MODE}}-output AS final
    """).lstrip("\n")

    # If we can't reliably parse stages, fall back to simple concatenation
    merged = header + odh_stages + "\n" + footer_bridge + rhoai_stages + "\n"

    # Only add the selector if both sides have identifiable last stages
    if odh_last and rhoai_last:
        merged += selector
    else:
        pair.warnings.append(
            "Could not reliably identify final stages; manual review recommended."
        )

    return merged


def _rename_stages(content: str, prefix: str) -> str:
    """Prefix all stage names in FROM ... AS <name> to avoid collisions."""
    lines = content.splitlines(keepends=True)
    result = []
    stage_map = {}
    stage_count = 0
    for line in lines:
        stripped = line.strip()
        if stripped.upper().startswith("FROM "):
            parts = stripped.split()
            # Handle FROM image AS name
            if len(parts) >= 4 and parts[2].upper() == "AS":
                old_name = parts[3]
                new_name = f"{prefix}-{old_name}"
                stage_map[old_name] = new_name
                parts[3] = new_name
                line = " ".join(parts) + "\n"
            else:
                # Add a stage name
                new_name = f"{prefix}-stage-{stage_count}"
                parts.insert(2, "AS")
                parts.insert(3, new_name)
                stage_map[f"__stage_{stage_count}"] = new_name
                line = " ".join(parts) + "\n"
            stage_count += 1
        else:
            # Replace references to old stage names (e.g., COPY --from=builder)
            for old, new in stage_map.items():
                if old.startswith("__"):
                    continue
                line = line.replace(f"--from={old}", f"--from={new}")
        result.append(line)
    return "".join(result)


def _last_stage_name(content: str, fallback: str) -> str:
    """Return the AS name of the last FROM line in content."""
    last = fallback
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.upper().startswith("FROM "):
            parts = stripped.split()
            if len(parts) >= 4 and parts[2].upper() == "AS":
                last = parts[3]
    return last


# ---------------------------------------------------------------------------
# Phase 5: Output – write files and generate documentation
# ---------------------------------------------------------------------------

def _dir_for_pair(pair: MatchedPair, multi_component_repos: set[str]) -> Path:
    """Determine the output directory for a matched pair."""
    base = OUTPUT_DIR / pair.repo_name
    if pair.repo_name in multi_component_repos:
        # Use a short suffix derived from the normalized component name
        suffix = pair.odh.norm_name
        # Remove the repo name prefix if present to keep it short
        if suffix.startswith(pair.repo_name + "-"):
            suffix = suffix[len(pair.repo_name) + 1:]
        elif suffix.startswith("odh-"):
            suffix = suffix[4:]
        suffix = suffix or "default"
        return base / suffix
    return base


def write_pair(pair: MatchedPair):
    """Write Dockerfile.ODH, Dockerfile.RHOAI, Dockerfile.Konflux, README.md."""
    d = pair.dir_path
    d.mkdir(parents=True, exist_ok=True)

    if pair.odh_content:
        (d / "Dockerfile.ODH").write_text(pair.odh_content)
    if pair.rhoai_content:
        (d / "Dockerfile.RHOAI").write_text(pair.rhoai_content)
    if pair.merged_content:
        (d / "Dockerfile.Konflux").write_text(pair.merged_content)

    _write_readme(pair, d)


def _write_readme(pair: MatchedPair, d: Path):
    """Generate a per-component README.md."""
    strategy_desc = {
        "A": "Near-identical (Strategy A) -- files are effectively the same; BUILD_MODE ARG added for consistency.",
        "B/C": "Conditional merge (Strategy B/C) -- differing lines wrapped in BUILD_MODE conditionals.",
        "D": "Multi-stage (Strategy D) -- radically different files; each mode is a separate build stage selected at final FROM.",
    }
    warn_section = ""
    if pair.warnings:
        warn_section = "## Warnings\n\n" + "\n".join(f"- {w}" for w in pair.warnings) + "\n\n"

    extra_args_section = ""
    if pair.extra_args:
        extra_args_section = "## Additional Build Args\n\n" + "\n".join(
            f"- `{a}`: base image override" for a in pair.extra_args
        ) + "\n\n"

    error_section = ""
    if pair.error:
        error_section = f"## Errors\n\n- {pair.error}\n\n"

    readme = (
        f"# {pair.repo_name} -- Dockerfile.Konflux\n\n"
        f"## Components\n\n"
        f"| Side  | Component Name | Repo | Branch | Dockerfile |\n"
        f"|-------|---------------|------|--------|------------|\n"
        f"| ODH   | `{pair.odh.component_name}` | `{pair.odh.url}` | `{pair.odh.revision}` | `{pair.odh.dockerfile_url}` |\n"
        f"| RHOAI | `{pair.rhoai.component_name}` | `{pair.rhoai.url}` | `{pair.rhoai.revision}` | `{pair.rhoai.dockerfile_url}` |\n\n"
        f"## Merge Strategy\n\n"
        f"{strategy_desc.get(pair.strategy, 'Unknown')}\n\n"
        f"## Build Modes\n\n"
        f"| Mode  | Description |\n"
        f"|-------|-------------|\n"
        f"| ODH   | Non-hermetic community build (opendatahub-io) |\n"
        f"| RHOAI | Hermetic product build (red-hat-data-services / Konflux) |\n\n"
        f"## Build Commands\n\n"
        f"```bash\n"
        f"# ODH build\n"
        f"docker build --build-arg BUILD_MODE=ODH -f Dockerfile.Konflux .\n\n"
        f"# RHOAI build\n"
        f"docker build --build-arg BUILD_MODE=RHOAI -f Dockerfile.Konflux .\n"
        f"```\n\n"
        f"{extra_args_section}{warn_section}{error_section}"
    )

    (d / "README.md").write_text(readme)


def write_report(
    matched: list[MatchedPair],
    odh_only: list[ComponentInfo],
    rhoai_only: list[ComponentInfo],
    errors: list[MatchedPair],
):
    """Write the overall Dockerfiles/report.md."""
    strat_counts = defaultdict(int)
    for p in matched:
        strat_counts[p.strategy or "error"] += 1

    lines = [
        "# ODH & RHOAI Dockerfile Merge Report\n\n",
        "## Summary\n\n",
        f"- **Total matched pairs**: {len(matched)}\n",
        f"- **ODH-only components** (no RHOAI counterpart): {len(odh_only)}\n",
        f"- **RHOAI-only components** (no ODH counterpart): {len(rhoai_only)}\n",
        f"- **Merge failures**: {len(errors)}\n\n",
        "### Strategy Breakdown\n\n",
        "| Strategy | Count | Description |\n",
        "|----------|-------|-------------|\n",
        f"| A | {strat_counts.get('A', 0)} | Near-identical |\n",
        f"| B/C | {strat_counts.get('B/C', 0)} | Conditional merge |\n",
        f"| D | {strat_counts.get('D', 0)} | Multi-stage |\n",
        f"| error | {strat_counts.get('error', 0)} | Failed |\n\n",
    ]

    # Matched table
    lines.append("## Matched Components\n\n")
    lines.append("| Repo | ODH Component | RHOAI Component | Strategy | Notes |\n")
    lines.append("|------|--------------|-----------------|----------|-------|\n")
    for p in sorted(matched, key=lambda x: x.repo_name):
        notes = p.error or ""
        lines.append(
            f"| {p.repo_name} | `{p.odh.component_name}` | `{p.rhoai.component_name}` "
            f"| {p.strategy or 'error'} | {notes} |\n"
        )

    # ODH only
    lines.append("\n## ODH-Only Components (no RHOAI match)\n\n")
    lines.append("| Component | Repo | Dockerfile |\n")
    lines.append("|-----------|------|------------|\n")
    for c in sorted(odh_only, key=lambda x: x.repo_name):
        lines.append(f"| `{c.component_name}` | `{c.repo_name}` | `{c.dockerfile_url}` |\n")

    # RHOAI only
    lines.append("\n## RHOAI-Only Components (no ODH match)\n\n")
    lines.append("| Component | Repo | Dockerfile |\n")
    lines.append("|-----------|------|------------|\n")
    for c in sorted(rhoai_only, key=lambda x: x.repo_name):
        lines.append(f"| `{c.component_name}` | `{c.repo_name}` | `{c.dockerfile_url}` |\n")

    # Errors
    if errors:
        lines.append("\n## Merge/Download Errors\n\n")
        lines.append("| Repo | ODH Component | RHOAI Component | Error |\n")
        lines.append("|------|--------------|-----------------|-------|\n")
        for p in errors:
            lines.append(
                f"| {p.repo_name} | `{p.odh.component_name}` | `{p.rhoai.component_name}` "
                f"| {p.error} |\n"
            )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "report.md").write_text("".join(lines))


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("=" * 60)
    print("ODH & RHOAI Dockerfile Merge Tool")
    print("=" * 60)

    # Phase 1
    print("\n[Phase 1] Parsing YAML files...")
    odh_components = parse_odh_yaml(ODH_YAML)
    rhoai_components = parse_rhoai_yaml(RHOAI_YAML)
    print(f"  ODH components:  {len(odh_components)}")
    print(f"  RHOAI components: {len(rhoai_components)}")

    # Phase 2
    print("\n[Phase 2] Correlating components...")
    matched, odh_only, rhoai_only = correlate(odh_components, rhoai_components)
    print(f"  Matched pairs:   {len(matched)}")
    print(f"  ODH-only:        {len(odh_only)}")
    print(f"  RHOAI-only:      {len(rhoai_only)}")

    # Determine multi-component repos
    repo_counts = defaultdict(int)
    for p in matched:
        repo_counts[p.repo_name] += 1
    multi_repos = {r for r, c in repo_counts.items() if c > 1}

    # Assign output directories
    for p in matched:
        p.dir_path = _dir_for_pair(p, multi_repos)

    # Phase 3
    print("\n[Phase 3] Downloading Dockerfiles...")
    for i, pair in enumerate(matched, 1):
        status = f"  [{i}/{len(matched)}] {pair.repo_name}/{pair.odh.norm_name}"
        try:
            download_pair(pair)
            if pair.error:
                print(f"{status} -- DOWNLOAD ERROR: {pair.error}")
            else:
                print(f"{status} -- OK")
        except Exception as e:
            pair.error = str(e)
            print(f"{status} -- EXCEPTION: {e}")

    # Phase 4
    print("\n[Phase 4] Merging Dockerfiles...")
    for i, pair in enumerate(matched, 1):
        status = f"  [{i}/{len(matched)}] {pair.repo_name}/{pair.odh.norm_name}"
        try:
            merge_dockerfiles(pair)
            if pair.error:
                print(f"{status} -- SKIP (prior error)")
            else:
                print(f"{status} -- Strategy {pair.strategy}")
        except Exception as e:
            pair.error = f"Merge error: {e}"
            print(f"{status} -- MERGE ERROR: {e}")

    # Phase 5
    print("\n[Phase 5] Writing output files...")
    for pair in matched:
        try:
            write_pair(pair)
        except Exception as e:
            print(f"  Error writing {pair.repo_name}: {e}")

    errors = [p for p in matched if p.error]
    write_report(matched, odh_only, rhoai_only, errors)

    print(f"\n{'=' * 60}")
    print(f"Done. Output in: {OUTPUT_DIR}")
    print(f"  Matched: {len(matched)}  |  Errors: {len(errors)}")
    print(f"  ODH-only: {len(odh_only)}  |  RHOAI-only: {len(rhoai_only)}")
    print(f"  Report: {OUTPUT_DIR / 'report.md'}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()

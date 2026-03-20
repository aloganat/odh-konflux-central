---
name: Dockerfile Unification Script
overview: Build a Python automation script that parses both ODH and RHOAI gitops YAMLs, correlates components by repo name and component identity, downloads each pair of Dockerfiles from GitHub, merges them into a single parameterized Dockerfile.Konflux using a BUILD_MODE ARG, and generates per-component READMEs plus an overall report.
todos:
  - id: setup
    content: Create requirements.txt with pyyaml and set up project structure
    status: completed
  - id: parse-yaml
    content: Implement YAML parsing for both ODH (direct Component docs) and RHOAI (Go-template-based ProjectDevelopmentStreamTemplate) files
    status: completed
  - id: correlate
    content: "Implement component correlation: normalize repo names/component names, match ODH<->RHOAI pairs, identify unmatched components"
    status: completed
  - id: download
    content: Implement Dockerfile download from raw.githubusercontent.com, handling context+dockerfileUrl path resolution and error cases
    status: completed
  - id: merge-engine
    content: "Implement the merge engine with strategies A-D: diff comparison, similarity scoring, conditional BUILD_MODE parameterization, multi-stage fallback"
    status: completed
  - id: generate-docs
    content: Generate per-component README.md and overall Dockerfiles/report.md with statistics and unmatched component lists
    status: completed
  - id: run-and-verify
    content: Execute the script, review output, and fix any issues with downloads/merges/edge cases
    status: completed
isProject: false
---

# ODH and RHOAI Dockerfile Merge -- Execution Plan

## Scope and Scale

- ~80 ODH components from [opendatahub-ci-components.yaml](/Users/dchouras/RHODS/DevOps/konflux-release-data/tenants-config/cluster/stone-prd-rh01/tenants/open-data-hub-tenant/opendatahub-ci-components.yaml)
- ~70 RHOAI components from [ProjectDevelopmentStream-v3.4.yaml](/Users/dchouras/RHODS/DevOps/konflux-release-data/tenants-config/cluster/stone-prod-p02/tenants/rhoai-tenant/v3.4/ProjectDevelopmentStream-v3.4.yaml)
- Multi-component repos (e.g., `notebooks` ~25 components, `odh-dashboard` ~8, `kserve` ~5, `data-science-pipelines` ~5, `distributed-workloads` ~10)
- This will be automated via a Python script; manual merge for 100+ Dockerfiles is impractical

## Architecture: Single Python Script

Create `merge_dockerfiles.py` in the workspace root. It will perform all phases sequentially.

### Phase 1: Parse and Extract Components

- Parse both YAML files using `pyyaml`
- **ODH**: Iterate `---`-separated documents, filter `kind: Component`, extract: `metadata.name`, `spec.source.git.url`, `.revision`, `.context`, `.dockerfileUrl`
- **RHOAI**: Parse the `ProjectDevelopmentStreamTemplate` and extract from `spec.resources[]` where `kind: Component`. Strip Go template syntax (`{{.versionName}}`, `{{.branch}}`) to get the structural component name and leave branch as a placeholder that we resolve from the template values (`rhoai-3.4`)

### Phase 2: Correlate Components

Matching strategy (multi-step):

1. **Normalize repo names**: Strip trailing `.git` and `/` from URLs, extract last path segment (e.g., `https://github.com/opendatahub-io/kserve` and `https://github.com/red-hat-data-services/kserve.git` both yield `kserve`)
2. **Normalize component names**: Strip `-ci` suffix from ODH names, strip `-{{.versionName}}` (or the resolved `-v3-4`) from RHOAI names
3. **Primary match**: Group by (repo_name, normalized_component_name). Exact component-name match pairs them.
4. **Fallback match**: For same-repo components that don't name-match, attempt matching by dockerfile path similarity (e.g., `backend/Dockerfile` vs `backend/Dockerfile.konflux.api` share the `backend/` prefix and `api` keyword)
5. **Unmatched**: Record any component without a counterpart for the final report

### Phase 3: Download Dockerfiles

- Construct raw GitHub URLs: `https://raw.githubusercontent.com/{org}/{repo}/{branch}/{context_path}/{dockerfileUrl}`
  - Handle the context + dockerfileUrl combination carefully (some dockerfileUrls are absolute from repo root like `./ray-operator/Dockerfile.rhoai`, some are relative to context)
- Download via `urllib.request` (no external dependencies needed)
- Save each pair into `Dockerfiles/{repo_name}/{component_id}/Dockerfile.ODH` and `Dockerfile.RHOAI`
  - For repos with a single component: `Dockerfiles/{repo_name}/`
  - For repos with multiple components: `Dockerfiles/{repo_name}/{component_suffix}/` (e.g., `kserve/agent/`, `kserve/controller/`)

### Phase 4: Intelligent Merge

For each matched pair, produce `Dockerfile.Konflux` using these strategies:

**Strategy A -- Identical Files**: If the two Dockerfiles are identical (or differ only in whitespace/comments), emit a single file with `ARG BUILD_MODE=ODH` at the top (no other changes needed). Flag in README as "identical".

**Strategy B -- Different Base Images Only**: Use `ARG BUILD_MODE=ODH` and `ARG BASE_IMAGE` with a conditional default:

```dockerfile
ARG BUILD_MODE=ODH
ARG BASE_IMAGE=${BUILD_MODE:+default_based_on_mode}
FROM ${BASE_IMAGE} AS builder
```

Or use a shell-based approach in an entrypoint script if needed.

**Strategy C -- Divergent Build Steps**: Use conditional RUN blocks:

```dockerfile
ARG BUILD_MODE=ODH
FROM base_image
RUN if [ "$BUILD_MODE" = "RHOAI" ]; then \
      <rhoai-specific steps>; \
    else \
      <odh-specific steps>; \
    fi
```

**Strategy D -- Radically Different Files**: Use multi-stage conditional builds:

```dockerfile
ARG BUILD_MODE=ODH

FROM image1 AS odh-build
# ... full ODH dockerfile steps ...

FROM image2 AS rhoai-build
# ... full RHOAI dockerfile steps ...

FROM ${BUILD_MODE}-build AS final
# (selected stage based on BUILD_MODE value matching stage name)
```

The script should:

1. Compute a diff between the two files
2. Select strategy based on similarity ratio (using `difflib.SequenceMatcher`)
  - ratio > 0.95 --> Strategy A
  - ratio > 0.6 --> Strategy B/C (line-by-line merge with conditionals)
  - ratio <= 0.6 --> Strategy D (multi-stage)
3. For Strategy B/C: identify differing lines, wrap them in `BUILD_MODE` conditionals
4. For all strategies: ensure base image references use digests where the original already does; flag tag-only references in a warnings section of the README

### Phase 5: Generate Documentation

**Per-component `README.md`** containing:

- Component name (ODH and RHOAI)
- Source repos and branches
- Merge strategy used (A/B/C/D)
- `BUILD_MODE` values: `ODH` and `RHOAI`
- Any additional build-args introduced
- Build commands: `docker build --build-arg BUILD_MODE=ODH .` / `docker build --build-arg BUILD_MODE=RHOAI .`
- Diff summary (what differs between the two modes)
- Warnings (e.g., base images using tags instead of digests)

**Overall `Dockerfiles/report.md`** containing:

- Summary statistics: total components, matched, unmatched, merge strategy breakdown
- Table of all matched components with merge strategy
- List of ODH-only components (no RHOAI counterpart)
- List of RHOAI-only components (no ODH counterpart)
- List of components that failed to download or merge (with error details)

## Output Directory Structure

```
Dockerfiles/
  report.md
  {repo_name}/                         # for single-component repos
    Dockerfile.ODH
    Dockerfile.RHOAI
    Dockerfile.Konflux
    README.md
  {repo_name}/{component_suffix}/      # for multi-component repos
    Dockerfile.ODH
    Dockerfile.RHOAI
    Dockerfile.Konflux
    README.md
```

## Key Edge Cases to Handle

- **RHOAI Go templates**: Replace `{{.branch}}` with `rhoai-3.4` and `{{.versionName}}` with `v3-4` for actual values
- **URL normalization**: Strip `.git` suffix, handle trailing slashes
- **Context + dockerfileUrl resolution**: Some dockerfileUrl paths are relative to context, some are relative to repo root (e.g., `./ray-operator/Dockerfile.rhoai` when context is `./ray-operator/`)
- **Multi-component repos**: `notebooks` (~~25 components), `odh-dashboard` (~~8), `kserve` (~~5), `data-science-pipelines` (~~5), `distributed-workloads` (~10) -- need subdirectories per component
- **Download failures**: Some branches or files may not exist; log errors and continue
- **Base image digests**: Check if FROM lines use `@sha256:...` format; warn when they use tags only

## Dependencies

- Python 3 (standard library only: `yaml` needs `pip install pyyaml`)
- `requirements.txt` with `pyyaml` (only external dependency)
- Network access to `raw.githubusercontent.com` for downloading Dockerfiles


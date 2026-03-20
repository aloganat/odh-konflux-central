# guardrails-detectors -- Dockerfile.Konflux

## Components

| Side  | Component Name | Repo | Branch | Dockerfile |
|-------|---------------|------|--------|------------|
| ODH   | `fms-guardrails-hf-detector-ci` | `https://github.com/opendatahub-io/guardrails-detectors` | `stable` | `Dockerfile.hf` |
| RHOAI | `odh-guardrails-detector-huggingface-runtime-v3-4` | `https://github.com/red-hat-data-services/guardrails-detectors` | `rhoai-3.4` | `Dockerfile.konflux.hf` |

## Merge Strategy

Conditional merge (Strategy B/C) -- differing lines wrapped in BUILD_MODE conditionals.

## Build Modes

| Mode  | Description |
|-------|-------------|
| ODH   | Non-hermetic community build (opendatahub-io) |
| RHOAI | Hermetic product build (red-hat-data-services / Konflux) |

## Build Commands

```bash
# ODH build
docker build --build-arg BUILD_MODE=ODH -f Dockerfile.Konflux .

# RHOAI build
docker build --build-arg BUILD_MODE=RHOAI -f Dockerfile.Konflux .
```

## Warnings

- ODH: base image uses tag, not digest: `registry.access.redhat.com/ubi9/ubi-minimal`
- ODH: base image uses tag, not digest: `base`
- ODH: base image uses tag, not digest: `base`
- ODH: base image uses tag, not digest: `base`
- ODH: base image uses tag, not digest: `builder`
- RHOAI: base image uses tag, not digest: `registry.access.redhat.com/ubi9/ubi-minimal`
- RHOAI: base image uses tag, not digest: `base`
- RHOAI: base image uses tag, not digest: `base`
- RHOAI: base image uses tag, not digest: `base`
- RHOAI: base image uses tag, not digest: `builder`


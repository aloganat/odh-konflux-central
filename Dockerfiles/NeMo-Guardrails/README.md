# NeMo-Guardrails -- Dockerfile.Konflux

## Components

| Side  | Component Name | Repo | Branch | Dockerfile |
|-------|---------------|------|--------|------------|
| ODH   | `odh-trustyai-nemo-guardrails-serve-ci` | `https://github.com/opendatahub-io/NeMo-Guardrails.git` | `develop` | `Dockerfile` |
| RHOAI | `odh-trustyai-nemo-guardrails-server-v3-4` | `https://github.com/red-hat-data-services/NeMo-Guardrails` | `rhoai-3.4` | `Dockerfile.konflux` |

## Merge Strategy

Multi-stage (Strategy D) -- radically different files; each mode is a separate build stage selected at final FROM.

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

- ODH: base image uses tag, not digest: `python:3.12-slim`
- RHOAI: base image uses tag, not digest: `packages-build`
- RHOAI: base image uses tag, not digest: `packages-build`
- RHOAI: base image uses tag, not digest: `packages-build`
- RHOAI: base image uses tag, not digest: `packages-build`
- RHOAI: base image uses tag, not digest: `packages-build`
- RHOAI: base image uses tag, not digest: `registry.access.redhat.com/ubi9/python-312:latest`


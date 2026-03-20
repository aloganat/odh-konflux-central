# llama-stack-distribution -- Dockerfile.Konflux

## Components

| Side  | Component Name | Repo | Branch | Dockerfile |
|-------|---------------|------|--------|------------|
| ODH   | `odh-llama-stack-core-ci` | `https://github.com/opendatahub-io/llama-stack-distribution.git` | `main` | `distribution/Containerfile` |
| RHOAI | `odh-llama-stack-core-v3-4` | `https://github.com/red-hat-data-services/llama-stack-distribution` | `rhoai-3.4` | `Dockerfile.konflux` |

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

- RHOAI: base image uses tag, not digest: `${BASE_IMAGE}`


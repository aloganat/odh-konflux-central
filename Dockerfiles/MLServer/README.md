# MLServer -- Dockerfile.Konflux

## Components

| Side  | Component Name | Repo | Branch | Dockerfile |
|-------|---------------|------|--------|------------|
| ODH   | `mlserver-ci` | `https://github.com/opendatahub-io/MLServer.git` | `master` | `Dockerfile` |
| RHOAI | `odh-mlserver-v3-4` | `https://github.com/red-hat-data-services/MLServer.git` | `rhoai-3.4` | `Dockerfile.konflux` |

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

- ODH: base image uses tag, not digest: `${BUILDER_BASE_IMAGE}`
- ODH: base image uses tag, not digest: `${RUNTIME_BASE_IMAGE}`
- RHOAI: base image uses tag, not digest: `${RUNTIME_BASE_IMAGE}`


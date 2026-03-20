# model-registry -- Dockerfile.Konflux

## Components

| Side  | Component Name | Repo | Branch | Dockerfile |
|-------|---------------|------|--------|------------|
| ODH   | `odh-model-registry-ci` | `https://github.com/opendatahub-io/model-registry` | `stable` | `Dockerfile` |
| RHOAI | `odh-model-registry-v3-4` | `https://github.com/red-hat-data-services/model-registry.git` | `rhoai-3.4` | `Dockerfile.konflux` |

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

- ODH: base image uses tag, not digest: `--platform=$BUILDPLATFORM`
- ODH: base image uses tag, not digest: `common`
- ODH: base image uses tag, not digest: `registry.access.redhat.com/ubi9/ubi-minimal:latest`


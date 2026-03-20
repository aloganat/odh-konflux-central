# model-registry-operator -- Dockerfile.Konflux

## Components

| Side  | Component Name | Repo | Branch | Dockerfile |
|-------|---------------|------|--------|------------|
| ODH   | `odh-model-registry-operator-ci` | `https://github.com/opendatahub-io/model-registry-operator` | `stable` | `Dockerfile` |
| RHOAI | `odh-model-registry-operator-v3-4` | `https://github.com/red-hat-data-services/model-registry-operator.git` | `rhoai-3.4` | `Dockerfile.konflux` |

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

- ODH: base image uses tag, not digest: `registry.access.redhat.com/ubi9/go-toolset:1.25.7`
- ODH: base image uses tag, not digest: `registry.access.redhat.com/ubi9/ubi-minimal:latest`


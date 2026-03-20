# odh-dashboard -- Dockerfile.Konflux

## Components

| Side  | Component Name | Repo | Branch | Dockerfile |
|-------|---------------|------|--------|------------|
| ODH   | `odh-mod-arch-automl-ci` | `https://github.com/opendatahub-io/odh-dashboard` | `main` | `packages/automl/Dockerfile.workspace` |
| RHOAI | `odh-mod-arch-automl-v3-4` | `https://github.com/red-hat-data-services/odh-dashboard` | `rhoai-3.4` | `Dockerfile.konflux.automl` |

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

- ODH: base image uses tag, not digest: `${NODE_BASE_IMAGE}`
- ODH: base image uses tag, not digest: `${GOLANG_BASE_IMAGE}`
- ODH: base image uses tag, not digest: `${DISTROLESS_BASE_IMAGE}`
- RHOAI: base image uses tag, not digest: `${NODE_BASE_IMAGE}`
- RHOAI: base image uses tag, not digest: `${GOLANG_BASE_IMAGE}`
- RHOAI: base image uses tag, not digest: `${DISTROLESS_BASE_IMAGE}`


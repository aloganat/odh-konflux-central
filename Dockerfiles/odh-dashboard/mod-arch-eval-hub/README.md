# odh-dashboard -- Dockerfile.Konflux

## Components

| Side  | Component Name | Repo | Branch | Dockerfile |
|-------|---------------|------|--------|------------|
| ODH   | `odh-mod-arch-eval-hub` | `https://github.com/opendatahub-io/odh-dashboard.git` | `main` | `packages/eval-hub/Dockerfile.workspace` |
| RHOAI | `odh-mod-arch-eval-hub-v3-4` | `https://github.com/red-hat-data-services/odh-dashboard.git` | `rhoai-3.4` | `Dockerfile.konflux.eval-hub` |

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


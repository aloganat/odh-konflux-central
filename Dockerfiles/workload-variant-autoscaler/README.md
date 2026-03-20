# workload-variant-autoscaler -- Dockerfile.Konflux

## Components

| Side  | Component Name | Repo | Branch | Dockerfile |
|-------|---------------|------|--------|------------|
| ODH   | `workload-variant-autoscaler-ci` | `https://github.com/opendatahub-io/workload-variant-autoscaler.git` | `main` | `Dockerfile` |
| RHOAI | `odh-workload-variant-autoscaler-controller-v3-4` | `https://github.com/red-hat-data-services/workload-variant-autoscaler` | `rhoai-3.4` | `Dockerfile.konflux` |

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

## Additional Build Args

- `BASE_IMAGE`: base image override
- `BASE_IMAGE_1`: base image override


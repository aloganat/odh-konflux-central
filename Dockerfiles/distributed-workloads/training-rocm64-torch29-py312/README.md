# distributed-workloads -- Dockerfile.Konflux

## Components

| Side  | Component Name | Repo | Branch | Dockerfile |
|-------|---------------|------|--------|------------|
| ODH   | `odh-training-rocm64-torch29-py312-ci` | `https://github.com/opendatahub-io/distributed-workloads` | `stable` | `Dockerfile` |
| RHOAI | `odh-training-rocm64-torch29-py312-v3-4` | `https://github.com/red-hat-data-services/distributed-workloads` | `rhoai-3.4` | `Dockerfile.konflux` |

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

## Warnings

- ODH: base image uses tag, not digest: `registry.access.redhat.com/ubi9/python-${PYTHON_VERSION}:${IMAGE_TAG}`


# mlflow -- Dockerfile.Konflux

## Components

| Side  | Component Name | Repo | Branch | Dockerfile |
|-------|---------------|------|--------|------------|
| ODH   | `mlflow-ci` | `https://github.com/opendatahub-io/mlflow` | `master` | `Dockerfile.konflux` |
| RHOAI | `odh-mlflow-v3-4` | `https://github.com/red-hat-data-services/mlflow.git` | `rhoai-3.4` | `Dockerfile.konflux` |

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
- `BASE_IMAGE_2`: base image override

## Warnings

- ODH: base image uses tag, not digest: `registry.access.redhat.com/ubi9/nodejs-20:9.7`
- ODH: base image uses tag, not digest: `registry.access.redhat.com/ubi9/python-312:9.7`
- ODH: base image uses tag, not digest: `registry.access.redhat.com/ubi9/ubi-minimal:9.7`


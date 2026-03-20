# data-science-pipelines -- Dockerfile.Konflux

## Components

| Side  | Component Name | Repo | Branch | Dockerfile |
|-------|---------------|------|--------|------------|
| ODH   | `odh-ml-pipelines-api-server-v2-ci` | `https://github.com/opendatahub-io/data-science-pipelines` | `master` | `backend/Dockerfile` |
| RHOAI | `odh-ml-pipelines-api-server-v2-v3-4` | `https://github.com/red-hat-data-services/data-science-pipelines.git` | `rhoai-3.4` | `backend/Dockerfile.konflux.api` |

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

## Warnings

- ODH: base image uses tag, not digest: `registry.access.redhat.com/ubi9/go-toolset:1.25.7-1771417345`
- ODH: base image uses tag, not digest: `registry.access.redhat.com/ubi9/python-311`
- ODH: base image uses tag, not digest: `registry.access.redhat.com/ubi9/ubi-minimal:9.5`


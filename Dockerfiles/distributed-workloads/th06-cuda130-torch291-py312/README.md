# distributed-workloads -- Dockerfile.Konflux

## Components

| Side  | Component Name | Repo | Branch | Dockerfile |
|-------|---------------|------|--------|------------|
| ODH   | `odh-th06-cuda130-torch291-py312-ci` | `https://github.com/opendatahub-io/distributed-workloads.git` | `stable` | `Dockerfile` |
| RHOAI | `odh-th06-cuda130-torch291-py312-v3-4` | `https://github.com/red-hat-data-services/distributed-workloads` | `rhoai-3.4` | `Dockerfile.konflux.cuda` |

## Merge Strategy

Near-identical (Strategy A) -- files are effectively the same; BUILD_MODE ARG added for consistency.

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

- ODH: base image uses tag, not digest: `${BASE_IMAGE}`
- ODH: base image uses tag, not digest: `${BASE_IMAGE}`
- RHOAI: base image uses tag, not digest: `${BASE_IMAGE}`
- RHOAI: base image uses tag, not digest: `${BASE_IMAGE}`


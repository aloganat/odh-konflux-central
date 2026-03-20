# notebooks -- Dockerfile.Konflux

## Components

| Side  | Component Name | Repo | Branch | Dockerfile |
|-------|---------------|------|--------|------------|
| ODH   | `odh-pipeline-runtime-pytorch-llmcompressor-cuda-py312-ci` | `https://github.com/opendatahub-io/notebooks.git` | `stable` | `runtimes/pytorch+llmcompressor/ubi9-python-3.12/Dockerfile.cuda` |
| RHOAI | `odh-pipeline-runtime-pytorch-llmcompressor-cuda-py312-v3-4` | `https://github.com/red-hat-data-services/notebooks` | `rhoai-3.4` | `runtimes/pytorch+llmcompressor/ubi9-python-3.12/Dockerfile.konflux.cuda` |

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

- ODH: base image uses tag, not digest: `${BASE_IMAGE}`
- ODH: base image uses tag, not digest: `cuda-base`
- RHOAI: base image uses tag, not digest: `${BASE_IMAGE}`
- RHOAI: base image uses tag, not digest: `cuda-base`


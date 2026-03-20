# notebooks -- Dockerfile.Konflux

## Components

| Side  | Component Name | Repo | Branch | Dockerfile |
|-------|---------------|------|--------|------------|
| ODH   | `odh-workbench-jupyter-tensorflow-cuda-py312-ubi9-ci` | `https://github.com/opendatahub-io/notebooks` | `stable` | `jupyter/tensorflow/ubi9-python-3.12/Dockerfile.cuda` |
| RHOAI | `odh-workbench-jupyter-tensorflow-cuda-py312-v3-4` | `https://github.com/red-hat-data-services/notebooks` | `rhoai-3.4` | `jupyter/tensorflow/ubi9-python-3.12/Dockerfile.konflux.cuda` |

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

- ODH: base image uses tag, not digest: `registry.access.redhat.com/ubi9/go-toolset:latest`
- ODH: base image uses tag, not digest: `${BASE_IMAGE}`
- ODH: base image uses tag, not digest: `cuda-base`
- ODH: base image uses tag, not digest: `cuda-jupyter-minimal`
- ODH: base image uses tag, not digest: `cuda-jupyter-datascience`
- RHOAI: base image uses tag, not digest: `registry.access.redhat.com/ubi9/go-toolset:latest`
- RHOAI: base image uses tag, not digest: `${BASE_IMAGE}`
- RHOAI: base image uses tag, not digest: `cuda-base`
- RHOAI: base image uses tag, not digest: `cuda-jupyter-minimal`
- RHOAI: base image uses tag, not digest: `cuda-jupyter-datascience`


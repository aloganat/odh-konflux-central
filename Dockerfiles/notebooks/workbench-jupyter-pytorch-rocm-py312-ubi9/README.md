# notebooks -- Dockerfile.Konflux

## Components

| Side  | Component Name | Repo | Branch | Dockerfile |
|-------|---------------|------|--------|------------|
| ODH   | `odh-workbench-jupyter-pytorch-rocm-py312-ubi9-ci` | `https://github.com/opendatahub-io/notebooks` | `stable` | `jupyter/rocm/pytorch/ubi9-python-3.12/Dockerfile.rocm` |
| RHOAI | `odh-workbench-jupyter-pytorch-rocm-py312-v3-4` | `https://github.com/red-hat-data-services/notebooks` | `rhoai-3.4` | `jupyter/rocm/pytorch/ubi9-python-3.12/Dockerfile.konflux.rocm` |

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
- ODH: base image uses tag, not digest: `rocm-base`
- ODH: base image uses tag, not digest: `rocm-jupyter-minimal`
- ODH: base image uses tag, not digest: `rocm-jupyter-datascience`
- RHOAI: base image uses tag, not digest: `registry.access.redhat.com/ubi9/go-toolset:latest`
- RHOAI: base image uses tag, not digest: `${BASE_IMAGE}`
- RHOAI: base image uses tag, not digest: `rocm-base`
- RHOAI: base image uses tag, not digest: `rocm-jupyter-minimal`
- RHOAI: base image uses tag, not digest: `rocm-jupyter-datascience`


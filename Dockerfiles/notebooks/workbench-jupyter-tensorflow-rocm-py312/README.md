# notebooks -- Dockerfile.Konflux

## Components

| Side  | Component Name | Repo | Branch | Dockerfile |
|-------|---------------|------|--------|------------|
| ODH   | `odh-workbench-jupyter-tensorflow-rocm-py312-ci` | `https://github.com/opendatahub-io/notebooks.git` | `stable` | `jupyter/rocm/tensorflow/ubi9-python-3.12/build-args/rocm.conf` |
| RHOAI | `odh-workbench-jupyter-tensorflow-rocm-py312-v3-4` | `https://github.com/red-hat-data-services/notebooks` | `rhoai-3.4` | `jupyter/rocm/tensorflow/ubi9-python-3.12/Dockerfile.konflux.rocm` |

## Merge Strategy

Multi-stage (Strategy D) -- radically different files; each mode is a separate build stage selected at final FROM.

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

- RHOAI: base image uses tag, not digest: `registry.access.redhat.com/ubi9/go-toolset:latest`
- RHOAI: base image uses tag, not digest: `${BASE_IMAGE}`
- RHOAI: base image uses tag, not digest: `rocm-base`
- RHOAI: base image uses tag, not digest: `rocm-jupyter-minimal`
- RHOAI: base image uses tag, not digest: `rocm-jupyter-datascience`


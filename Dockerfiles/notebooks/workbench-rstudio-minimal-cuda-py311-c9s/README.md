# notebooks -- Dockerfile.Konflux

## Components

| Side  | Component Name | Repo | Branch | Dockerfile |
|-------|---------------|------|--------|------------|
| ODH   | `odh-workbench-rstudio-minimal-cuda-py311-c9s-ci` | `https://github.com/opendatahub-io/notebooks` | `main` | `rstudio/c9s-python-3.11/Dockerfile.cuda` |
| RHOAI | `odh-pipeline-runtime-pytorch-cuda-py312-v3-4` | `https://github.com/red-hat-data-services/notebooks` | `rhoai-3.4` | `runtimes/pytorch/ubi9-python-3.12/Dockerfile.konflux.cuda` |

## Merge Strategy

Unknown

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

## Errors

- ODH download failed: HTTP 404 downloading https://raw.githubusercontent.com/opendatahub-io/notebooks/main/rstudio/c9s-python-3.11/Dockerfile.cuda


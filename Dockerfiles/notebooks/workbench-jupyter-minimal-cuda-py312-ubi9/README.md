# notebooks -- Dockerfile.Konflux

## Components

| Side  | Component Name | Repo | Branch | Dockerfile |
|-------|---------------|------|--------|------------|
| ODH   | `odh-workbench-jupyter-minimal-cuda-py312-ubi9-ci` | `https://github.com/opendatahub-io/notebooks` | `stable` | `jupyter/minimal/ubi9-python-3.12/Dockerfile.cuda` |
| RHOAI | `odh-workbench-jupyter-minimal-cuda-py312-v3-4` | `https://github.com/red-hat-data-services/notebooks` | `rhoai-3.4` | `jupyter/minimal/ubi9-python-3.12/Dockerfile.konflux.cuda` |

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
- ODH: base image uses tag, not digest: `cuda-base`
- RHOAI: base image uses tag, not digest: `${BASE_IMAGE}`
- RHOAI: base image uses tag, not digest: `cuda-base`


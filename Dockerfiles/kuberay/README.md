# kuberay -- Dockerfile.Konflux

## Components

| Side  | Component Name | Repo | Branch | Dockerfile |
|-------|---------------|------|--------|------------|
| ODH   | `odh-kuberay-operator-controller-ci` | `https://github.com/opendatahub-io/kuberay` | `main` | `./ray-operator/Dockerfile.rhoai` |
| RHOAI | `odh-kuberay-operator-controller-v3-4` | `https://github.com/red-hat-data-services/kuberay.git` | `rhoai-3.4` | `./ray-operator/Dockerfile.konflux` |

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

- ODH download failed: HTTP 404 downloading https://raw.githubusercontent.com/opendatahub-io/kuberay/main/ray-operator/Dockerfile.rhoai


# kserve -- Dockerfile.Konflux

## Components

| Side  | Component Name | Repo | Branch | Dockerfile |
|-------|---------------|------|--------|------------|
| ODH   | `kserve-storage-initializer-ci` | `https://github.com/opendatahub-io/kserve` | `master` | `storage-initializer.Dockerfile` |
| RHOAI | `odh-kserve-storage-initializer-v3-4` | `https://github.com/red-hat-data-services/kserve` | `rhoai-3.4` | `Dockerfiles/storage-initializer.Dockerfile.konflux` |

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

- RHOAI download failed: HTTP 404 downloading https://raw.githubusercontent.com/red-hat-data-services/kserve/rhoai-3.4/python/Dockerfiles/storage-initializer.Dockerfile.konflux


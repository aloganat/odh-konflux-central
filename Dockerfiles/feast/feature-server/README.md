# feast -- Dockerfile.Konflux

## Components

| Side  | Component Name | Repo | Branch | Dockerfile |
|-------|---------------|------|--------|------------|
| ODH   | `odh-feature-server-ci` | `https://github.com/opendatahub-io/feast` | `stable` | `Dockerfile` |
| RHOAI | `odh-feature-server-v3-4` | `https://github.com/red-hat-data-services/feast` | `rhoai-3.4` | `Dockerfiles/Dockerfile.feature-server.konflux` |

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

- RHOAI download failed: HTTP 404 downloading https://raw.githubusercontent.com/red-hat-data-services/feast/rhoai-3.4/sdk/python/feast/infra/feature_servers/multicloud/Dockerfiles/Dockerfile.feature-server.konflux


# openvino_model_server -- Dockerfile.Konflux

## Components

| Side  | Component Name | Repo | Branch | Dockerfile |
|-------|---------------|------|--------|------------|
| ODH   | `openvino-model-server-ci` | `https://github.com/opendatahub-io/openvino_model_server` | `main` | `Dockerfile.redhat` |
| RHOAI | `odh-openvino-model-server-v3-4` | `https://github.com/red-hat-data-services/openvino_model_server` | `rhoai-3.4` | `Dockerfile.konflux` |

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

- ODH: base image uses tag, not digest: `$BASE_IMAGE`
- ODH: base image uses tag, not digest: `base_build`
- ODH: base image uses tag, not digest: `$BUILD_IMAGE`
- ODH: base image uses tag, not digest: `$BUILD_IMAGE`
- ODH: base image uses tag, not digest: `$RELEASE_BASE_IMAGE`
- RHOAI: base image uses tag, not digest: `$BASE_IMAGE`
- RHOAI: base image uses tag, not digest: `base_build`
- RHOAI: base image uses tag, not digest: `$BUILD_IMAGE`
- RHOAI: base image uses tag, not digest: `$BUILD_IMAGE`
- RHOAI: base image uses tag, not digest: `$RELEASE_BASE_IMAGE`


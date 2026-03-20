# llm-d-inference-scheduler -- Dockerfile.Konflux

## Components

| Side  | Component Name | Repo | Branch | Dockerfile |
|-------|---------------|------|--------|------------|
| ODH   | `llm-d-routing-sidecar-ci` | `https://github.com/opendatahub-io/llm-d-inference-scheduler.git` | `main` | `Dockerfile` |
| RHOAI | `odh-llm-d-routing-sidecar-v3-4` | `https://github.com/red-hat-data-services/llm-d-inference-scheduler` | `rhoai-3.4` | `Dockerfile.sidecar.konflux` |

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

- ODH download failed: HTTP 404 downloading https://raw.githubusercontent.com/opendatahub-io/llm-d-inference-scheduler/main/Dockerfile


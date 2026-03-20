# trustyai-service-operator -- Dockerfile.Konflux

## Components

| Side  | Component Name | Repo | Branch | Dockerfile |
|-------|---------------|------|--------|------------|
| ODH   | `ta-lmes-driver-ci` | `https://github.com/opendatahub-io/trustyai-service-operator` | `stable` | `Dockerfile.driver` |
| RHOAI | `odh-ta-lmes-driver-v3-4` | `https://github.com/red-hat-data-services/trustyai-service-operator.git` | `rhoai-3.4` | `Dockerfile.konflux.driver` |

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

- ODH: base image uses tag, not digest: `registry.access.redhat.com/ubi9/go-toolset:1.23`
- ODH: base image uses tag, not digest: `registry.access.redhat.com/ubi9/ubi-minimal:latest`
- RHOAI: base image uses tag, not digest: `registry.access.redhat.com/ubi9/go-toolset:1.23`
- RHOAI: base image uses tag, not digest: `registry.access.redhat.com/ubi9/ubi-minimal:latest`


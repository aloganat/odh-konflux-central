# vllm-orchestrator-gateway -- Dockerfile.Konflux

## Components

| Side  | Component Name | Repo | Branch | Dockerfile |
|-------|---------------|------|--------|------------|
| ODH   | `trustyai-vllm-orchestrator-gateway-ci` | `https://github.com/opendatahub-io/vllm-orchestrator-gateway` | `stable` | `Dockerfile` |
| RHOAI | `odh-trustyai-vllm-orchestrator-gateway-v3-4` | `https://github.com/red-hat-data-services/vllm-orchestrator-gateway` | `rhoai-3.4` | `Dockerfile.konflux` |

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

## Additional Build Args

- `BASE_IMAGE`: base image override

## Warnings

- ODH: base image uses tag, not digest: `rust:1.84.0`
- ODH: base image uses tag, not digest: `rust-builder`
- ODH: base image uses tag, not digest: `gateway-builder`
- ODH: base image uses tag, not digest: `gateway-builder`
- ODH: base image uses tag, not digest: `gateway-builder`
- ODH: base image uses tag, not digest: `${UBI_MINIMAL_BASE_IMAGE}:${UBI_BASE_IMAGE_TAG}`
- RHOAI: base image uses tag, not digest: `${UBI_MINIMAL_BASE_IMAGE}:${UBI_BASE_IMAGE_TAG}`
- RHOAI: base image uses tag, not digest: `rust-builder`
- RHOAI: base image uses tag, not digest: `gateway-builder`
- RHOAI: base image uses tag, not digest: `gateway-builder`
- RHOAI: base image uses tag, not digest: `gateway-builder`
- RHOAI: base image uses tag, not digest: `${UBI_MINIMAL_BASE_IMAGE}:${UBI_BASE_IMAGE_TAG}`


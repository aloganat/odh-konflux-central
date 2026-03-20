# fms-guardrails-orchestrator -- Dockerfile.Konflux

## Components

| Side  | Component Name | Repo | Branch | Dockerfile |
|-------|---------------|------|--------|------------|
| ODH   | `fms-guardrails-orchestrator-ci` | `https://github.com/opendatahub-io/fms-guardrails-orchestrator` | `konflux-poc` | `Dockerfile` |
| RHOAI | `odh-fms-guardrails-orchestrator-v3-4` | `https://github.com/red-hat-data-services/fms-guardrails-orchestrator` | `rhoai-3.4` | `Dockerfile.konflux` |

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

- ODH: base image uses tag, not digest: `rust:1.84.0-bullseye`
- ODH: base image uses tag, not digest: `rust-builder`
- ODH: base image uses tag, not digest: `fms-guardrails-orchestr8-builder`
- ODH: base image uses tag, not digest: `fms-guardrails-orchestr8-builder`
- ODH: base image uses tag, not digest: `fms-guardrails-orchestr8-builder`
- ODH: base image uses tag, not digest: `${UBI_MINIMAL_BASE_IMAGE}:${UBI_BASE_IMAGE_TAG}`
- RHOAI: base image uses tag, not digest: `${UBI_MINIMAL_BASE_IMAGE}:${UBI_BASE_IMAGE_TAG}`
- RHOAI: base image uses tag, not digest: `rust-builder`
- RHOAI: base image uses tag, not digest: `${UBI_MINIMAL_BASE_IMAGE}:${UBI_BASE_IMAGE_TAG}`


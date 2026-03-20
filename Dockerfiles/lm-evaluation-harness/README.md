# lm-evaluation-harness -- Dockerfile.Konflux

## Components

| Side  | Component Name | Repo | Branch | Dockerfile |
|-------|---------------|------|--------|------------|
| ODH   | `ta-lmes-job-ci` | `https://github.com/opendatahub-io/lm-evaluation-harness` | `stable` | `Dockerfile.lmes-job` |
| RHOAI | `odh-ta-lmes-job-v3-4` | `https://github.com/red-hat-data-services/lm-evaluation-harness.git` | `rhoai-3.4` | `Dockerfile.konflux.lmes-job` |

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

- ODH: base image uses tag, not digest: `registry.access.redhat.com/ubi9/python-311:latest`
- ODH: base image uses tag, not digest: `builder`
- ODH: base image uses tag, not digest: `builder`
- ODH: base image uses tag, not digest: `builder`
- ODH: base image uses tag, not digest: `builder`
- RHOAI: base image uses tag, not digest: `registry.access.redhat.com/ubi9/python-311:latest`
- RHOAI: base image uses tag, not digest: `builder`
- RHOAI: base image uses tag, not digest: `builder`
- RHOAI: base image uses tag, not digest: `builder`
- RHOAI: base image uses tag, not digest: `builder`


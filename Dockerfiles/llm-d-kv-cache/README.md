# llm-d-kv-cache -- Dockerfile.Konflux

## Components

| Side  | Component Name | Repo | Branch | Dockerfile |
|-------|---------------|------|--------|------------|
| ODH   | `llm-d-kv-cache-ci` | `https://github.com/opendatahub-io/llm-d-kv-cache.git` | `main` | `Dockerfile` |
| RHOAI | `odh-llm-d-kv-cache-v3-4` | `https://github.com/red-hat-data-services/llm-d-kv-cache` | `rhoai-3.4` | `Dockerfile.konflux` |

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

- ODH: base image uses tag, not digest: `python:3.12-slim`
- ODH: base image uses tag, not digest: `quay.io/projectquay/golang:1.24`
- ODH: base image uses tag, not digest: `registry.access.redhat.com/ubi9/ubi:latest`
- RHOAI: base image uses tag, not digest: `--platform=$TARGETPLATFORM`
- RHOAI: base image uses tag, not digest: `--platform=$TARGETPLATFORM`


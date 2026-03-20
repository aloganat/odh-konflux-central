# kserve -- Dockerfile.Konflux

## Components

| Side  | Component Name | Repo | Branch | Dockerfile |
|-------|---------------|------|--------|------------|
| ODH   | `kserve-agent-ci` | `https://github.com/opendatahub-io/kserve` | `master` | `agent.Dockerfile` |
| RHOAI | `odh-kserve-agent-v3-4` | `https://github.com/red-hat-data-services/kserve` | `rhoai-3.4` | `Dockerfiles/agent.Dockerfile.konflux` |

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

- ODH: base image uses tag, not digest: `registry.access.redhat.com/ubi9/go-toolset:1.25`
- ODH: base image uses tag, not digest: `registry.access.redhat.com/ubi9/ubi-minimal:latest`
- RHOAI: base image uses tag, not digest: `registry.access.redhat.com/ubi9/go-toolset:1.24`
- RHOAI: base image uses tag, not digest: `registry.access.redhat.com/ubi9/ubi-minimal:latest`


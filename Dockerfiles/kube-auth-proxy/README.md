# kube-auth-proxy -- Dockerfile.Konflux

## Components

| Side  | Component Name | Repo | Branch | Dockerfile |
|-------|---------------|------|--------|------------|
| ODH   | `kube-auth-proxy-ci` | `https://github.com/opendatahub-io/kube-auth-proxy` | `main` | `Dockerfile` |
| RHOAI | `odh-kube-auth-proxy-v3-4` | `https://github.com/red-hat-data-services/kube-auth-proxy.git` | `rhoai-3.4` | `Dockerfile.konflux` |

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
- `BASE_IMAGE_1`: base image override

## Warnings

- ODH: base image uses tag, not digest: `--platform=${BUILDPLATFORM}`
- ODH: base image uses tag, not digest: `${RUNTIME_IMAGE}`
- RHOAI: base image uses tag, not digest: `--platform=${BUILDPLATFORM}`


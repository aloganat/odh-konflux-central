# argo-workflows -- Dockerfile.Konflux

## Components

| Side  | Component Name | Repo | Branch | Dockerfile |
|-------|---------------|------|--------|------------|
| ODH   | `odh-data-science-pipelines-argo-argoexec-ci` | `https://github.com/opendatahub-io/argo-workflows` | `main` | `argo-argoexec/Dockerfile.ODH` |
| RHOAI | `odh-data-science-pipelines-argo-argoexec-v3-4` | `https://github.com/red-hat-data-services/argo-workflows.git` | `rhoai-3.4` | `argo-argoexec/Dockerfile.konflux` |

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

- ODH: base image uses tag, not digest: `registry.access.redhat.com/ubi9/go-toolset:1.25`
- ODH: base image uses tag, not digest: `registry.redhat.io/ubi9/ubi-minimal:9.5`


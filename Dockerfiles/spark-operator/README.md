# spark-operator -- Dockerfile.Konflux

## Components

| Side  | Component Name | Repo | Branch | Dockerfile |
|-------|---------------|------|--------|------------|
| ODH   | `spark-operator-ci` | `https://github.com/opendatahub-io/spark-operator.git` | `main` | `Dockerfile` |
| RHOAI | `odh-spark-operator-v3-4` | `https://github.com/red-hat-data-services/spark-operator` | `rhoai-3.4` | `Dockerfile` |

## Merge Strategy

Near-identical (Strategy A) -- files are effectively the same; BUILD_MODE ARG added for consistency.

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

- ODH: base image uses tag, not digest: `golang:1.24.10`
- ODH: base image uses tag, not digest: `${SPARK_IMAGE}`
- RHOAI: base image uses tag, not digest: `golang:1.24.10`
- RHOAI: base image uses tag, not digest: `${SPARK_IMAGE}`


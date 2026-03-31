# Upstream Fixes Needed in konflux-release-data

This document lists the incorrect Dockerfile paths in the konflux-release-data repository YAMLs that need to be fixed.

## Summary

- **7 components** have incorrect paths in their YAML configurations
- **1 component** (kuberay) needs investigation - Dockerfile not found in repository
- All 7 incorrect paths have been identified and corrected locally

## RHOAI Tenant YAML Fixes

**File**: `tenants-config/cluster/stone-prod-p02/tenants/rhoai-tenant/v3.4/ProjectDevelopmentStream-v3.4.yaml`

### 1. odh-feast-operator-v3-4

**Current (incorrect):**
```yaml
dockerfileUrl: infra/feast-operator/Dockerfiles/Dockerfile.feast-operator.konflux
```

**Should be:**
```yaml
dockerfileUrl: Dockerfiles/Dockerfile.feast-operator.konflux
```

**Reason**: File is at root `Dockerfiles/`, not nested under `infra/feast-operator/`

---

### 2. odh-feature-server-v3-4

**Current (incorrect):**
```yaml
dockerfileUrl: sdk/python/feast/infra/feature_servers/multicloud/Dockerfiles/Dockerfile.feature-server.konflux
```

**Should be:**
```yaml
dockerfileUrl: Dockerfiles/Dockerfile.feature-server.konflux
```

**Reason**: File is at root `Dockerfiles/`, not nested under `sdk/python/...`

---

### 3. odh-kserve-storage-initializer-v3-4

**Current (incorrect):**
```yaml
dockerfileUrl: python/Dockerfiles/storage-initializer.Dockerfile.konflux
```

**Should be:**
```yaml
dockerfileUrl: Dockerfiles/storage-initializer.Dockerfile.konflux
```

**Reason**: File is at root `Dockerfiles/`, not under `python/Dockerfiles/`

---

## ODH Tenant YAML Fixes

**File**: `tenants-config/cluster/stone-prd-rh01/tenants/open-data-hub-tenant/opendatahub-ci-components.yaml`

### 4. llm-d-inference-scheduler-ci

**Current (incorrect):**
```yaml
dockerfileUrl: Dockerfile
```

**Should be:**
```yaml
dockerfileUrl: Dockerfile.epp
```

**Reason**: Generic `Dockerfile` doesn't exist; component uses `Dockerfile.epp`

---

### 5. llm-d-routing-sidecar-ci

**Current (incorrect):**
```yaml
dockerfileUrl: Dockerfile
```

**Should be:**
```yaml
dockerfileUrl: Dockerfile.sidecar
```

**Reason**: Generic `Dockerfile` doesn't exist; component uses `Dockerfile.sidecar`

---

### 6. odh-workbench-rstudio-minimal-cpu-py311-c9s-ci

**Current (incorrect):**
```yaml
dockerfileUrl: rstudio/c9s-python-3.11/Dockerfile.cpu
```

**Should be:**
```yaml
dockerfileUrl: rstudio/c9s-python-3.12/Dockerfile.cpu
```

**Reason**: Python 3.11 version doesn't exist in repository; only 3.12 is available

**Additional Note**: Component name also needs review - it's currently matched with RHOAI's `odh-workbench-codeserver-datascience-cpu-py312-v3-4` which is a completely different workbench type (codeserver vs rstudio)

---

### 7. odh-workbench-rstudio-minimal-cuda-py311-c9s-ci

**Current (incorrect):**
```yaml
dockerfileUrl: rstudio/c9s-python-3.11/Dockerfile.cuda
```

**Should be:**
```yaml
dockerfileUrl: rstudio/c9s-python-3.12/Dockerfile.cuda
```

**Reason**: Python 3.11 version doesn't exist in repository; only 3.12 is available

**Additional Note**: Component name also needs review - it's currently matched with RHOAI's `odh-pipeline-runtime-pytorch-cuda-py312-v3-4` which is a completely different component type (pipeline runtime vs workbench)

---

### 8. odh-kuberay-operator-controller-ci

**Current (incorrect):**
```yaml
url: https://github.com/opendatahub-io/kuberay
revision: main
dockerfileUrl: ./ray-operator/Dockerfile.rhoai
```

**Should be:**
```yaml
url: https://github.com/opendatahub-io/kuberay
revision: dev
dockerfileUrl: ./ray-operator/Dockerfile.rhoai
```

**Reason**: The repository's default branch is `dev`, not `main`. The Dockerfile.rhoai exists on the `dev` branch.

**Note**: This is a fork of ray-project/kuberay with `dev` as the default branch.

---

## Verification

All fixes have been tested locally by downloading the Dockerfiles from the corrected paths:

```bash
# All 8 components successfully downloaded and merged
✓ feast-operator
✓ feature-server
✓ kserve-storage-initializer
✓ llm-d-inference-scheduler
✓ llm-d-routing-sidecar
✓ rstudio-cpu-py312
✓ rstudio-cuda-py312
✓ kuberay-operator-controller
```

## Impact

Fixing these 8 errors will improve the merge success rate from **90.5% (76/84)** to **100% (84/84)**.

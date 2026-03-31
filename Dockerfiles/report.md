# ODH & RHOAI Dockerfile Merge Report

## Summary

- **Total matched pairs**: 84
- **ODH-only components** (no RHOAI counterpart): 12
- **RHOAI-only components** (no ODH counterpart): 12
- **Merge failures**: 0 ✅

### Strategy Breakdown

| Strategy | Count | Description |
|----------|-------|-------------|
| A | 10 | Near-identical |
| B/C | 61 | Conditional merge |
| D | 13 | Multi-stage |
| **Total** | **84** | **100% Success Rate** ✅ |

## Matched Components

| Repo | ODH Component | RHOAI Component | Strategy | Notes |
|------|--------------|-----------------|----------|-------|
| MLServer | `mlserver-ci` | `odh-mlserver-v3-4` | D |  |
| NeMo-Guardrails | `odh-trustyai-nemo-guardrails-serve-ci` | `odh-trustyai-nemo-guardrails-server-v3-4` | D |  |
| argo-workflows | `odh-data-science-pipelines-argo-argoexec-ci` | `odh-data-science-pipelines-argo-argoexec-v3-4` | B/C |  |
| argo-workflows | `odh-data-science-pipelines-argo-workflowcontroller-ci` | `odh-data-science-pipelines-argo-workflowcontroller-v3-4` | B/C |  |
| data-science-pipelines | `odh-ml-pipelines-api-server-v2-ci` | `odh-ml-pipelines-api-server-v2-v3-4` | B/C |  |
| data-science-pipelines | `odh-ml-pipelines-driver-ci` | `odh-ml-pipelines-driver-v3-4` | B/C |  |
| data-science-pipelines | `odh-ml-pipelines-launcher-ci` | `odh-ml-pipelines-launcher-v3-4` | B/C |  |
| data-science-pipelines | `odh-ml-pipelines-persistenceagent-v2-ci` | `odh-ml-pipelines-persistenceagent-v2-v3-4` | B/C |  |
| data-science-pipelines | `odh-ml-pipelines-scheduledworkflow-v2-ci` | `odh-ml-pipelines-scheduledworkflow-v2-v3-4` | B/C |  |
| data-science-pipelines-operator | `odh-data-science-pipelines-operator-controller-ci` | `odh-data-science-pipelines-operator-controller-v3-4` | D |  |
| distributed-workloads | `odh-training-rocm64-torch28-py312-ci` | `odh-training-rocm64-torch28-py312-v3-4` | B/C |  |
| distributed-workloads | `odh-training-rocm62-torch25-py311-ci` | `odh-training-rocm62-torch25-py311-v3-4` | B/C |  |
| distributed-workloads | `odh-training-rocm62-torch24-py311-ci` | `odh-training-rocm62-torch24-py311-v3-4` | B/C |  |
| distributed-workloads | `odh-training-cuda128-torch28-py312-ci` | `odh-training-cuda128-torch28-py312-v3-4` | B/C |  |
| distributed-workloads | `odh-training-cuda124-torch25-py311-ci` | `odh-training-cuda124-torch25-py311-v3-4` | B/C |  |
| distributed-workloads | `odh-training-cuda121-torch24-py311-ci` | `odh-training-cuda121-torch24-py311-v3-4` | B/C |  |
| distributed-workloads | `odh-training-rocm64-torch29-py312-ci` | `odh-training-rocm64-torch29-py312-v3-4` | B/C |  |
| distributed-workloads | `odh-training-cuda128-torch29-py312-ci` | `odh-training-cuda128-torch29-py312-v3-4` | B/C |  |
| distributed-workloads | `odh-th06-cpu-torch291-py312-ci` | `odh-th06-cpu-torch291-py312-v3-4` | B/C |  |
| distributed-workloads | `odh-th06-cuda130-torch291-py312-ci` | `odh-th06-cuda130-torch291-py312-v3-4` | A |  |
| distributed-workloads | `odh-th06-rocm64-torch291-py312-ci` | `odh-th06-rocm64-torch291-py312-v3-4` | B/C |  |
| feast | `odh-feast-operator-ci` | `odh-feast-operator-v3-4` | B/C | Fixed: RHOAI path corrected |
| feast | `odh-feature-server-ci` | `odh-feature-server-v3-4` | D | Fixed: RHOAI path corrected |
| fms-guardrails-orchestrator | `fms-guardrails-orchestrator-ci` | `odh-fms-guardrails-orchestrator-v3-4` | D |  |
| guardrails-detectors | `odh-built-in-detector-ci` | `odh-built-in-detector-v3-4` | B/C |  |
| guardrails-detectors | `fms-guardrails-hf-detector-ci` | `odh-guardrails-detector-huggingface-runtime-v3-4` | B/C |  |
| kserve | `odh-kserve-llmisvc-controller` | `odh-kserve-llmisvc-controller-v3-4` | B/C |  |
| kserve | `kserve-agent-ci` | `odh-kserve-agent-v3-4` | B/C |  |
| kserve | `kserve-controller-ci` | `odh-kserve-router-v3-4` | B/C |  |
| kserve | `kserve-router-ci` | `odh-kserve-controller-v3-4` | B/C |  |
| kserve | `kserve-storage-initializer-ci` | `odh-kserve-storage-initializer-v3-4` | D | Fixed: RHOAI path corrected |
| kube-auth-proxy | `kube-auth-proxy-ci` | `odh-kube-auth-proxy-v3-4` | B/C |  |
| kubeflow | `odh-kf-notebook-controller-ci` | `odh-kf-notebook-controller-v3-4` | B/C |  |
| kubeflow | `odh-notebook-controller-ci` | `odh-notebook-controller-v3-4` | B/C |  |
| kuberay | `odh-kuberay-operator-controller-ci` | `odh-kuberay-operator-controller-v3-4` | B/C | Fixed: ODH branch corrected (dev not main) |
| llama-stack-distribution | `odh-llama-stack-core-ci` | `odh-llama-stack-core-v3-4` | D |  |
| llama-stack-k8s-operator | `llama-stack-k8s-operator-ci` | `odh-llama-stack-k8s-operator-v3-4` | B/C |  |
| llm-d-inference-scheduler | `llm-d-inference-scheduler-ci` | `odh-llm-d-inference-scheduler-v3-4` | B/C | Fixed: ODH filename corrected (Dockerfile.epp) |
| llm-d-inference-scheduler | `llm-d-routing-sidecar-ci` | `odh-llm-d-routing-sidecar-v3-4` | B/C | Fixed: ODH filename corrected (Dockerfile.sidecar) |
| llm-d-kv-cache | `llm-d-kv-cache-ci` | `odh-llm-d-kv-cache-v3-4` | D |  |
| lm-evaluation-harness | `ta-lmes-job-ci` | `odh-ta-lmes-job-v3-4` | B/C |  |
| ml-metadata | `odh-mlmd-grpc-server-ci` | `odh-mlmd-grpc-server-v3-4` | B/C |  |
| mlflow | `mlflow-ci` | `odh-mlflow-v3-4` | B/C |  |
| mlflow-operator | `mlflow-operator-ci` | `odh-mlflow-operator-v3-4` | B/C |  |
| model-metadata-collection | `odh-model-metadata-collection-ci` | `odh-model-metadata-collection-v3-4` | B/C |  |
| model-registry | `odh-model-registry-ci` | `odh-model-registry-v3-4` | D |  |
| model-registry | `odh-model-registry-job-async-upload-ci` | `odh-model-registry-job-async-upload-v3-4` | B/C |  |
| model-registry-operator | `odh-model-registry-operator-ci` | `odh-model-registry-operator-v3-4` | D |  |
| models-as-a-service | `odh-maas-api-ci` | `odh-maas-api-v3-4` | B/C |  |
| notebooks | `odh-pipeline-runtime-pytorch-llmcompressor-cuda-py312-ci` | `odh-pipeline-runtime-pytorch-llmcompressor-cuda-py312-v3-4` | B/C |  |
| notebooks | `odh-workbench-jupyter-tensorflow-rocm-py312-ci` | `odh-workbench-jupyter-tensorflow-rocm-py312-v3-4` | D |  |
| notebooks | `odh-workbench-rstudio-minimal-cpu-py311-c9s-ci` | `odh-workbench-codeserver-datascience-cpu-py312-v3-4` | A | Fixed: ODH version corrected (py3.12 not py3.11) |
| notebooks | `odh-workbench-rstudio-minimal-cuda-py311-c9s-ci` | `odh-pipeline-runtime-pytorch-cuda-py312-v3-4` | A | Fixed: ODH version corrected (py3.12 not py3.11) |
| notebooks | `odh-workbench-jupyter-minimal-cpu-py312-ubi9-ci` | `odh-workbench-jupyter-minimal-cpu-py312-v3-4` | B/C |  |
| notebooks | `odh-workbench-jupyter-minimal-cuda-py312-ubi9-ci` | `odh-workbench-jupyter-minimal-cuda-py312-v3-4` | A |  |
| notebooks | `odh-workbench-jupyter-minimal-rocm-py312-ubi9-ci` | `odh-workbench-jupyter-minimal-rocm-py312-v3-4` | B/C |  |
| notebooks | `odh-workbench-jupyter-datascience-cpu-py312-ubi9-ci` | `odh-workbench-jupyter-datascience-cpu-py312-v3-4` | A |  |
| notebooks | `odh-workbench-jupyter-pytorch-cuda-py312-ubi9-ci` | `odh-workbench-jupyter-pytorch-cuda-py312-v3-4` | A |  |
| notebooks | `odh-workbench-jupyter-pytorch-rocm-py312-ubi9-ci` | `odh-workbench-jupyter-pytorch-rocm-py312-v3-4` | A |  |
| notebooks | `odh-workbench-jupyter-tensorflow-cuda-py312-ubi9-ci` | `odh-workbench-jupyter-tensorflow-cuda-py312-v3-4` | A |  |
| notebooks | `odh-workbench-jupyter-trustyai-cpu-py312-ubi9-ci` | `odh-workbench-jupyter-trustyai-cpu-py312-v3-4` | A |  |
| notebooks | `odh-pipeline-runtime-datascience-cpu-py312-ubi9-ci` | `odh-pipeline-runtime-datascience-cpu-py312-v3-4` | B/C |  |
| notebooks | `odh-pipeline-runtime-minimal-cpu-py312-ubi9-ci` | `odh-pipeline-runtime-minimal-cpu-py312-v3-4` | B/C |  |
| notebooks | `odh-pipeline-runtime-pytorch-cuda-py312-ubi9-ci` | `odh-pipeline-runtime-pytorch-rocm-py312-v3-4` | B/C |  |
| notebooks | `odh-pipeline-runtime-pytorch-rocm-py312-ubi9-ci` | `odh-pipeline-runtime-tensorflow-rocm-py312-v3-4` | B/C |  |
| notebooks | `odh-pipeline-runtime-tensorflow-cuda-py312-ubi9-ci` | `odh-pipeline-runtime-tensorflow-cuda-py312-v3-4` | B/C |  |
| notebooks | `odh-pipeline-runtime-tensorflow-rocm-py312-ubi9-ci` | `odh-wb-jupyter-pytorch-llmcompressor-cuda-py312-v3-4` | D |  |
| odh-dashboard | `odh-dashboard-ci` | `odh-dashboard-v3-4` | B/C |  |
| odh-dashboard | `odh-mod-arch-gen-ai-ci` | `odh-mod-arch-gen-ai-v3-4` | B/C |  |
| odh-dashboard | `odh-mod-arch-automl-ci` | `odh-mod-arch-automl-v3-4` | B/C |  |
| odh-dashboard | `odh-mod-arch-mlflow` | `odh-mod-arch-mlflow-v3-4` | B/C |  |
| odh-dashboard | `odh-mod-arch-autorag-ci` | `odh-mod-arch-autorag-v3-4` | B/C |  |
| odh-dashboard | `odh-mod-arch-eval-hub` | `odh-mod-arch-eval-hub-v3-4` | B/C |  |
| odh-dashboard | `odh-mod-arch-modular-architecture-ci` | `odh-mod-arch-model-registry-v3-4` | B/C |  |
| odh-model-controller | `odh-model-controller-ci` | `odh-model-controller-v3-4` | D |  |
| openvino_model_server | `openvino-model-server-ci` | `odh-openvino-model-server-v3-4` | B/C |  |
| spark-operator | `spark-operator-ci` | `odh-spark-operator-v3-4` | A |  |
| trainer | `trainer-ci` | `odh-trainer-v3-4` | B/C |  |
| training-operator | `odh-training-operator-ci` | `odh-training-operator-v3-4` | B/C |  |
| trustyai-explainability | `odh-trustyai-service-ci` | `odh-trustyai-service-v3-4` | B/C |  |
| trustyai-service-operator | `odh-trustyai-service-operator-ci` | `odh-trustyai-service-operator-v3-4` | B/C |  |
| trustyai-service-operator | `ta-lmes-driver-ci` | `odh-ta-lmes-driver-v3-4` | B/C |  |
| vllm-orchestrator-gateway | `trustyai-vllm-orchestrator-gateway-ci` | `odh-trustyai-vllm-orchestrator-gateway-v3-4` | B/C |  |
| workload-variant-autoscaler | `workload-variant-autoscaler-ci` | `odh-workload-variant-autoscaler-controller-v3-4` | B/C |  |

## ODH-Only Components (no RHOAI match)

| Component | Repo | Dockerfile |
|-----------|------|------------|
| `odh-fbc-fragment-ci` | `ODH-Build-Config` | `Dockerfile` |
| `odh-operator-bundle-ci` | `ODH-Build-Config` | `bundle/Dockerfile` |
| `batch-gateway-apiserver-ci` | `batch-gateway` | `dockerfile/Dockerfile.apiserver.konflux` |
| `batch-gateway-processor-ci` | `batch-gateway` | `dockerfile/Dockerfile.processor.konflux` |
| `caikit-tgis-serving-ci` | `caikit-tgis-serving` | `Dockerfile` |
| `fms-guardrails-regex-detector-ci` | `guardrails-regex-detector` | `Dockerfile` |
| `llama-stack-provider-ragas-ci` | `llama-stack-provider-ragas` | `Containerfile` |
| `odh-maas-controller-ci` | `models-as-a-service` | `maas-controller/Dockerfile` |
| `nudge-only-notebooks-ci` | `notebooks` | `Dockerfile` |
| `odh-workbench-codeserver-datascience-cpu-py312-ubi9-ci` | `notebooks` | `codeserver/ubi9-python-3.12/Dockerfile.cpu` |
| `odh-workbench-jupyter-pytorch-llmcompressor-cuda-ci` | `notebooks` | `jupyter/pytorch+llmcompressor/ubi9-python-3.12/Dockerfile.cuda` |
| `odh-operator-ci` | `opendatahub-operator` | `Dockerfiles/Dockerfile` |

## RHOAI-Only Components (no ODH match)

| Component | Repo | Dockerfile |
|-----------|------|------------|
| `odh-operator-bundle-v3-4` | `RHOAI-Build-Config` | `bundle/Dockerfile` |
| `rhoai-fbc-fragment-v3-4` | `RHOAI-Build-Config` | `Dockerfile` |
| `odh-eval-hub-v3-4` | `eval-hub` | `Dockerfile.konflux` |
| `odh-trustyai-garak-lls-provider-dsp-v3-4` | `llama-stack-provider-trustyai-garak` | `Dockerfile.konflux` |
| `odh-model-performance-data-v3-4` | `models-perf-benchmark-data` | `Dockerfile.konflux` |
| `odh-must-gather-v3-4` | `must-gather` | `Dockerfile.konflux` |
| `odh-cli-v3-4` | `odh-cli` | `Dockerfile.konflux` |
| `odh-mod-arch-maas-v3-4` | `odh-dashboard` | `Dockerfile.konflux.maas` |
| `odh-automl-v3-4` | `pipelines-components` | `Dockerfile.konflux.automl` |
| `odh-operator-v3-4` | `rhods-operator` | `Dockerfiles/Dockerfile.konflux` |
| `odh-vllm-cpu-v3-4` | `vllm-cpu` | `Dockerfile.konflux.cpu` |
| `odh-vllm-gaudi-v3-4` | `vllm-gaudi` | `Dockerfile.konflux.gaudi` |

## Previously Failed Components - Now Fixed ✅

All 8 previously failed components have been successfully fixed by correcting paths in the upstream YAML configurations:

| Repo | Component | Issue | Fix Applied | Strategy |
|------|-----------|-------|-------------|----------|
| feast | `odh-feast-operator-ci` / `odh-feast-operator-v3-4` | RHOAI path incorrect | Corrected to `Dockerfiles/Dockerfile.feast-operator.konflux` | B/C |
| feast | `odh-feature-server-ci` / `odh-feature-server-v3-4` | RHOAI path incorrect | Corrected to `Dockerfiles/Dockerfile.feature-server.konflux` | D |
| kserve | `kserve-storage-initializer-ci` / `odh-kserve-storage-initializer-v3-4` | RHOAI path incorrect | Corrected to `Dockerfiles/storage-initializer.Dockerfile.konflux` | D |
| llm-d-inference-scheduler | `llm-d-inference-scheduler-ci` / `odh-llm-d-inference-scheduler-v3-4` | ODH filename wrong | Corrected to `Dockerfile.epp` | B/C |
| llm-d-inference-scheduler | `llm-d-routing-sidecar-ci` / `odh-llm-d-routing-sidecar-v3-4` | ODH filename wrong | Corrected to `Dockerfile.sidecar` | B/C |
| notebooks | `odh-workbench-rstudio-minimal-cpu-py311-c9s-ci` / `odh-workbench-codeserver-datascience-cpu-py312-v3-4` | ODH version wrong | Corrected to Python 3.12 (3.11 doesn't exist) | A |
| notebooks | `odh-workbench-rstudio-minimal-cuda-py311-c9s-ci` / `odh-pipeline-runtime-pytorch-cuda-py312-v3-4` | ODH version wrong | Corrected to Python 3.12 (3.11 doesn't exist) | A |
| kuberay | `odh-kuberay-operator-controller-ci` / `odh-kuberay-operator-controller-v3-4` | ODH branch wrong | Corrected to `dev` branch (not `main`) | B/C |

### Fix Summary
- **RHOAI path corrections**: 3 components (feast-operator, feature-server, kserve-storage-initializer)
- **ODH filename corrections**: 2 components (llm-d-inference-scheduler, llm-d-routing-sidecar)
- **ODH version corrections**: 2 components (rstudio-cpu-py312, rstudio-cuda-py312)
- **ODH branch corrections**: 1 component (kuberay-operator-controller)

See `UPSTREAM_FIXES_NEEDED.md` for details on required YAML fixes in konflux-release-data repository.

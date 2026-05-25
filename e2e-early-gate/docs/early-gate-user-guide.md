# Early Gate Testing — User Guide

Early gate testing is a pre-merge smoke testing infrastructure for ODH. It validates that a pull request does not break core functionality by building a complete set of OLM artifacts (operator, bundle, and FBC catalog) using the PR's latest images and running smoke tests against them — all before the PR is merged.

---

## 1. How It Works

When you open a pull request on an onboarded component or operator repository, the early gate infrastructure runs a three-stage pipeline chain:

```mermaid
flowchart TD
    subgraph STAGE1["Stage 1: PR Build"]
        direction TB
        PR1["PR is opened or updated"]:::start --> PR2["Konflux builds the component <br /> image from the PR source"]:::build
        PR2 --> PR3["Image is pushed to Quay <br /> tagged with the PR identifier"]:::build
        PR3 --> PR4["All PR builds succeed"]:::build
    end

    subgraph STAGE2["Stage 2: Early Gate Build"]
        direction TB
        EG1["Fetch latest PR image for <br /> the triggering component"]:::egbuild --> EG2["Use stable images for <br /> all other components"]:::egbuild
        EG2 --> EG3["Build operator container"]:::egbuild
        EG3 --> EG4["Build OLM bundle"]:::egbuild
        EG4 --> EG5["Build FBC catalog"]:::egbuild
    end

    subgraph STAGE3["Stage 3: Early Gate Test"]
        direction TB
        ET1["Verify catalog and bundle <br /> images exist"]:::egtest --> ET2["Trigger Jenkins <br /> smoke test job"]:::egtest
        ET2 --> ET3["Monitor job until <br /> completion"]:::egtest
        ET3 --> ET4["Post test results <br /> as PR comment"]:::egtest
    end

    STAGE1 -->|"auto-trigger"| STAGE2
    STAGE2 -->|"auto-trigger"| STAGE3

    classDef start fill:#e0e0e0,stroke:#757575,color:#000
    classDef build fill:#bbdefb,stroke:#1976d2,color:#000
    classDef egbuild fill:#c8e6c9,stroke:#388e3c,color:#000
    classDef egtest fill:#b2dfdb,stroke:#00796b,color:#000
```

**For component PRs** (e.g., feast, model-mesh, kserve): the build pipeline uses the PR's component image while keeping all other components at their latest stable versions.

**For operator PRs**: the build pipeline builds the operator directly from the PR's source code.

---

## 2. Triggering Early Gate Tests

### Automatic Triggers

Early gate pipelines are triggered automatically:

1. When all PR build pipelines succeed on a PR, the **early gate build pipeline** is triggered automatically.
2. When the early gate build pipeline completes successfully, the **early gate test pipeline** is triggered automatically.

No manual action is needed for the standard flow.

### Manual Triggers (PR Comments)

You can manually trigger each stage by commenting on the PR:

| Command | What It Does |
|---------|--------------|
| `/early-gate-build` | Triggers the early gate build pipeline (operator + bundle + FBC) |
| `/early-gate-test` | Triggers the early gate test pipeline (smoke tests) |

These commands are useful when:
- You want to re-run tests after a transient failure
- You want to trigger tests without waiting for all PR builds to complete
- A previous run was interrupted

---

## 3. What Each Stage Does

### Stage 1: PR Build

The standard Konflux pull request build pipeline. It compiles and builds a container image from the PR source code, pushes it to Quay with a PR-specific tag, and runs basic checks. This is the same build pipeline that runs for all PRs — nothing early-gate-specific happens here.

### Stage 2: Early Gate Build Pipeline

Builds a complete set of OLM artifacts using the PR's latest images:

1. **Operator image** — built from source (operator PRs) or fetched from the PR's existing image (component PRs)
2. **OLM Bundle** — operator bundle containing the CSV and CRDs, patched with the PR's component images
3. **FBC Catalog** — a File-Based Catalog fragment for the target OpenShift version

All three images are pushed to Quay and tagged with the PR identifier.

There are two variants of this pipeline:
- `early-gate-component-pipeline` — triggered by component PRs
- `early-gate-operator-pipeline` — triggered by operator PRs

Both follow the same structure; the difference is which repository triggers them.

### Stage 3: Early Gate Test Pipeline

Orchestrates smoke testing through Jenkins:

1. **Verify prerequisites** — confirms the catalog and bundle images exist on Quay
2. **Trigger Jenkins job** — dispatches a GitHub Actions workflow that starts a Jenkins smoke test
3. **Monitor to completion** — polls the Jenkins job status until it finishes
4. **Post results** — fetches the test summary and posts a completion comment on the PR

The test pipeline is **idempotent** — if it is interrupted and re-run, it detects the in-progress Jenkins job from the previous run and resumes monitoring it instead of triggering a duplicate.

---

## 4. PR Comments and Status Updates

The bot posts comments on your PR to keep you informed of the testing progress.

### During Testing

As the test progresses, the bot posts status comments showing the current phase (queued, running). These intermediate comments are automatically cleaned up once the next phase begins.

### Completion Comment

When testing finishes, a permanent completion comment is posted with the test results:

**All tests passed:**

> :white_check_mark: **Early Gate Test - Complete**
>
> | Field | Value |
> |-------|-------|
> | **Job URL** | /job/devops/job/early-gate-tests/42/ |
> | **Status** | :white_check_mark: SUCCESS |
> | **FBC Tag** | odh-pr-73-feast |
>
> **Test Summary**
>
> | Passed | Failed | Skipped | Total |
> |--------|--------|---------|-------|
> | 15 | 0 | 2 | 17 |

**Tests failed:**

> :x: **Early Gate Test - Complete**
>
> | Field | Value |
> |-------|-------|
> | **Job URL** | /job/devops/job/early-gate-tests/42/ |
> | **Status** | :x: FAILED - 3 test(s) failed |
>
> **Test Summary**
>
> | Passed | Failed | Skipped | Total |
> |--------|--------|---------|-------|
> | 12 | **3** | 2 | 17 |

### Comment Lifecycle

```mermaid
stateDiagram-v2
    [*] --> Queued : Build pipeline triggers test

    state "Job Queued" as Queued
    note right of Queued
        Bot posts a comment indicating
        the Jenkins job is queued
    end note

    Queued --> Running : Jenkins job starts

    state "Job Running" as Running
    note right of Running
        Bot replaces the queued comment
        with a running status comment
    end note

    Running --> Complete : Job finishes

    state "Results Posted" as Complete
    note right of Complete
        Bot posts the final completion
        comment with test summary
    end note

    Complete --> [*]

    classDef queued fill:#fff9c4,stroke:#f9a825,color:#000
    classDef running fill:#bbdefb,stroke:#1976d2,color:#000
    classDef complete fill:#c8e6c9,stroke:#388e3c,color:#000

    class Queued queued
    class Running running
    class Complete complete
```

---

## 5. Re-running Tests

| Scenario | What to Do |
|----------|------------|
| Tests failed due to a real issue | Push a fix to the PR — the entire flow restarts automatically |
| Tests failed due to a transient/infra issue | Comment `/early-gate-test` to re-run just the test stage |
| Build failed or needs to be re-triggered | Comment `/early-gate-build` to re-run the build + test stages |
| Pipeline was interrupted mid-run | Simply re-trigger — the test pipeline detects the existing Jenkins job and resumes monitoring it |

Re-running is always safe. The test pipeline will not trigger duplicate Jenkins jobs.

---

## 6. How Tests Run on Your PR

When the early gate test pipeline triggers a Jenkins job, the following stages execute:

```mermaid
flowchart LR
    A["Provision <br /> ROSA HCP <br /> cluster"]:::cluster --> B["Deploy RHOAI <br /> operator from <br /> FBC image"]:::deploy
    B --> C["Run component <br /> smoke tests"]:::test
    C --> D["Collect results <br /> and clean up"]:::results

    classDef cluster fill:#bbdefb,stroke:#1976d2,color:#000
    classDef deploy fill:#c8e6c9,stroke:#388e3c,color:#000
    classDef test fill:#fff9c4,stroke:#f9a825,color:#000
    classDef results fill:#e1bee7,stroke:#7b1fa2,color:#000
```

### Cluster

A fresh **ROSA HCP** cluster is provisioned on AWS for each test run.

| Property | Value |
|----------|-------|
| **Platform** | ROSA HCP (AWS, us-west-2) |
| **OpenShift version** | 4.20-latest (configurable) |
| **Lifetime** | Deleted immediately after tests (default) |

The cluster is a dedicated, isolated environment — no test run shares a cluster with another.

### RHOAI Deployment

The RHOAI operator is deployed from the **FBC catalog image built in Stage 2** (the early gate build pipeline). This image is installed using the **`odh-stable`** subscription channel, ensuring the PR's component images are what gets tested.

The deployment flow:
1. The FBC image tag (e.g., `odh-pr-73-feast`) is resolved to a full Quay URI via the [Tracer](https://github.com/red-hat-data-services/rhods-devops-infra) tool
2. A `CatalogSource` is created pointing to this FBC image
3. The RHOAI operator is installed via CLI using the `odh-stable` channel
4. An identity provider and external DNS are configured
5. Cluster and operator health checks verify everything is ready

### Smoke Tests

The Jenkins job determines which tests to run based on the component's configuration:

- **Component mapping:** your repository's Konflux component key (from [`component_repo_map.json`](https://github.com/opendatahub-io/odh-konflux-central/blob/main/config/component_repo_map.json)) is mapped to a test configuration that defines which smoke tests to execute.
- **Quality gate:** the `early-gate` quality gate is used, which typically maps to smoke-level tests (e.g., `-m smoke` for pytest components, or `FeatureStoreANDSmoke` for Robot Framework components).
- **Test runners:** depending on your component's configuration, tests run either via **Robot Framework** (ods-ci) or as **containerized pytest/gotestsum jobs** (shift-left). The runner is determined by the `metadata.earlyGateTestRunner` field in your component's config — `ods-ci` for Robot, `shiftleft` (the default) for containers.

### Must-Gather

Must-gather diagnostic collection runs automatically for components that have `--collect-must-gather` in their test configuration. This collects OpenShift cluster diagnostics when tests fail, which helps with debugging.

If your component uses the `opendatahub-tests` shared framework (shift-left runner), you can enable must-gather by adding `--collect-must-gather` to your component's `image.args` in its configuration file:

```yaml
# In your component's main.yaml
# e.g. resources/configs/components-testing/components/<your-component>/main.yaml
merge:
  image:
    args: [
        --collect-must-gather,
        -o junit_suite_name=<your-component>,
        tests/<your-test-path>/
    ]
```

---

## 7. Limitations

- **ODH repos only** — early gate testing currently supports only ODH repository builds. RHDS and RHOAI builds are not supported yet.
- **Single architecture only** — early gate testing currently supports x86 architecture only.
- **Repo-scoped testing** — each early gate run tests a single PR from a single repository. Testing PRs from multiple repositories together (group testing) is planned for a future phase.

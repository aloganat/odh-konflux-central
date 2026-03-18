# E2E Early-Gate

Single Tekton pipeline that sequentially builds **operator -> bundle -> FBC-fragment** for quick feature-branch validation before pushing to stable.

- **[E2E-EARLY-GATE-PLAN.md](./E2E-EARLY-GATE-PLAN.md)** -- fully executable plan (Sections 1-10).

## Artifacts

| File | Description |
|------|-------------|
| `early-gate-e2e-pipeline.yaml` | E2E Tekton Pipeline (17 tasks in 3 blocks) |
| `early-gate-e2e-pipelinerun.yaml` | PipelineRun for triggering from PR events |
| `tasks/bundle-processor.yaml` | Tekton Task replacing the bundle-processor GitHub workflow |
| `tasks/fbc-processor.yaml` | Tekton Task replacing the fbc-processor GitHub workflow |
| `repos/ODH-Build-Config/.github/workflows/` | Reference copies of GitHub workflows with early-gate guards |

# kuberay-operator-controller - Fixed

## Status
✓ Fixed - ODH YAML uses wrong branch (main instead of dev)

## Issue
- YAML specified revision: `main`
- Actual default branch: `dev`
- Dockerfile.rhoai exists on `dev` branch

## Files
- `Dockerfile.ODH` - from opendatahub-io/kuberay dev branch
- `Dockerfile.RHOAI` - from red-hat-data-services/kuberay rhoai-3.4 branch
- `Dockerfile.Konflux` - Merged version

## Upstream Fix Needed
Update ODH YAML to use `revision: dev` instead of `revision: main`

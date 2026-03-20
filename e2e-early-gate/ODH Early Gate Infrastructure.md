# ODH Early Gate Infrastructure

## Brief Design

1. A custom pipeline triggered only on creating a specific tag  
   1. We can keep the events configurable through on-cel expression and let the teams change it as they need  
   2. On tag creation, on-push?, on pull?  
2. Build the component with image tag as git tag name  
3. Trigger an ITS using /feature-build  
   1. ITS pipeline will execute operator build only if the component itself is not odh-operator  
4. ITS pipeline will take a parameter of current component name and image URI  
5. Operator processor task will ensure to take everything from stable, but this one component image will be taken from the parameter  
6. Pull the latest bundle manifests and CSV from OBC repo  
7. Replace all the images based on the current operands map from the previous steps  
8. Build the bundle using a buildah task  
9. Translate FBC processor to prepare catalog.yaml using the latest bundle image  
10. Build the FBC using buildah task  
11. Keep all the image tags same as current git tag

* Take a yaml file as an input, which will contains (tags?) of the images which need to be different than odh-stable, (all the images with code-changes, like current component and operator)

How to trigger the early gates

* Single PRs  
  * Use group testing infra  
  * Let people trigger it manually by commenting /early-gate  
  * If a team wants to execute it on each PR mandatorily  
    * Enable-early-gate \= true, in PLR  
    * Use group-testing infra to automatically comment /early-gate on the PR  
* Group PRs  
  * Use a group snapshot? No, we can’t avoid its frequent execution on unrelated PRs, like for main  
  * Ask teams to upload a file with name “group-definition.yaml” as an attachment by adding a new comment on the PR

```json
group_map:
 component_images:
   - name: feast-operator-ci
     image_repo: quay.io/opendatahub/feast-operator:odh-pr-73
   - name: feature-server-ci
     image_repo: quay.io/opendatahub/feature-server:odh-pr-73

```

  *   
    *   
* Test customization  
  * How do you customize what tests will be executed for each feature build  
* Template  
  * Should we provide a feature build template rather than the build pipeline  
  * Let teams add what tests they want to 
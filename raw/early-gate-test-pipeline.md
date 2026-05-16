# early-gate-test-pipeline

## Objective

* Write a fully atomic and parameterized “early-gate-test-pipeline” tekton pipeline with mentioned tasks and steps  
* Goal of this pipeline is to trigger an early-gate test automation jenkins job, monitor it and reflect the pipeline status based on the job status

## Overall

* All the labels and annotation should be same  
* Analyze the “e2e-early-gate/early-gate-component-pipeline.yaml” thoroughly to understand the tekton theme, all the possible patterns and available capabilities which which we can use to implement this pipeline  
* We will use the mentioned github workflows to trigger and monitor the jenkins job rather than directly interacting with it   
* Each type of comment we are making on the PR should have some fixed format and marker, so that it is easy to find the comment later  
* Make sure to create reusable tekton tasks wherever possible rather than writing all the code in pipeline itself, store the tasks under “e2e-early-gate/tasks”   
* You should keep separate configurable github token for various github operations like interacting with github workflow, commenting on the PR and downloading the github file  stored in a kubernetes secret for all the github operations wherever needed, make sure to make it configurable  
* We need to make this pipeline idempotent means, if there is jenkins job triggered in previous execution and pipeline got terminated for some reason, then we should pickup the same job rather than triggering new one  
* Jenkins host to be used everywhere is jenkins-csb-rhods-opendatascience.dno.corp.redhat.com

## Tasks

* It should have following tasks  
  * Check prerequisites task  
    * It should first check if following 2 quay images exist  
      * quay.io/opendatahub/opendatahub-operator-catalog:odh-pr-\<PR_NUMBER\>-\<REPO_NAME\>  
      * quay.io/opendatahub/opendatahub-operator-bundle:odh-pr-\<PR_NUMBER\>-\<REPO_NAME\>  
    * See the reference pipeline on how to get PR_NUMBER and REPO_NAME  
    * You can use skopeo to check the existence of quay images  
    * If prerequisites not met then exit the pipeline  
  * Check for any ongoing jobs for current PR \- task  
    * Analyze the comments on the PRs made by the current user in descending order to see:  
      * If there is a “**queue-url-comment**” which doesn’t have any “**job-url-comment**” or “**job-completion-comment**” after it  
        * If yes then extract the queue-url from the comment, most probably previous pipeline got terminated in-between for some reason, we should skip the “Trigger test pipeline” task and start from “Monitor the jenkins job” task using the extracted queue-url  
      * If there is a “**job-url-comment**” which doesn’t have any “**job-completion-comment**” after it  
        * If yes then extract the jenkin job-url from the comment, most probably previous pipeline got terminated in-between for some reason, we should skip the “Trigger test pipeline” task and start from “Monitor the jenkins job” task using the extracted job-url  
  * Trigger test pipeline task  
    * This should trigger the test pipeline using a github workflow \- https://github.com/red-hat-data-services/rhods-devops-infra/actions/workflows/dummy-earlygate-smoke-trigger.yaml  
    * Inputs for triggering the workflow:  
      * repositories \== \<REPO_NAME\>  
      * fbc_tag \== odh-pr-\<PR_NUMBER\>-\<REPO_NAME\>  
      * pr_number \== \<PR_NUMBER\>  
      * correlation_id \== eg-\<current-unix-datetime-stamp\>  
    * Monitor the triggered workflow:  
      * Once the workflow execution is complete, try to read the workflow job output with name “queue-url” to find out the queue-url for the jenkins job scheduled to be triggered  
      * If the workflow job fails try to parse the queue-url from the output of the “trigger-jenkins” step, it should be of the format \- “https://jenkins-csb-rhods-opendatascience.dno.corp.redhat.com/queue/item/\<numeric-item-id”  
      * If queue-url is not found either from job output or the step log, then throw the proper error and exit the pipeline  
      * “**queue-url-comment**” \- If the queue-url is found, then add a comment on the current PR mentioning the queue-url and a message that job is queued, it will be triggered shortly.  
      * Make sure to have a fixed format and some marker for the comment, so that it is easy to find it later when needed  
  * Monitor jenkins job task  
    * Use following github workflow to monitor the jenkins job  
      * https://github.com/red-hat-data-services/rhods-devops-infra/actions/workflows/monitor-jenkins-job.yaml
    * It takes following parameters  
      * queue-url \- jenkin job queue url  
      * job-url \- jenkins job url  
    * At a time only one input needs to be passed not both  
    * The job also has following outputs declared  
      * jenkins-job-url  
      * jenkins-job-status  
    * Keep invoking this workflow every 30s, if the workflow fails once then keep trying every 30s, only exit the pipeline if continuous 10 executions fail  
    * First Get the jenkins job url  
      * Based on the queue-url found in the previous step invoke the monitor-jenkins-job with the queue-url  
      * Once the workflow is complete try to read its jenkins-job-url output to check if we get the jenkins job url of the triggered job  
      * “**job-url-comment**” \- If we get the jenkins job url, then add a comment on the current PR mentioning the jenkins-job-url and a message that job is triggered  
      * Make sure to have a fixed format and some marker for the comment, so that it is easy to find it later when needed  
      * Also delete the previous “**queue-url-comment**” comment on the PR containing the queue-url, which we posted in the previous task, make sure to delete no other comment, only this one comment should be deleted if found, decide to delete it only if it contains the correct queue-url, do proper validation using the format and marker we are adopting for all the comments, iterate the comments in descending order, only process the comments made by the current user, if there is an error deleting the comment then ignore it and move ahead  
    * Get the job status  
      * Once the jenkins job url is obtained, then invoke the workflow with job-url input (don’t pass queue-url)  
      * Once the workflow is complete try to read its jenkins-job-status output to check the current status of the jenkins job  
    * Get the job results  
      * Once the job is completed, successfully or failed based on its status, try to get the summary results from github  
      * Try to download raw content of following file from github https://github.com/opendatahub-io/odh-build-metadata/blob/early-gate/\<REPO_NAME\>/\<PR_NUMBER\>/early-gate-test-summary.yaml  
        * This requires not github token since repo is public  
      * If the download failed for some reason then keep trying max 5 times with a gap of 30s  
      * early-gate-test-summary.yaml will have following yaml structure:  
        * job_url \- relative jenkins job url without the base-server  
        * fbc_tag : \<fbc_tag passed to workflow as an input in “Trigger test pipeline” task\>  
        * correlation_id : \<correlation_id passed to workflow as an input in “Trigger test pipeline” task\>  
        * test_summary.Failed \- number of failed tests  
        * test_summary.Passed \- number of Passed tests  
        * test_summary.Skipped \- number of Skipped tests  
        * test_summary.Total \- number of Total tests  
      * Verify the job_url and fbc_tag to ensure we are reading the results for correct job, if the values of  job_url and fbc_tag don’t match then keep trying max 5 times with a gap of 30s  
      * Optionally verify correlation_id id as but don’t conclude anything if it doesn’t match, just throw a warning  
      * “**job-completion-comment**” \- Once all the validation is successful, post a summary comment on the current PR mentioning the Job url, job status, FBC tag and the summary of test counts for each status  
        * If correct early-gate-test-summary.yaml is not found, then also the summary comment needs to be posted in similar format with the jenkins job url and status along with a warning that job results could not be obtained from the github file at expected location.  
      * Make sure to have a fixed format and some marker for the comment, so that it is easy to find it later when needed  
      * Also delete the previous “**job-url-comment**” comment on the PR containing the jenkins-job-url, which we posted in the previous step, make sure to delete no other comment, only this one comment should be deleted if found, decide to delete it only if it contains the correct jenkins-job-url, do proper validation using the format and marker we are adopting for all the comments, iterate the comments in descending order, only process the comments made by the current user, if there is an error deleting the comment then ignore it and move ahead  
      * Stop invoking the workflow now  
      * If the jenkins job final status is failed or Failed count is more than zero, then the pipeline needs to be marked as failed at the end and need to exit 1  
      * If the correct early-gate-test-summary.yaml is not found, but jenkins job status is failed, then the pipeline needs to be marked as failed at the end and exit 1, and   
      * If the correct early-gate-test-summary.yaml is not found, but jenkins job status is success, then the pipeline needs to be marked as success at the end
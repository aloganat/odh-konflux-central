use kubearchive for getting logs of Konflux pipelinerun or taskrun
these custom resorces are also denoted with pr or tr respectively
logs can be obtained using 

oc ka logs pr/<pipelinerun-name>
oc ka logs tr/<taskrun-name>

taskrun names for a given pipelinerun can be found by scanning the output of command "oc ka get pr <pipelinerun-name> -o yaml"
taskrun name format would be of <pipelinerun-name>-<task-name>
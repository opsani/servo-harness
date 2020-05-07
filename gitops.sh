#!/bin/bash 
set -e

### VARIABLES
CPU=$1 
MEMORY=$2 
APP_NAME=$3
REPO_NAME="co-http-harness"
REPO_URL="git@github.com:benburdick/co-http-harness.git"

# YAML files to be modified (space separated)
TRIGGERS="opsani_promote_trigger.yaml optimization_update.yaml canary_update.yaml ancestry_on_new_artifact.yaml"


clone(){
	git clone $REPO_URL
}

cleanup(){
    rm -rf /tmp/$REPO_NAME
}

fn_commit(){
    echo "INFO: Adding files to Github commit"
    git add .
    echo "Generating the commit"
    git commit -m "harness.io script commiting cloud provider changes"
    echo "Pushing code to github"
    git push origin master
}

fn_nav_trigger(){
	cd /tmp/$REPO_NAME/Setup/Applications/$APP_NAME/Triggers
}

#Edit the CPU Value
fn_mainpulate_cpu(){
    for trigger in $TRIGGERS; do
        namesArr=$(yq r $trigger 'workflowVariables[*].name' | xargs)
        names=($(echo ${namesArr//- /}))
        for i in "${!names[@]}"; do 
            if [[ ${names[$i]} == "cpu" ]]; then
                yq w $trigger "workflowVariables[$i].value" $CPU --inplace 
            fi
        done
    done
}

#Edit the Memory Value
fn_mainpulate_memory(){
    for trigger in $TRIGGERS; do
        namesArr=$(yq r $trigger 'workflowVariables[*].name' | xargs)
        names=($(echo ${namesArr//- /}))
        for i in "${!names[@]}"; do 
            if [[ ${names[$i]} == "mem" ]]; then
                yq w $trigger "workflowVariables[$i].value" $MEMORY --inplace 
            fi
        done
    done
}

### MAIN
if [ $# -lt 3 ]; then
    echo "ERROR: Not enough arguments"
    echo "Usage: ./main.sh <cpuVal> <memVal> <APP_NAME>"
    exit 0
else
    echo "Git Clone $REPO_URL"
    clone
fi

if [ -d "$REPO_NAME/Setup" ]; then 
    CPU=$1
    MEM=$2
    APP_NAME=$3
	
	echo "INFO: Navigating to Trigger YML"
    fn_nav_trigger
	
	echo "Manipulating the cpu"
	fn_mainpulate_cpu
	
	echo "Manipulating Memory"
	fn_mainpulate_memory
	
	echo "Commiting to GitHub"
	fn_commit
	
    echo "Cleaning Up"
    cleanup
else 
  echo "ERROR: No Setup Directory Found"
fi

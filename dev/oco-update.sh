#!/bin/bash 
set -e

APP='harness-dev'
ACCOUNT='dev.opsani.com'
TOKEN='${secrets.getValue("CO_TOKEN")}'

URL='https://api.opsani.com/accounts/$ACCOUNT/applications/$APP/config/'

CPU='${workflow.variables.cpu}'
MEM='${workflow.variables.mem}'

curl -X PUT \
    -H 'Content-type: application/merge-patch+json' \
    -H 'Authorization: Bearer '${TOKEN}'' \
    'https://api.optune.ai/accounts/'${ACCOUNT}'/applications/'${APP}'/config?reset=false&patch=true' \
    -d '{"adjustment": {"control": {"userdata": {"${workflow.variables.name}": {"cpu": "'$CPU'", "mem": "'$MEM'"}}}}}'

#!/bin/bash 
set -e

OPSANI_APP='golden-opsani-v1'
OPSANI_ACCOUNT='ancestry.com'
OPSANI_TOKEN='c25609faf7257b2af7caa2e746cf16b7689228dd12b86b013554be'

curl -X PUT \#    -H 'Content-type: application/json' \
    -H 'Authorization: Bearer '${OPSANI_TOKEN}'' \
    'https://api.opsani.com/accounts/'${OPSANI_ACCOUNT}'/applications/'${OPSANI_APP}'/config?reset=false&patch=true' \
    -d '{"adjustment": {"control": {"userdata": {"${workflow.variables.name}": {"cpu": ${workflow.variables.cpu}, "mem": ${workflow.variables.mem}}}}}}'

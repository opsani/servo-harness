# Opsani Servo adjust plugin for Harness.io

Trigger and watch a workflow in Harness.io as a method of adjusting workflow parameters

Supported parameters workflow parameters:

    "infraDef": "opsani-servo",  # workflow.variables.InfraDefinition_KUBERNETES
    "mem": "256Mi",  # ${workflow.variables.mem}
    "cpu": "500m",  # ${workflow.variables.cpu}
    "adjust": "True",  # ${workflow.variables.adjust}
    "name": "canary",  # ${workflow.variables.name}
    "buildNo": "200",  # ${artifact.buildNo}
    "service": "web-canary-deployment",  # ${service.name}

Static config parameters:

    "token": ""
    "accountId": ""
    "application": ""
    "apiKey": ""

Create a trigger in Harness for a Workflow
Capture the parameters above from the proposed CURL command
Add to config.yaml

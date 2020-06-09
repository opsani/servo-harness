import requests
import json
import yaml

with open("config.yaml", "r") as ymlfile:
    config = yaml.load(ymlfile, Loader=yaml.FullLoader)
#
api_url = f"https://app.harness.io/gateway/api/graphql?accountId={config['harness']['account_id']}"
headers = {"x-api-key": config["harness"]["api_key"], "Content-Type": "application/json"}
application_name = config["harness"]["application_name"]
infradefinition_ecs = config["harness"]["infradefinition_ecs"]
service = config["harness"]["service"]
artifact_source_name = config["harness"]['artifact_source_name']

query="""
query {
  applicationByName(name:"%s"){
    id
  }
}
""" % (application_name)

def run_query(query):
  request = requests.post(api_url, json={'query': query}, headers=headers)
  if request.status_code == 200:
	  return request.json()
  else:
    raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))

result = run_query(query)
application_id = result['data']['applicationByName']['id']

query="""
query {
  workflowByName(applicationId:"%s",workflowName:"Opsani Rolling"){
    id
	  name
  }
}
""" % (application_id)
result = run_query(query)
workflow_id = result['data']['workflowByName']['id']

mutation="""
mutation {
  startExecution(input: {
    applicationId: "%s"
    entityId: "%s"
    executionType: WORKFLOW,
    variableInputs: [
      {
        name: "name"
        variableValue: {
          type: NAME
          value: "canary"
        }
      },
      {
        name: "cpu"
        variableValue: {
          type: NAME
          value: "256"
        }
      },
      {
        name: "mem"
        variableValue: {
          type: NAME
          value: "512"
        }
      },
      {
        name: "InfraDefinition_ECS"
        variableValue: {
          type: NAME
          value: "%s"
        }
      },
      {
        name: "Service"
        variableValue: {
          type: NAME
          value: "%s"
        }
      }
    ]
    serviceInputs: [ {
      name: "web-canary",
      artifactValueInput: {
        valueType: BUILD_NUMBER
        buildNumber: {
          buildNumber: "latest"
          artifactSourceName: "%s"
        }
      }
    }
    ]
    notes: "Triggered by Opsani Engine",
  }) {
    clientMutationId
    warningMessage
  }
}
""" % (application_id,workflow_id,infradefinition_ecs,service,artifact_source_name)

result = run_query(mutation)
# = requests.post(api_url, json={'query': mutation}, headers=headers)

print(application_id)
print(workflow_id)
print(result)

import requests
import json
import yaml

with open("config.yaml", "r") as ymlfile:
    config = yaml.load(ymlfile, Loader=yaml.FullLoader)
#
api_url = f"https://app.harness.io/gateway/api/graphql?accountId={config['harness']['account_id']}"
headers = {"x-api-key": config["harness"]["api_key"], "Content-Type": "application/json"}
application_name = config["harness"]["application_name"]
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
  pipelineByName(applicationId:"%s",pipelineName:"Opsani Promotion"){
    id
	  name
  }
}
""" % (application_id)
result = run_query(query)
print(result)
pipeline_id = result['data']['pipelineByName']['id']

mutation="""
mutation {
  startExecution(input: {
    applicationId: "%s"
    entityId: "%s"
    executionType: PIPELINE,
    variableInputs: [
      {
        name: "cpu"
        variableValue: {
          type: NAME
          value: "2048"
        }
      },
      {
        name: "mem"
        variableValue: {
          type: NAME
          value: "4096"
        }
      }
    ]
    notes: "Triggered by Opsani Engine",
  }) {
    clientMutationId
    warningMessage
  }
}
""" % (application_id,pipeline_id)

#request = requests.post(api_url, json={'query': mutation}, headers=headers)
result = run_query(mutation)
print(application_id)
print(pipeline_id)
print(result)

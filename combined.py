import requests
import json
import yaml
import sys

with open("config.yaml", "r") as ymlfile:
    config = yaml.load(ymlfile, Loader=yaml.FullLoader)

harness = {
    "token": config["adjust"]["token"],
    "accountId": config["harness"]["accountId"],
    "application": config["harness"]["application"],
    "apiKey": config["harness"]["apiKey"],
}

data = {
    "application": config["harness"]["application"],
    "parameters": {"cpu": sys.argv[1], "mem": sys.argv[2],},
}

def trigger_canary(data):
    headers = {"content-type": "application/json"}
    url = f"https://app.harness.io/gateway/api/webhooks/{config['adjust']['token']}?accountId={harness['accountId']}"
    data["parameters"]["adjust"] = "True"
    trigger_result = requests.post(url, json=data, headers=headers).json()
    return trigger_result


def trigger_promote(data):
    headers = {"content-type": "application/json"}
    url = f"https://app.harness.io/gateway/api/webhooks/{config['promote']['token']}?accountId={harness['accountId']}"
    data["parameters"]["promote"] = "True"
    trigger_result = requests.post(url, json=data, headers=headers).json()
    get_trigger_status(trigger_result)

def get_trigger_status(response):
    headers = {
        "X-API-KEY": harness["apiKey"],
        "content-type": "application/json",
    }
    harness_api_url = response["apiUrl"].replace("https://app.harness.io/api/","https://app.harness.io/gateway/api/")
    status = requests.get(url=harness_api_url, headers=headers).json()
    # Status returns as one of the following:
    #
    # {'status': 'RUNNING'}
    # {'status': 'FAILED'}
    # {'status': 'SUCCESS'}
    return status
    
def get_state(config):
    url = f"https://api.opsani.com/accounts/{config['opsani']['account']}/applications/{config['opsani']['app_name']}/config/"
    headers = {
        "Content-type": "application/merge-patch+json",
        "Authorization": f"Bearer {config['opsani']['token']}",
    }
    opsani_config = requests.get(url, headers=headers).json()
    return opsani_config

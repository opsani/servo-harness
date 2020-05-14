# Opsani Servo adjust plugin for Harness.io

Optune servo driver for Harness.io

This driver supports updating the cpu and memory of Kubernetes or Amazon ECS deployments by triggering a harness workflow passing the desired values as parameters. It then monitors the status of the workflow until it reaches the SUCCESS state. If it reaches the FAILED state, an error will be raised.

## Config

```yaml
harness:
  settings: # OPTIONAL. Guard rails for canary adjustment
    mem:
      min: 0.5
      max: 1
      step: 0.25
      default: 0.5 # Returned as value when OCO userdata does not contain value for memory
    cpu:
      min: 0.5
      max: 1
      step: 0.25
      default: 0.5 # Returned as value when OCO userdata does not contain value for cpu
  account_id: aaaa # REQUIRED. Id of harness account
  application: bbbb # REQUIRED. Id of the harness application
  api_key: cccc # REQUIRED. X-API-KEY for authentication during retrieval of workflow status
  adjust_token: dddd # REQUIRED. Webhook event token for adjustment of canary settings
  promote_token: eeee # NOT IMPLEMENTED YET. Webhook event token for promotion of settings
  opsani_account: ffff # REQUIRED. Optune account name
  opsani_app_name: gggg # REQUIRED. Name of application in Optune
  opsani_token: hhhh # REQUIRED. Optune auth token
  target_platform: k8s # REQUIRED. Either 'ecs' or 'k8s'
  adjust_timeout: 3600 # OPTIONAL. How long to wait for workflow to be in SUCCESS or FAILED status
```

## How to run tests

Prerequisites:

* Python 3.5 or higher
* PyTest 4.3.0 or higher

Follow these steps:

1. Pull the repository
1. Copy/symlink `adjust` (no file extension) from this repo's project folder to folder `test/`, rename to `adjust_driver.py`
1. Copy/symlink `adjust.py` from `https://github.com/opsani/servo/tree/master/` to folder `test/`
1. Add a valid `config.yaml` to folder `test/` (see config.yaml.example for a reference)
1. Run `python3 -m pytest` from the test folder

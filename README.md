# Opsani Servo adjust plugin for Harness.io

Optune servo driver for Harness.io

This driver supports updating the cpu and memory of Kubernetes or Amazon ECS deployments by triggering a harness workflow passing the desired values as parameters. It then monitors the status of the workflow until it reaches the SUCCESS state. If it reaches the FAILED state, an error will be raised.

## Environment Variables

OPTUNE_USE_DRIVER_NAME - When set to true or 1, the connector will use it's own filename to determine which config section to use

## Config

```yaml
harness: # NOTE: if OPTUNE_USE_DRIVER_NAME is truthy, the name of the connector file will be used instead, eg "adjust"
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
  opsani_account: ffff # REQUIRED. Optune account name
  opsani_app_name: gggg # REQUIRED. Name of application in Optune
  adjust_timeout: 3600 # OPTIONAL. How long to wait for workflow to be in SUCCESS or FAILED status
  adjust_on: canary # OPTIONAL. when specified, the input data control.userdata.deploy_to must match the value configured here
  target_platform: k8s # REQUIRED. Either 'ecs' or 'k8s'
  adjust_interface: graphql # OPTIONAL. Canary adjustment interafce, defaults to graphql, valid values are graphql and webhook
  promote_interface: graphql # OPTIONAL. Mainline adjustment interafce, defaults to graphql, valid values are graphql and webhook
  account_id: aaaa # REQUIRED. Id of harness account
  application_name: bbbb # Name of the harness application
  graphql_url: cccc # REQUIRED. URL of harness graphql API, used to query webhook info as well
  ssl_verify: True # OPTIONAL. Set to False to disable verification of graphql API ssl verification
  # graphql config (REQUIRED when either target interface is graphql)
  artifact_source_name: dddd # Name of Artifact to be deployed
  infradefinition_ecs: eeee # Name of Harness infradefinition_ecs
  service: hhhh # Name of Harness service
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

## Harness Integration

Fore documention on integrating into Harness, please see [Integration Documentation](doc/README.md)

## Servo

See [Sample Servo Manifest](doc/servo.yaml.example) for an example of how to deploy the servo via k8s.

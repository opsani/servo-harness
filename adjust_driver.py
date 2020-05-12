#!/usr/bin/env python3
import json
import os
import requests
import sys
import time
import yaml

from adjust import Adjust, AdjustError

DESC = "Harness adjust driver for Opsani Optune"
VERSION = "0.0.1"
HAS_CANCEL = False

DEFAULT_MEM_STEP=0.125 # cores
DEFAULT_MEM_MIN=0.125 # cores
DEFAULT_MEM_MAX=4 # cores
DEFAULT_CPU_STEP=0.125 # GiB
DEFAULT_CPU_MIN=0.125 # GiB
DEFAULT_CPU_MAX=4 # GiB
DEFAULT_ADJUST_TIMEOUT=3600

config_path = os.environ.get('OPTUNE_CONFIG', './config.yaml')

class HarnessDriver(Adjust):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not (self.args.info or self.args.version):
            self.load_config()

    def load_config(self):
        try:
            with open(config_path) as in_file:
                c = yaml.safe_load(in_file)
        except yaml.YAMLError as e:
            raise Exception('Could not parse config file located at "{}". '
                            'Please check its contents. Error: {}'.format(config_path, str(e)))

        assert c and c.get('harness', None), 'Harness Servo Configuration was not provided in "{}". ' \
                                        'Please refer to README.md'.format(config_path)
        
        h = c['harness']
        # TODO config validation

        self.config = h

    def query(self):
        settings = {
            'cpu': {
                'type': 'range',
                'unit': 'cores',
                'min': self.config.get('cpu', {}).get('min', DEFAULT_CPU_MIN),
                'max': self.config.get('cpu', {}).get('max', DEFAULT_CPU_MAX),
                'step': self.config.get('cpu', {}).get('step', DEFAULT_CPU_STEP)
            },
            'mem': {
                'type': 'range',
                'unit': 'GiB',
                'min': self.config.get('mem', {}).get('min', DEFAULT_MEM_MIN), 
                'max': self.config.get('mem', {}).get('max', DEFAULT_MEM_MAX), 
                'step': self.config.get('mem', {}).get('step', DEFAULT_MEM_STEP)
            }
        }

        url = f"https://api.opsani.com/accounts/{self.config['opsani_account']}/applications/{self.config['opsani_app_name']}/config/"
        headers = {
            "Content-type": "application/merge-patch+json",
            "Authorization": f"Bearer {self.config['opsani_token']}",
        }
        opsani_config = requests.get(url, headers=headers).json()
        userdata = opsani_config.get('adjustment', {}).get('control', {}).get('userdata')

        if userdata and userdata.get('cpu'):
            settings['cpu']['value'] = cpuunits(userdata['cpu'])
        else:
            # TODO: require default in config validation or implement default values for setting defaults
            settings['cpu']['value'] = self.config.get('cpu', {}).get('default')
        
        if userdata and userdata.get('mem'):
            settings['mem']['value'] = memunits(userdata['mem'])
        else:
            settings['mem']['value'] = self.config.get('mem', {}).get('default')

        return { 'application': { 'components': { 'canary': { 'settings': settings } } } }

    def adjust(self, data):
        # TODO: promote component
        canary_settings = data['application']['components'].get('canary', {}).get('settings')
        if not canary_settings:
            return # Nothing to adjust

        trigger_headers = {"content-type": "application/json"}
        trigger_json_data = {
            "application": self.config["application"],
            'adjust': 'True', # TODO: only set this on canary comp
            "parameters": {
                "cpu": canary_settings['cpu']['value'], 
                "mem": '{}Gi'.format(canary_settings['mem']['value'])
            },
        }
        trigger_params = { 'accountId': self.config['account_id'] }
        trigger_url = f"https://app.harness.io/gateway/api/webhooks/{self.config['adjust_token']}"

        response = requests.post(url=trigger_url, json=trigger_json_data, headers=trigger_headers, params=trigger_params)
        if not response.ok:
            raise AdjustError('Unable to trigger canary harness workflow. Status code {}. Data {}'.format(response.status_code, response.text))
        trigger_result = response.json()
        
        status_url = trigger_result["apiUrl"].replace("https://app.harness.io/api/","https://app.harness.io/gateway/api/")
        status_headers = {
            "X-API-KEY": self.config["api_key"],
            "content-type": "application/json",
        }

        start_time = time.time()
        while True:
            status_response = requests.get(url=status_url, headers=status_headers)
            if not status_response.ok:
                raise AdjustError('Unable to get triggered workflow status. Status code {}. Data {}'.format(status_response.status_code, status_response.text))
            
            status_json = status_response.json()
            if status_json['status'] == 'SUCCESS':
                break
            if status_json['status'] == 'FAILED':
                raise AdjustError('Triggered workflow finished with FAILED status: {}'.format(status_json))
            # else: status == 'RUNNING'

            if time.time() - start_time > self.config.get('adjust_timeout', DEFAULT_ADJUST_TIMEOUT):
                raise AdjustError('Time out waiting for completion of adjustment')

            time.sleep(30)

def cpuunits(s):
    '''convert a string for CPU resource (with optional unit suffix) into a number'''
    if s[-1] == "m": # there are no units other than 'm' (millicpu)
        return float(s[:-1])/1000.0
    return float(s)

# valid mem units: E, P, T, G, M, K, Ei, Pi, Ti, Gi, Mi, Ki
# nb: 'm' suffix found after setting 0.7Gi
mumap = {"E":1000**6,  "P":1000**5,  "T":1000**4,  "G":1000**3,  "M":1000**2,  "K":1000, "m":1000**-1,
         "Ei":1024**6, "Pi":1024**5, "Ti":1024**4, "Gi":1024**3, "Mi":1024**2, "Ki":1024}


def memunits(s):
    '''convert a string for memory resource (with optional unit suffix) into a number'''
    for u, m in mumap.items():
        if s.endswith(u):
            return float(s[:-len(u)]) * m
    return float(s)

if __name__ == '__main__':
    driver = HarnessDriver(cli_desc=DESC, supports_cancel=HAS_CANCEL, version=VERSION, progress_interval=30)
    driver.run()

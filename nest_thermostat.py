import requests
import json
import os

class thermostat:
    def __init__(self):
        self.access_token = self.get_access_token()
        self.request_headers = { 'Content-Type' : 'application/json',
                                'Authorization' : 'Bearer ' + self.access_token
                            }
        project_id = os.environ['NEST_GCP_PROJECT_ID']
        device_id = os.environ['NEST_GCP_DEVICE_ID']
        self.endpoint = f'https://smartdevicemanagement.googleapis.com/v1/enterprises/{project_id}/devices/{device_id}'

    def get_access_token(self):
        NEST_GCP_CLIENT_ID = os.environ['NEST_GCP_CLIENT_ID']
        NEST_GCP_CLIENT_SECRET = os.environ['NEST_GCP_CLIENT_SECRET']
        NEST_GCP_REFRESH_TOKEN = os.environ['NEST_GCP_REFRESH_TOKEN']
        refresh_url = f'https://www.googleapis.com/oauth2/v4/token?client_id={NEST_GCP_CLIENT_ID}&client_secret={NEST_GCP_CLIENT_SECRET}&refresh_token={NEST_GCP_REFRESH_TOKEN}&grant_type=refresh_token'
        response = requests.post(refresh_url)
        access_token = response.json()["access_token"]
        return access_token

    def execute_thermostat_command(self, command, params):
        post_url = self.endpoint + ':executeCommand'
        message = {'command': f'sdm.devices.commands.{command}',
                    'params': params
                    }
        response = requests.post(post_url, headers=self.request_headers, json=message)
        if response.status_code != 200:
            print(f' * error: {command} failed with status code {response.status_code}')
            exit(1)

    def set_mode(self, mode):
        params = {'mode' : mode}
        self.execute_thermostat_command('ThermostatMode.SetMode', params)

    def check_mode(self):
        response = requests.get(self.endpoint, headers=self.request_headers)
        return response.json()['traits']['sdm.devices.traits.ThermostatMode']['mode']

    def set_fan_timer(self, duration_mins):
        # System must be set to HEAT in order for fan to run - but HEAT mode doesn't it's always blowing warm air. You can just set the heat to a low temp.
        
        # If you want to prevent the fan from running when the heat is set to off, comment out the below line
        # self.set_mode('HEAT')

        params = {'timerMode' : 'ON',
                  'duration' : str(duration_mins * 60) + 's'
                }
        
        current_mode = self.check_mode() 

        # Heat must be on in order for fan to run.
        # You can set the heat to turn on with self.set_mode('HEAT')...
        # ...but leaving it like this creates a manual override, since anyone can disable the script by setting heat to OFF)
        if current_mode == "HEAT":
            self.execute_thermostat_command('Fan.SetTimer', params)
        else:
            print(f'Heat is set to {current_mode}, doing nothing')

    

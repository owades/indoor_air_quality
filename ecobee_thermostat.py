import requests
import json
import os
import math

class thermostat:
    def __init__(self):
        self.access_token = self.get_access_token()
        self.request_headers = { 'Content-Type': 'application/json;charset=UTF-8',
                                'Authorization' : 'Bearer ' + self.access_token
                            }
        self.endpoint = 'https://api.ecobee.com/1/thermostat'

    def get_access_token(self):
        api_key = os.environ['ECOBEE_API_KEY']
        auth_code = os.environ['ECOBEE_AUTH_CODE']
        refresh_token = os.environ['ECOBEE_REFRESH_TOKEN']
        token_url = f'https://api.ecobee.com/token?grant_type=refresh_token&code={refresh_token}&client_id={api_key}'
        response = requests.post(token_url)
        access_token = response.json()["access_token"]
        return access_token

    def check_mode(self):
        selection = {'selection':  {
                        'selectionType': 'registered',
                        'selectionMatch': '',
                        'includeSettings':'true'
                    }}

        mode = self.execute_thermostat_command(selection)["thermostatList"][0]["settings"]["hvacMode"]
        print(f'mode: {mode}')
        return mode

    def execute_thermostat_command(self, selection):
   
        params = {'json': json.dumps(selection)}
        
        response = requests.get(self.endpoint, headers=self.request_headers, params=params)
        
        return response.json()

    # Runs fan for the provided time - rounding up to the nearest hour.
    def set_fan_timer(self, duration_mins):
        duration_hours = math.ceil(duration_mins/60)

        selection = {
            "selection": {
                "selectionType":"registered",
                "selectionMatch":""
            },
             "functions": [{
                "type":"setHold",
                "params":{
                    "holdType":"holdHours",
                    "holdHours":duration_hours,
                    # Need to figure out proper hold temps
                    "heatHoldTemp":690,
                    "coolHoldTemp":720,
                    "fan": "on"
                }
            }]
        }  
        response = self.execute_thermostat_command(selection)
        print(response)

    

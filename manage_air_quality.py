import sys
import requests
import json
import requests
import os

class purple_air_sensor:
    def __init__(self, device_id):
        self.endpoint = f'https://www.purpleair.com/json?show={device_id}'

    def get_aqi(self):
        result = requests.get(self.endpoint)
        data = json.loads(result.text)
        pm2_5_atm = float(data['results'][0]['pm2_5_atm'])
        return pm2_5_atm

class nest_thermostat:
    def __init__(self, access_token, project_id, device_id):
        self.access_token = access_token
        self.request_headers = { 'Content-Type' : 'application/json',
                                'Authorization' : 'Bearer ' + access_token
                            }
        self.endpoint = f'https://smartdevicemanagement.googleapis.com/v1/enterprises/{project_id}/devices/{device_id}'

    def set_mode(self, mode):
        params = {'mode' : mode}
        self.execute_thermostat_command('ThermostatMode.SetMode', params)

    def set_fan_timer(self, duration_mins):
        # System must be set to HEAT in order for fan to run - but HEAT mode doesn't it's always blowing warm air. You can just set the heat to a low temp.
        self.set_mode('HEAT')
        params = {'timerMode' : 'ON',
                  'duration' : str(duration_mins * 60) + 's'
                }
        self.execute_thermostat_command('Fan.SetTimer', params)

    def execute_thermostat_command(self, command, params):
        post_url = self.endpoint + ':executeCommand'
        message = {'command': f'sdm.devices.commands.{command}',
                    'params': params
                    }
        response = requests.post(post_url, headers=self.request_headers, json=message)
        if response.status_code != 200:
            print(f' * error: {command} failed with status code {response.status_code}')
            exit(1)

    def check_mode():
        response = requests.get(self.endpoint, request_headers=self.request_headers)
        return response.json()['traits']['sdm.devices.traits.ThermostatMode']['mode']

def get_google_access_token():
    NEST_GCP_CLIENT_ID = os.environ['NEST_GCP_CLIENT_ID']
    NEST_GCP_CLIENT_SECRET = os.environ['NEST_GCP_CLIENT_SECRET']
    NEST_GCP_REFRESH_TOKEN = os.environ['NEST_GCP_REFRESH_TOKEN']
    refresh_url = f'https://www.googleapis.com/oauth2/v4/token?client_id={NEST_GCP_CLIENT_ID}&client_secret={NEST_GCP_CLIENT_SECRET}&refresh_token={NEST_GCP_REFRESH_TOKEN}&grant_type=refresh_token'
    response = requests.post(refresh_url)
    access_token = response.json()["access_token"]
    return access_token

class air_quality_manager:
    def __init__(self, aqi_sensor, thermostat, aqi_ceiling, fan_runtime_mins):
        aqi = aqi_sensor.get_aqi()
        if(aqi >= aqi_ceiling):
            print(f'Current AQI of {str(aqi)} is above the acceptable value of {str(aqi_ceiling)}, running fan for {str(fan_runtime_mins)} min')
            thermostat.set_fan_timer(fan_runtime_mins)
        else:
            print(f'Current AQI of {str(aqi)} is below the acceptable value of {str(aqi_ceiling)}')

def main(argv):
    aqi_sensor = purple_air_sensor(os.environ['PURPLE_AIR_DEVICE_ID'])
    thermostat = nest_thermostat(get_google_access_token(), os.environ['NEST_GCP_PROJECT_ID'], os.environ['NEST_GCP_DEVICE_ID'])
    air_quality_manager(aqi_sensor, thermostat, 50, 15)

if __name__ == '__main__':
   main(sys.argv[1:])
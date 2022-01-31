import sys
import requests
import json
import requests
import os

AQI_CEILING = 50
REFRESH_INTERVAL_MINS = 5
REFRESH_INTERVAL_SECS = REFRESH_INTERVAL_MINS * 60
AQI_URL = "https://www.purpleair.com/json?show="
PURPLE_AIR_DEVICE_ID = "110112"
CLIENT_ID = os.environ['NEST_GCP_CLIENT_ID']
REFRESH_TOKEN = os.environ['NEST_GCP_REFRESH_TOKEN']
CLIENT_SECRET = os.environ['NEST_GCP_CLIENT_SECRET']
REFRESH_URL = f'https://www.googleapis.com/oauth2/v4/token?client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}&refresh_token={REFRESH_TOKEN}&grant_type=refresh_token'
PROJECT_ID = os.environ['NEST_GCP_PROJECT_ID']
DEVICE_ID = os.environ['NEST_GCP_DEVICE_ID']
BASE_QUERY_URL = f'https://smartdevicemanagement.googleapis.com/v1/enterprises/{PROJECT_ID}/devices/{DEVICE_ID}'

def get_access_token():
    response = requests.post(REFRESH_URL)
    access_token = response.json()["access_token"]
    return access_token

HEADERS = { 'Content-Type' : 'application/json',
            'Authorization' : 'Bearer ' + get_access_token()
            }

def main(argv):
    aqi = get_aqi()
    if(aqi >= AQI_CEILING):
        print(f'Current AQI of {str(aqi)} is above the acceptable value of {str(AQI_CEILING)}, running fan for {str(REFRESH_INTERVAL_MINS)} min')
        set_fan_timer(REFRESH_INTERVAL_SECS * 2)
    else:
        print(f'Current AQI of {str(aqi)} is below the acceptable value of {str(AQI_CEILING)}, will check again in {str(REFRESH_INTERVAL_MINS)} min')

def get_aqi():
    result = requests.get(AQI_URL + PURPLE_AIR_DEVICE_ID)
    data = json.loads(result.text)
    pm2_5_atm = float(data['results'][0]['pm2_5_atm'])
    return pm2_5_atm

def set_mode(mode):
    params = {'mode' : mode}
    execute_thermostat_command('SetMode', params)

def set_fan_timer(duration_secs):
    # System must be set to HEAT in order for fan to run - but HEAT mode doesn't it's always blowing warm air. You can just set the heat to a low temp.
    turn_heat_on_if_off()
    params = {'timerMode' : 'ON',
              'duration' : str(duration_secs) + 's'
            }
    execute_thermostat_command('SetTimer', params)

def execute_thermostat_command(command, params):
    post_url = BASE_QUERY_URL + ':executeCommand'
    message = {'command': f'sdm.devices.commands.Fan.{command}',
                'params': params
                }

    response = requests.post(post_url, headers=HEADERS, json=message)
    print(response.json())

def turn_heat_on_if_off():
    response = requests.get(BASE_QUERY_URL, headers=HEADERS)
    mode = response.json()['traits']['sdm.devices.traits.ThermostatMode']['mode']
    if (mode == 'OFF'):
        print('Heat is off, turning on...')
        set_mode('HEAT')

if __name__ == '__main__':
   main(sys.argv[1:])
import json
import os
import requests

class sensor:
    def __init__(self):
        device_id = os.environ['PURPLE_AIR_DEVICE_ID']
        self.api_key = os.environ['PURPLE_AIR_READ_API_KEY']
        self.endpoint = f'https://api.purpleair.com/v1/sensors/{device_id}'

    def get_aqi(self):
        result = requests.get(self.endpoint, headers={"X-API-Key":self.api_key})
        # print(f'Status: {result.status_code}')
        data = json.loads(result.text)
        pm2_5_atm = float(data['sensor']['pm2.5_atm'])
        return pm2_5_atm

def main():
    aqi_sensor = sensor()
    print(aqi_sensor.get_aqi());

if __name__ == '__main__':
   main()
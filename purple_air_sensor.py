import json
import os
import requests

class sensor:
    def __init__(self):
        device_id = os.environ['PURPLE_AIR_DEVICE_ID']
        self.endpoint = f'https://www.purpleair.com/json?show={device_id}'

    def get_aqi(self):
        result = requests.get(self.endpoint)
        data = json.loads(result.text)
        pm2_5_atm = float(data['results'][0]['pm2_5_atm'])
        return pm2_5_atm
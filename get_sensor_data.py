import requests
import json

SMOKY_TRESHOLD = 50

result = requests.get("https://www.purpleair.com/json?show=110112")
data = json.loads(result.text)
pm2_5_atm = float(data['results'][0]['pm2_5_atm'])
print('pm2_5_atm: ' + str(pm2_5_atm))
if(pm2_5_atm >= SMOKY_TRESHOLD):
    print("smoky!")
else:
    print("all good!")
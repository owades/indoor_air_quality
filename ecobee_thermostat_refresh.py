import requests
import json
import os

api_key = os.environ['ECOBEE_API_KEY']
auth_code = os.environ['ECOBEE_AUTH_CODE']
token_url = f'https://api.ecobee.com/token?grant_type=ecobeePin&code={auth_code}&client_id={api_key}'
response = requests.post(token_url)
print(response.json())
access_token = response.json()["access_token"]
refresh_token = response.json()["refresh_token"]
print(f'Access Token: {access_token}')
print(f'Refresh Token: {refresh_token}')

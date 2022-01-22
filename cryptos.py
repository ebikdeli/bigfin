# We use 'CoinAPI' apis in the script. Here is the docs: https://docs.coinapi.io/#md-docs
import requests
import redis

BASE_URL = 'https://rest.coinapi.io'

currencies = 'BTC'
REQ_URL = f'/v1/assets?filter_asset_id={currencies}'

URL = BASE_URL + REQ_URL
headers = {'X-CoinAPI-Key': '8AC81A58-86B8-46E6-A1C3-D1A8D6E36A35'}

r = requests.get(url=URL, headers=headers)

data = r.json()
if data:
    for i in data:
        for k, v in i.items():
            print(f"{k}: {v}")
        # print(i['name'])
red = redis.Redis(host='127.0.0.1', port=6379, db=0)
# red.set('name', 'Ehsan')
# print(red.get('name').decode())
print(red.get('age'), '   ', red.get('name'))

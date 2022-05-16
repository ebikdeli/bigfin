"""
This script run every arbitrary time period to get every crypto or fiat currencies we want.
Instead of using 'database' directly, we are using 'redis' to cache received data. This way
the webapp getting so much faster and functions better.
"""
# We use 'CoinAPI' apis in the script. Here is the docs: https://docs.coinapi.io/#md-docs
import requests
import redis
from redis import exceptions

# Setup redis connection and object:
try:
    red = redis.Redis(host='127.0.0.1', port=6379, db=0)
    red.ping()
except (exceptions.ConnectionError, exceptions.TimeoutError):
    print('No connection made...')
    quit()
# Delete all coins in the redis cache
# red.ltrim('bitcoin', 99, 0)
# red.ltrim('dogecoin', 99, 0)
# red.ltrim('ethereum', 99, 0)

# Using 'request' to get price of the wanted currencies:
# BASE_URL = 'https://rest.coinapi.io/'
BASE_URL = 'https://rest-sandbox.coinapi.io'
currencies = 'BTC,ETH,DOGE'
REQ_URL = f'/v1/assets?filter_asset_id={currencies}'
URL = BASE_URL + REQ_URL
headers = {'X-CoinAPI-Key': '8AC81A58-86B8-46E6-A1C3-D1A8D6E36A35'}
try:
    r = requests.get(url=URL, headers=headers)
except requests.ConnectionError:
    print('Could not connect the "coinAPI" server...')
    exit()
except requests.Timeout:
    print('Connection takes too long...')
    quit()
if r.status_code == 200:
    data = r.json()
    if data:
        for currency in data:
            # To delete redis list completely:
            # print(red.ltrim(currency['name'].lower(), 99, 0))
            if not red.llen(currency['name'].lower()):
                values = (currency['asset_id'], currency['price_usd'], currency['data_end'])
                red.lpush(currency['name'].lower(), *values)
            else:
                red.lset(currency['name'].lower(), 0, currency['asset_id'])
                red.lset(currency['name'].lower(), 1, currency['price_usd'])
                red.lset(currency['name'].lower(), 2, currency['data_end'])
    else:
        print('No data received from "coinAPI"')
else:
    print('There is a problem in answer from server')
"""
x = red.lrange('bitcoin', 0, -1)
print(x)
y = red.lrange('ethereum', 0, -1)
print(y)
z = red.lrange('dogecoin', 0, -1)
print(z)
"""
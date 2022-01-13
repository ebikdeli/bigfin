from django.shortcuts import render, redirect
from django.contrib.auth.models import User, AnonymousUser
# from profile.models import Profile
import websocket
import json
import requests


API_KEY = '8AC81A58-86B8-46E6-A1C3-D1A8D6E36A35'

BASE_URL = 'https://rest-sandbox.coinapi.io/'
ASSETS = ['BTC', 'ETH', ]
HEADER = {'X-CoinAPI-Key': API_KEY, 'Accept': 'application/json',
          'Accept-Encoding': 'deflate, gzip'}

WS_URL = 'ws://ws.coinapi.io/v1/'
WS_PARAMS = {'type': 'hello', 'apikey': API_KEY, 'heatbeat': False,
             'subscribe_data_type': ['trade', ], 'subscribe_filter_asset_id': ['BTC', ]}

REQUEST_URL_BITCOIN = 'v1/ohlcv/BTC/USD/latest?period_id=1HRS&limit=10'
REQUEST_URL_ETHERIUM = 'v1/ohlcv/ETH/USD/latest?period_id=1HRS&limit=10'
REQUEST_URL_DOGECOIN = 'v1/ohlcv/DOGE/USD/latest?period_id=1HRS&limit=10'


def index(request):
    try:
        # if isinstance(request.user, AnonymousUser):
        #    return redirect('profile:create_user')
        r_btc = requests.get(url=BASE_URL + REQUEST_URL_BITCOIN, headers=HEADER)
        r_eth = requests.get(url=BASE_URL + REQUEST_URL_ETHERIUM, headers=HEADER)
        r_doge = requests.get(url=BASE_URL + REQUEST_URL_DOGECOIN, headers=HEADER)
        print(f'{r_btc.status_code} {r_eth.status_code} {r_doge.status_code}')
        data_btc, data_eth, data_doge = r_btc.json()[0], r_eth.json()[0], r_doge.json()[0]
        print(data_btc, '\n', data_eth, '\n', data_doge)
        
    except Profile.DoesNotExist:
        return redirect('profile:edit_profile', username=request.user.username)

    except ValueError:
        data_btc = {'price_high': '0000', 'price_low': '0000', 'price_close': 'اشکال در برقراری ارتباط با سرویس خارجی'}
        data_eth = {'price_high': '0000', 'price_low': '0000', 'price_close': 'اشکال در برقراری ارتباط با سرویس خارجی'}
        data_doge = {'price_high': '0000', 'price_low': '0000', 'price_close': 'اشکال در برقراری ارتباط با سرویس خارجی'}

    except AttributeError:
        data_btc = {'price_high': '0000', 'price_low': '0000', 'price_close': 'اشکال در برقراری ارتباط با سرویس خارجی'}
        data_eth = {'price_high': '0000', 'price_low': '0000', 'price_close': 'اشکال در برقراری ارتباط با سرویس خارجی'}
        data_doge = {'price_high': '0000', 'price_low': '0000', 'price_close': 'اشکال در برقراری ارتباط با سرویس خارجی'}
        
    return render(request, 'vitrin/templates/index.html', context={
                    'high_btc': data_btc['price_high'],
                    'low_btc': data_btc['price_low'],
                    'price_now_btc': data_btc['price_close'],
                    'high_eth': data_eth['price_high'],
                    'low_eth': data_eth['price_low'],
                    'price_now_eth': data_eth['price_close'],
                    'high_doge': data_doge['price_high'],
                    'low_doge': data_doge['price_low'],
                    'price_now_doge': data_doge['price_close']})


def page1(request):
    return render(request, 'vitrin/templates/page1.html')


def page2(request):
    return render(request, 'vitrin/templates/page2.html')

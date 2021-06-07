from django.shortcuts import render
import websocket
import json
import requests
from django.contrib.auth.models import User


API_KEY = '8AC81A58-86B8-46E6-A1C3-D1A8D6E36A35'

BASE_URL = 'https://rest-sandbox.coinapi.io/'
ASSETS = ['BTC', 'ETH', ]
HEADER = {'X-CoinAPI-Key': API_KEY, 'Accept': 'application/json',
          'Accept-Encoding': 'deflate, gzip'}

WS_URL = 'ws://ws.coinapi.io/v1/'
WS_PARAMS = {'type': 'hello', 'apikey': API_KEY, 'heatbeat': False,
             'subscribe_data_type': ['trade', ], 'subscribe_filter_asset_id': ['BTC', ]}

REQUEST_URL = 'v1/ohlcv/BTC/USD/latest?period_id=1HRS&limit=10'


def index(request):
    try:
        r = requests.get(url=BASE_URL + REQUEST_URL, headers=HEADER)
        print(r.status_code)
        data = r.json()[0]
        print(type(data))
        print(data)
    except:
        data = {'price_high': '0000', 'price_low': '0000', 'price_close': 'اشکال در برقراری ارتباط با سرویس خارجی'}

    return render(request, 'vitrin/templates/index.html', context={
                  'high': data['price_high'],
                  'low': data['price_low'],
                  'price_now': data['price_close']})


def page1(request):
    return render(request, 'vitrin/templates/page1.html')


def page2(request):
    return render(request, 'vitrin/templates/page2.html')

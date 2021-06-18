from bigfin.celery import app
import requests


@app.task(name='get_bitcoin_price')
def get_bitcoin_price():
    return 'hello world!'

from django.shortcuts import render
from django.http import JsonResponse

import redis
from redis import exceptions


def index(request):
    """Index page of view"""
    return JsonResponse(data='Hello my beautiful world', safe=False)
    # return render(request, 'vitrin/templates/index.html')


def price_list(request):
    """Send all price to client from redis"""
    try:
        red = redis.Redis(host='127.0.0.1', port=6379, db=0)
        red.ping()
    except (exceptions.ConnectionError, exceptions.TimeoutError):
        print('No connection made...')
        return JsonResponse({'error': 'Could not send the data. Check the server out...'})
    bitcoin = red.lindex(b'bitcoin', 1).decode()
    dogecoin = red.lindex(b'dogecoin', 1).decode()
    ethereum = red.lindex(b'ethereum', 1).decode()
    return JsonResponse({'bitcoin': float(bitcoin), 'dogecoin': float(dogecoin), 'ethereum': float(ethereum)})


def page1(request):
    return render(request, 'vitrin/templates/page1.html')


def page2(request):
    return render(request, 'vitrin/templates/page2.html')

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.authtoken.models import Token

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


def create_token(request):
    if request.user.is_authenticated:
        token = Token.objects.filter(user=request.user)
        if token.exists():
            return HttpResponse(f'<h1>User {request.user} already has a authentication token: {token.first().key}</h1>')
        token = Token.objects.create(user=request.user)
        print('Token created for ', request.user.username, '\n')
        print(token, '  ', type(token))
        return JsonResponse(data={'token': token.key}, safe=False)
    return HttpResponse('<h2>User is not authenticated</h2>')


def page2(request):
    return render(request, 'apps/vitrin/templates/page2.html')


def todo_view(request):
    return render(request, 'apps/vitrin/templates/todo_view.html')

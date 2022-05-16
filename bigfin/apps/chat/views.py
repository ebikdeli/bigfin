"""
This view implemented from this document:
https://channels.readthedocs.io/en/stable/tutorial/index.html
"""
from django.shortcuts import render


def index(request):
    return render(request, 'apps/chat/templates/chat/index.html')


def room(request, room_name):
    return render(request, 'apps/chat/templates/chat/room.html', {
        'room_name': room_name
    })

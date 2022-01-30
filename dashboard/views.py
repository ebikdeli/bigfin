"""
Django views does not support DRF authentication tokens. But with a little work we can do this.
but we should remember that it's better to have a only full stack django project or only client-
server based project.
"""
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import authenticate


def dashboard(request):
    """Main dashboard view"""
    try:
        # print(request.auth)
        token = request.headers.get('Authorization', None)
        if token:
            token = token.split()[1]
            print(token)
        else:
            print('No authentication made')
    except AttributeError:
        print('No user authenticated')

    print(request.user, "  ", request.user.is_authenticated)
    return JsonResponse(data='This is user dashboard', safe=False)

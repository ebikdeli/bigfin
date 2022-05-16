"""
Django views does not support DRF authentication tokens. But with a little work we can do this.
but we should remember that it's better to have a only full stack django project or only client-
server based project.
"""
from django.shortcuts import render
from django.http import JsonResponse

from apps.accounts.logins import token_login


def dashboard(request):
    """Main dashboard view"""
    a, b = token_login(request)
    print(a, '  ', b)
    return JsonResponse(data='This is user dashboard', safe=False)

from django.shortcuts import render
from django.http import JsonResponse


def index(request):
    return JsonResponse(data='Hello my beautiful world', safe=False)
    # return render(request, 'vitrin/templates/index.html')


def price_list(request):
    return JsonResponse(data={'Price': 3000000}, safe=False)


def page1(request):
    return render(request, 'vitrin/templates/page1.html')


def page2(request):
    return render(request, 'vitrin/templates/page2.html')

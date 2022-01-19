from django.urls import path
from vitrin import views

app_name = 'vitrin'

urlpatterns = [
    path('', views.index, name='index'),
    path('price_list/', views.price_list, name='price_list'),
    path('page1/', views.page1, name='page1'),
    path('page2/', views.page2, name='page2'),
]

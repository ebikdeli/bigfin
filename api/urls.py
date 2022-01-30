from django.urls import path
from rest_framework.authtoken import views as token_view

from . import views


app_name = 'api'

urlpatterns = [
    path('token-auth/', token_view.obtain_auth_token),
    path('user-list/', views.UserListView.as_view(), name='user-list'),
]

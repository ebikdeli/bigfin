from django.urls import path
from apps.vitrin import views

app_name = 'vitrin'

urlpatterns = [
    path('', views.index, name='index'),
    path('price_list/', views.price_list, name='price_list'),
    path('create-token/', views.create_token, name='create-token'),
    path('page2/', views.page2, name='page2'),
    path('todo-view', views.todo_view, name='todo_view'),
]

from django.urls import path
from dashboard import views
from django.contrib.auth.decorators import login_required

app_name = 'dashboard'

urlpatterns = [
    path('<slug>/', login_required(views.MainDashboardView.as_view()), name='main'),
]

from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from profile.models import Profile
from django.views.generic import DetailView


class MainDashboardView(DetailView):
    model = Profile
    template_name = 'dashboard_base.html'
    context_object_name = 'profile'

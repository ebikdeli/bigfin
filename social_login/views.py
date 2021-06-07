from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from profile.models import Profile
from django.shortcuts import redirect


# Create your views here.
def login(request):
    return render(request, 'social_login/templates/login.html')


@login_required
def home(request):
    try:
        request.user.profile
    except Profile.DoesNotExist:
        return redirect('profile:edit_profile', username=request.user.username)

    return render(request, 'social_login/templates/home.html')

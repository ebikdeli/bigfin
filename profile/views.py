from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.views import auth_login
from profile.models import Profile
from profile.forms import ProfileEditForm, EmailUserForm,\
    ProfileCreateForm, UserCreateForm, UserAuthenticationLoginForm
import re


def profile_login(request):
    if request.method == 'POST':
        user_auth_form = UserAuthenticationLoginForm(request.POST)
        if user_auth_form.is_valid():
            user_auth = user_auth_form.cleaned_data
            user = authenticate(request, username=user_auth['username'], password=user_auth['password'])
            if user is not None:
                login(request, user)
                return redirect('vitrin:index')
            messages.add_message(request, messages.ERROR, 'username or password is wrong!')
    else:
        user_auth_form = UserAuthenticationLoginForm()

    return render(request, 'profile_login.html', {'user_auth_form': user_auth_form})


def profile_create(request):
    if request.method == 'POST':
        user_create_form = UserCreateForm(data=request.POST)
        profile_create_form = ProfileCreateForm(data=request.POST, files=request.FILES)
        if user_create_form.is_valid() and profile_create_form.is_valid():
            user_create_form.save()
            profile_create_form.save()
    else:
        user_create_form = UserCreateForm()
        profile_create_form = ProfileCreateForm()

    return render(request, 'profile/templates/profile_create.html', context={
        'user_create_form': user_create_form,
        'profile_create_form': profile_create_form
    })


def profile_edit(request, username):
    initial_profile_form_data = {
        'phone': Profile.phone,
        'address': Profile.address,
        'picture': Profile.picture,
    }
    email_regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'

    if request.method == 'POST':
        profile_edit_form = ProfileEditForm(data=request.POST, files=request.FILES)
        email_form = EmailUserForm(data=request.POST)
        if profile_edit_form.is_valid() and email_form.is_valid():
            current_user = User.objects.get(username=username)
            current_user.email = email_form.cleaned_data['email']
            try:
                current_profile = current_user.profile
                current_profile.phone = profile_edit_form.cleaned_data['phone']
                current_profile.address = profile_edit_form.cleaned_data['address']
                current_profile.picture = profile_edit_form.cleaned_data['picture']
            except Profile.DoesNotExist:
                current_profile = Profile.objects.create(user=current_user,
                                                         phone=profile_edit_form.cleaned_data['phone'],
                                                         address=profile_edit_form.cleaned_data['address'],
                                                         picture=profile_edit_form.cleaned_data['picture'])
            current_profile.save()
            current_user.save()
            return redirect('vitrin:index')

    else:
        try:
            request.user.profile
            profile_edit_form = ProfileEditForm(initial=initial_profile_form_data)
        except Profile.DoesNotExist:
            profile_edit_form = ProfileEditForm()
        # email_form = EmailUserForm({'email': username}) if re.search(email_regex, username) else EmailUserForm()
        if User.objects.get(username=username).email:
            email_form = EmailUserForm({'email': User.objects.get(username=username).email})
        else:
            email_form = EmailUserForm()

    return render(request, 'profile/templates/profile_edit.html', context={'profile_edit_form': profile_edit_form,
                                                                           'email_form': email_form})

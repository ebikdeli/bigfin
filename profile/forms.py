from django import forms
<<<<<<< HEAD
from django.core.exceptions import ValidationError
# from django.contrib.auth.forms import UserCreationForm
=======
from django.contrib.auth.forms import UserCreationForm
>>>>>>> ffdcd51 (Revert "13/1/2022-13:47 PM")
from profile.models import Profile


class ProfileCreateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'address', 'picture']


<<<<<<< HEAD
# class UserCreateForm(UserCreationForm):
    # email = forms.EmailField()

class UserCreateForm(forms.Form):
    username = forms.CharField()
    password1 = forms.CharField()
    password2 = forms.CharField()
    email = forms.EmailField()

    def clean_password2(self):
        data = self.cleaned_data
        if not data['password1'] == data['password2']:
            raise ValidationError('پسوردها با هم یکی نیستند')
        return data

=======
class UserCreateForm(UserCreationForm):
    email = forms.EmailField()

>>>>>>> ffdcd51 (Revert "13/1/2022-13:47 PM")

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'address', 'picture', ]


<<<<<<< HEAD
class UserEmailNameForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
=======
class EmailUserForm(forms.Form):
>>>>>>> ffdcd51 (Revert "13/1/2022-13:47 PM")
    email = forms.EmailField()


class UserAuthenticationLoginForm(forms.Form):
    username_or_email_login = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

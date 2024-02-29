from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from users.models import User


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class UserProfileForm(UserChangeForm):
    class Meta:
        model = User
        field = ('email', 'first_name', 'last_name', 'phone', 'avatar')


class ManagerForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('is_active',)

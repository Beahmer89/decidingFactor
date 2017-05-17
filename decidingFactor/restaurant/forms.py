from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from collections import OrderedDict


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=200, required=True)

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

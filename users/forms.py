# -*- coding:utf-8 -*-

from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import TaskUser


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)

    class Meta:
        model = TaskUser
        fields = [
            'first_name',
            'last_name',
            'username',
            'password1',
            'password2',
        ]

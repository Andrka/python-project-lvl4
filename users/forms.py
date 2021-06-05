# -*- coding:utf-8 -*-

from django.contrib.auth.forms import UserCreationForm

from .models import TaskUser


class RegisterForm(UserCreationForm):
    class Meta:
        model = TaskUser
        fields = [
            'first_name',
            'last_name',
            'username',
            'password1',
            'password2',
        ]

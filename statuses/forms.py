# -*- coding:utf-8 -*-

from django.forms import ModelForm
from django.utils.translation import gettext

from .models import Status


class StatusForm(ModelForm):
    class Meta:
        model = Status
        fields = ['name']
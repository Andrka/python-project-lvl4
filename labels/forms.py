# -*- coding:utf-8 -*-

from django.forms import ModelForm

from .models import Label


class LabelForm(ModelForm):
    class Meta:
        model = Label
        fields = ['name']

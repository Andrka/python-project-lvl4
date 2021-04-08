# -*- coding:utf-8 -*-

"""URL Configuration tasks."""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.root, name='root'),
]
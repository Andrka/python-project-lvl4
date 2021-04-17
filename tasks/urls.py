# -*- coding:utf-8 -*-

"""URL Configuration tasks."""

from django.urls import path

from .views import IndexPage

urlpatterns = [
    path('', IndexPage.as_view(), name='index'),
]

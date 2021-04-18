# -*- coding:utf-8 -*-

from django.urls import path

from .views import UserDeleteView, UserRegisterView, UsersView, UserUpdateView

urlpatterns = [
    path('', UsersView.as_view(), name='users'),
    path('create/', UserRegisterView.as_view(), name='register_user'),
    path('<int:pk>/update/', UserUpdateView.as_view(), name='update_user'),
    path('<int:pk>/delete/', UserDeleteView.as_view(), name='delete_user'),
]

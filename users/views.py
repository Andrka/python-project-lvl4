# -*- coding:utf-8 -*-

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from .forms import RegisterForm


class UserRegisterView(CreateView):
    form_class = RegisterForm
    success_url = reverse_lazy('login')
    template_name = 'users/register.html'


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    form_class = RegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')
    login_url = 'login'

    def test_func(self):
        obj = self.get_object()
        return obj == self.request.user
    
    def handle_no_permission(self):
        return redirect('users')


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = 'users/delete.html'
    success_url = reverse_lazy('index')
    login_url = 'login'

    def test_func(self):
        obj = self.get_object()
        return obj == self.request.user

    def handle_no_permission(self):
        return redirect('users')


class UsersView(ListView):
    model = User
    template_name = 'users/users.html'

    def get_queryset(self):
        return User.objects.all()


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    success_url = reverse_lazy('index')

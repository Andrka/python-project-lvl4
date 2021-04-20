# -*- coding:utf-8 -*-

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from .forms import RegisterForm


class UserRegisterView(SuccessMessageMixin, CreateView):
    form_class = RegisterForm
    success_url = reverse_lazy('login')
    template_name = 'users/register.html'
    success_message = 'Пользователь успешно зарегистрирован'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['headline'] = 'Регистрация'
        context['button_title'] = 'Зарегистрировать'
        return context


class UserUpdateView(
    SuccessMessageMixin,
    LoginRequiredMixin,
    UserPassesTestMixin,
    UpdateView,
):
    model = User
    form_class = RegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')
    login_url = 'login'
    success_message = 'Пользователь успешно изменён'
    message_need_login = 'Вы не авторизованы! Пожалуйста, выполните вход.'
    message_miss_rights = 'У вас нет прав для изменения другого пользователя.'

    def test_func(self):
        obj = self.get_object()
        return obj == self.request.user

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(self.request, self.message_miss_rights)
            return redirect('users')
        else:
            messages.error(self.request, self.message_need_login)
            return redirect('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['headline'] = 'Изменение пользователя'
        context['button_title'] = 'Изменить'
        return context


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = 'users/delete.html'
    success_url = reverse_lazy('index')
    login_url = 'login'
    success_message = 'Пользователь успешно удалён'
    message_need_login = 'Вы не авторизованы! Пожалуйста, выполните вход.'
    message_miss_rights = 'У вас нет прав для изменения другого пользователя.'

    def test_func(self):
        obj = self.get_object()
        return obj == self.request.user

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(self.request, self.message_miss_rights)
            return redirect('users')
        else:
            messages.error(self.request, self.message_need_login)
            return redirect('login')

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(UserDeleteView, self).delete(request, *args, **kwargs)


class UsersView(ListView):
    model = User
    template_name = 'users/users.html'

    def get_queryset(self):
        return User.objects.all().order_by('id')


class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = 'users/login.html'
    success_url = reverse_lazy('index')
    success_message = 'Вы залогинены'


class UserLogoutView(LogoutView):
    success_url = reverse_lazy('index')
    success_message = 'Вы разлогинены'

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.info(request, self.success_message)
        return response

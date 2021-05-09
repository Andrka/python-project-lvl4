# -*- coding:utf-8 -*-

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext
from django.views.generic import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from .forms import RegisterForm
from .models import TaskUser


class UserRegisterView(SuccessMessageMixin, CreateView):
    model = TaskUser
    form_class = RegisterForm
    success_url = reverse_lazy('login')
    template_name = 'users/register.html'
    success_message = gettext('Пользователь успешно зарегистрирован')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['headline'] = gettext('Регистрация')
        context['button_title'] = gettext('Зарегистрировать')
        return context


class UserUpdateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    SuccessMessageMixin,
    UpdateView,
):
    model = TaskUser
    form_class = RegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')
    login_url = 'login'
    success_message = gettext('Пользователь успешно изменён')
    message_need_login = gettext(
        'Вы не авторизованы! Пожалуйста, выполните вход.',
    )
    message_miss_rights = gettext(
        'У вас нет прав для изменения другого пользователя.',
    )

    def test_func(self):
        obj = self.get_object()
        return obj.id == self.request.user.id

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(self.request, self.message_miss_rights)
            return redirect('users')
        else:
            messages.error(self.request, self.message_need_login)
            return redirect('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['headline'] = gettext('Изменение пользователя')
        context['button_title'] = gettext('Изменить')
        return context


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = TaskUser
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users')
    login_url = 'users'
    success_message = gettext('Пользователь успешно удалён')
    message_need_login = gettext(
        'Вы не авторизованы! Пожалуйста, выполните вход.',
    )
    message_miss_rights = gettext(
        'У вас нет прав для изменения другого пользователя.',
    )
    error_message = gettext(
        'Невозможно удалить пользователя, потому что он используется',
    )

    def test_func(self):
        obj = self.get_object()
        return obj.id == self.request.user.id

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(self.request, self.message_miss_rights)
            return redirect('users')
        else:
            messages.error(self.request, self.message_need_login)
            return redirect('login')

    def delete(self, *args, **kwargs):
        obj = self.get_object()
        try:
            super(UserDeleteView, self).delete(self.request, *args, **kwargs)
        except (AttributeError, ProtectedError):
            messages.error(
                self.request,
                self.error_message % obj.__dict__,
            )
        else:
            messages.success(
                self.request,
                self.success_message % obj.__dict__,
            )
        return redirect(self.success_url)


class UsersView(ListView):
    model = TaskUser
    template_name = 'users/users.html'

    def get_queryset(self):
        return TaskUser.objects.all().order_by('id')


class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = 'users/login.html'
    success_url = reverse_lazy('index')
    success_message = gettext('Вы залогинены')


class UserLogoutView(LogoutView):
    success_url = reverse_lazy('index')
    success_message = gettext('Вы разлогинены')

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.info(request, self.success_message)
        return response

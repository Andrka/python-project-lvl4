# -*- coding:utf-8 -*-

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from django_filters.views import FilterView
from users.models import TaskUser

from .filters import TasksFilter
from .forms import TaskForm
from .models import Task


class TasksDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/detail.html'


class TasksView(LoginRequiredMixin, FilterView):
    model = Task
    template_name = 'tasks/tasks.html'
    login_url = 'login'
    filterset_class = TasksFilter


class TasksCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    login_url = 'login'
    success_url = reverse_lazy('tasks')
    template_name = 'tasks/create.html'
    success_message = gettext('Задача успешно создана')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['headline'] = gettext('Создать задачу')
        context['button_title'] = gettext('Создать')
        return context

    def form_valid(self, form):
        form.instance.creator = TaskUser.objects.get(id=self.request.user.id)
        return super().form_valid(form)


class TasksUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/create.html'
    login_url = 'login'
    success_url = reverse_lazy('tasks')
    success_message = gettext('Задача успешно изменена')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['headline'] = gettext('Изменение задачи')
        context['button_title'] = gettext('Изменить')
        return context


class TasksDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    template_name = 'tasks/delete.html'
    success_url = reverse_lazy('tasks')
    login_url = 'login'
    success_message = gettext('Задача успешно удалёна')
    message_need_login = gettext(
        'Вы не авторизованы! Пожалуйста, выполните вход.',
    )
    message_miss_rights = gettext(
        'Задачу может удалить только её автор',
    )

    def test_func(self):
        obj = self.get_object()
        return obj.id == self.request.user.id

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(self.request, self.message_miss_rights)
            return redirect('tasks')
        else:
            messages.error(self.request, self.message_need_login)
            return redirect('tasks')

    def delete(self, *args, **kwargs):
        obj = self.get_object()
        try:
            super(TasksDeleteView, self).delete(self.request, *args, **kwargs)
        except ProtectedError:
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

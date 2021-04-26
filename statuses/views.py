# -*- coding:utf-8 -*-

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext
from django.views.generic import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from .forms import StatusForm
from .models import Status


class StatusesView(LoginRequiredMixin, ListView):
    model = Status
    template_name = 'statuses/statuses.html'
    form_class = StatusForm
    login_url = 'login'

    def get_queryset(self):
        return Status.objects.all().order_by('id')


class StatusCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = StatusForm
    login_url = 'login'
    success_url = reverse_lazy('statuses')
    template_name = 'statuses/create.html'
    success_message = gettext('Статус успешно создан')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['headline'] = gettext('Создать статус')
        context['button_title'] = gettext('Создать')
        return context


class StatusUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/create.html'
    login_url = 'login'
    success_url = reverse_lazy('statuses')
    success_message = gettext('Статус успешно изменён')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['headline'] = gettext('Изменение статуса')
        context['button_title'] = gettext('Изменить')
        return context


class StatusDeleteView(LoginRequiredMixin, DeleteView):
    model = Status
    template_name = 'statuses/delete.html'
    login_url = 'login'
    success_url = reverse_lazy('statuses')
    success_message = gettext('Статус успешно удалён')
    error_message = gettext(
        'Невозможно удалить статус, потому что он используется',
    )

    def delete(self, *args, **kwargs):
        self.obj = self.get_object()
        try:
            super(StatusDeleteView, self).delete(self.request, *args, **kwargs)
        except ProtectedError:
            messages.error(self.request, self.error_message % self.obj.__dict__)
        else:
            messages.success(self.request, self.success_message % self.obj.__dict__)
        return redirect(self.success_url)

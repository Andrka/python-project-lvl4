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

from .forms import LabelForm
from .models import Label


class LabelsView(LoginRequiredMixin, ListView):
    model = Label
    template_name = 'labels/labels.html'
    form_class = LabelForm
    login_url = 'login'

    def get_queryset(self):
        return Label.objects.all().order_by('id')


class LabelCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Label
    form_class = LabelForm
    login_url = 'login'
    success_url = reverse_lazy('labels')
    template_name = 'labels/create.html'
    success_message = gettext('Метка успешно создана')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['headline'] = gettext('Создать метку')
        context['button_title'] = gettext('Создать')
        return context


class LabelUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/create.html'
    login_url = 'login'
    success_url = reverse_lazy('labels')
    success_message = gettext('Метка успешно изменена')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['headline'] = gettext('Изменение метки')
        context['button_title'] = gettext('Изменить')
        return context


class LabelDeleteView(LoginRequiredMixin, DeleteView):
    model = Label
    template_name = 'labels/delete.html'
    login_url = 'login'
    success_url = reverse_lazy('labels')
    success_message = gettext('Метка успешно удалена')
    error_message = gettext(
        'Невозможно удалить метку, потому что она используется',
    )

    def delete(self, *args, **kwargs):
        obj = self.get_object()
        try:
            super(LabelDeleteView, self).delete(self.request, *args, **kwargs)
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

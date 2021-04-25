# -*- coding:utf-8 -*-

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from .models import Status


class StatusesView(LoginRequiredMixin, ListView):
    model = Status
    template_name = 'statuses/statuses.html'

    def get_queryset(self):
        return Status.objects.all().order_by('id')


class StatusCreateView(LoginRequiredMixin, CreateView):
    pass


class StatusUpdateView(LoginRequiredMixin, UpdateView):
    pass


class StatusDeleteView(LoginRequiredMixin, DeleteView):
    pass

# -*- coding:utf-8 -*-

from django.forms import CheckboxInput
from django_filters import BooleanFilter, FilterSet

from .models import Task


class TasksFilter(FilterSet):
    self_task = BooleanFilter(
        method='filter_self_tasks',
        widget=CheckboxInput,
    )

    def filter_self_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(creator=self.request.user).order_by('id')
        return queryset.order_by('id')

    class Meta:
        model = Task
        fields = ['status', 'executor', 'label', 'self_task']
        filter_overrides = {
            BooleanFilter: {
                'filter_class': BooleanFilter,
                'extra': lambda f: {'widget': CheckboxInput},
            },
        }

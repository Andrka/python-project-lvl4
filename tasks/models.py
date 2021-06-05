# -*- coding:utf-8 -*-
from django.db import models
from django.db.models import Model
from django.utils.translation import gettext
from labels.models import Label
from statuses.models import Status
from users.models import TaskUser


class Task(Model):
    name = models.CharField(
        max_length=100,
        verbose_name=gettext('Имя'),
        help_text=gettext('Имя'),
    )
    description = models.TextField(
        max_length=500,
        blank=True,
        verbose_name=gettext('Описание'),
        help_text=gettext('Описание'),
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        null=True,
        verbose_name=gettext('Статус'),
    )
    executor = models.ForeignKey(
        TaskUser,
        on_delete=models.PROTECT,
        related_name="task_executor",
        null=True,
        blank=True,
        verbose_name=gettext('Исполнитель'),
    )
    creator = models.ForeignKey(
        TaskUser,
        on_delete=models.PROTECT,
        related_name='task_creator',
        null=True,
    )
    added_at = models.DateTimeField(auto_now_add=True)
    label = models.ManyToManyField(
        Label,
        through='LabelToTask',
        through_fields=('task', 'label'),
        blank=True,
        verbose_name=gettext('Метки'),
    )

    def __str__(self):
        return self.name


class LabelToTask(Model):
    task = models.ForeignKey(Task, on_delete=models.PROTECT)
    label = models.ForeignKey(Label, on_delete=models.PROTECT)

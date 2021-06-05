# -*- coding:utf-8 -*-

from django.db import models
from django.db.models import Model
from django.utils.translation import gettext


class Label(Model):
    name = models.CharField(
        max_length=100,
        verbose_name=gettext('Имя'),
        help_text=gettext('Имя'),
    )
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

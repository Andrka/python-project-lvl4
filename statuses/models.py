# -*- coding:utf-8 -*-

from django.db import models
from django.db.models import Model


class Status(Model):
    name = models.CharField(
        max_length=100,
    )
    added_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return self.name

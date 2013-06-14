# -*- coding: utf-8 -*-

from django.db import models
from djson_field.models import JSONField


class JSONModel(models.Model):
    title = models.CharField('Назва', max_length=255)
    json_field = JSONField('JSON field')

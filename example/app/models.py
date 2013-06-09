# -*- coding: utf-8 -*-

from django.db import models
from djson_field import JSONField

# Create your models here.

class JSONModel(models.Model):
    title = models.CharField('Назва', max_length=255)
    json_field = JSONField('JSON field')

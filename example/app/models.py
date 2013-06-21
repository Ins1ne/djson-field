# -*- coding: utf-8 -*-

from django.db import models
from django.forms import IntegerField
from djson_field.models import JSONField


def get_rules():
    return [
        (['key'], {
            'type': IntegerField(),
            'actions': ['add_plain'],
            'allow_item_removing': False
        }),
    ]


class JSONModel(models.Model):
    title = models.CharField('Назва', max_length=255)
    json_field = JSONField('JSON field', rules=get_rules)

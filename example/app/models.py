# -*- coding: utf-8 -*-

from django.db import models
from djson_field.models import JSONField
import re
_ = re.compile

def get_rules():
    return [
        (['key'], {
            'type': {
                'field1': models.IntegerField(),
                'field2': models.CharField(max_length=255)
            },
            'actions': ['add_plain'],
            'allow_item_removing': False
        }),
        (['key', _(r'.*')], {
            'type': models.CharField(max_length=255),
            'actions': [],
            'allow_item_removing': False
        }),
    ]


class JSONModel(models.Model):
    title = models.CharField('Назва', max_length=255)
    json_field = JSONField('JSON field', rules=get_rules)

# -*- coding: utf-8 -*-
from django.forms import CharField
from djson_field.widgets import JSONWidget


class JsonField(CharField):

    def __init__(self, *args, **kwargs):
        kwargs['widget'] = JSONWidget(rules=kwargs.get('rules', []))
        if 'rules' in kwargs:
            del kwargs['rules']
        return super(JsonField, self).__init__(*args, **kwargs)

# -*- coding: utf-8 -*-
from django.forms import CharField
from djson_field.widgets import JSONWidget


class JsonField(CharField):

    def __init__(self, **kwargs):
        kwargs['widget'] = JSONWidget()
        return super(JsonField, self).__init__(**kwargs)

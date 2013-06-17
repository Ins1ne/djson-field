# -*- coding: utf-8 -*-

from django.db import models
from django.forms import CharField
from djson_field.forms import JsonField

import re
_ = re.compile


class JSONField(models.TextField):
    """ Stores and loads valid JSON objects. """

    description = 'JSON object'
    BASE_RULES = [
        ([], {
            'type': CharField(),
            'actions': ['add_plain'],
            'allow_item_removing': False
        }),
    ]

    def __init__(self, *args, **kwargs):
        self.rules = self.BASE_RULES
        if 'rules' in kwargs:
            self.rules += kwargs['rules']
            del kwargs['rules']
        super(JSONField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'form_class': JsonField}
        defaults['rules'] = self.rules
        defaults.update(kwargs)
        return super(JSONField, self).formfield(**defaults)

    def validate(self, value, *args, **kwargs):
        super(JSONField, self).validate(*args, **kwargs)

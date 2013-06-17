# -*- coding: utf-8 -*-

from django.db import models
from django.forms import CharField, IntegerField
from djson_field.forms import JsonField

import json
import re
_ = re.compile


class JSONField(models.TextField):
    """ Stores and loads valid JSON objects. """

    description = 'JSON object'
    BASE_RULES = [
        (['key'], {
            'type': IntegerField(),
            'actions': ['add_plain'],
            'allow_item_removing': False
        }),
    ]

    def __init__(self, *args, **kwargs):
        self.rules = self.BASE_RULES
        if 'rules' in kwargs:
            add_rules = kwargs['rules']
            if hasattr(add_rules, '__call__'):
                self.rules += add_rules()
            else:
                self.rules += add_rules
            del kwargs['rules']
        super(JSONField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'form_class': JsonField}
        defaults['rules'] = self.rules
        defaults.update(kwargs)
        return super(JSONField, self).formfield(**defaults)

    def validate_item(self, item, model_instance, path):
        errors = []
        if isinstance(item, dict):
            for key, subitem in item.iteritems():
                errors += self.validate_item(subitem, model_instance, path + [key])
        elif isinstance(item, list):
            for subitem in item:
                errors += self.validate_item(subitem, model_instance, path)
        else:
            field = self.formfield()
        return errors
        

    def validate(self, value, model_instance):
        item = json.loads(value)
        errors = self.validate_item(item, model_instance)
        super(JSONField, self).validate(value, model_instance)

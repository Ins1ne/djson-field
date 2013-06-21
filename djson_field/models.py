# -*- coding: utf-8 -*-

from django.core.exceptions import ValidationError
from django.db import models
from django.forms import CharField
from djson_field.forms import JsonField

import json
import re
import string
_ = re.compile


class JSONField(models.TextField):
    """ Stores and loads valid JSON objects. """

    description = 'JSON object'
    BASE_RULES = [
        ([_(r'.*')], {
            'type': CharField(),
            'actions': ['add_plain', 'add_list', 'add_dict'],
            'allow_item_removing': True
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

    def validate_item(self, item, model_instance, path=[]):
        errors = []
        if isinstance(item, dict):
            for key, subitem in item.iteritems():
                errors += self.validate_item(subitem, model_instance,
                                             path + [key])
        elif isinstance(item, list):
            for i, subitem in enumerate(item):
                errors += self.validate_item(subitem, model_instance,
                                             path + [i])
        else:
            field = self.formfield()
            rules = field.widget.get_rules(path)
            field_type = rules['type']
            try:
                field_type.clean(item)
            except ValidationError as e:
                for msg in e.messages:
                    errors.append(string.join(path, "->") + ": " + msg)
        return errors

    def clean(self, value, model_instance):
        cleaned_data = super(JSONField, self).clean(value, model_instance)
        item = json.loads(value)
        errors = self.validate_item(item, model_instance)
        if len(errors) > 0:
            raise ValidationError(errors)
        return cleaned_data

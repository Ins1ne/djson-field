# -*- coding: utf-8 -*-

from django.db import models
from djson_field.forms import JsonField


class JSONField(models.TextField):
    """ Stores and loads valid JSON objects. """

    description = 'JSON object'

    def __init__(self, *args, **kwargs):
        super(JSONField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'form_class': JsonField}
        defaults.update(kwargs)
        return super(JSONField, self).formfield(**defaults)

    def validate(self, value, *args, **kwargs):
        super(JSONField, self).validate(*args, **kwargs)

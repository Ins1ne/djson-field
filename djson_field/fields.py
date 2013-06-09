# -*- coding: utf-8 -*-

from django.db import models


class JSONField(models.TextField):
    """ Stores and loads valid JSON objects. """

    description = 'JSON object'

    def __init__(self, *args, **kwargs):
        super(JSONField, self).__init__(*args, **kwargs)

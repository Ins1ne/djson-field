# -*- coding: utf-8 -*-

from django.db import models
from djson_field.models import JSONField
import re
_ = re.compile


def get_rules():
    return [
        ([], {
            "allow_removing": False,
            "verbose_name": None,
            "help_text": None,
            "hidden": False,
        }),
        (["key"], {
            "actions": ["add_dict", "add_plain", "add_list"],
        }),
        (["key", _(r".*")], {
            "type": {
                "field1": models.IntegerField(),
                "field2": models.CharField(max_length=255)
            },
            "actions": ["add_plain", "add_dict"],
            "allow_item_removing": False
        }),
        (["key", _(r".*"), _(r".*")], {
            "type": models.CharField(max_length=255),
            "actions": [],
            "allow_item_removing": False
        }),
    ]


def get_initial():
    return {
        "key": {
            "1": 1,
            "2": 2
        }
    }


def get_initial2():
    return {
        "key1": "key1 default value",
        "key2": "key2 default value",
        "key3": ["key3.1 default value", "key3.2 default value"],
        "key4": {
            "key4.1": "key4.1 default value",
            "key4.2": "key4.2 default value"
        }
    }


class JSONModel(models.Model):
    title = models.CharField(u"Title", max_length=255)
    simple_json_field = JSONField(u"JSON field", rules=get_rules, initial=get_initial)
    masked_json_field = JSONField(u"Masked field", initial=get_initial2, is_masked=True)

    def __unicode__(self):
        return self.title

# -*- coding: utf-8 -*-

from app.models import JSONModel
from django import forms
from djson_field import JSONWidget

import re


class JSONModelAdminForm(forms.ModelForm):
    """
    Admin form for JSONModel
    """
    class Meta:
        model = JSONModel
        widgets = {
            'json_field': JSONWidget(rules=[
                ([r"key3"], {
                    'actions': ['add_plain', 'add_list'],
                    'type': forms.ChoiceField(choices=[(0, u"value3.1"), (1, u"value3.2"), (2, u"value3.3"), (3, u"value3.4")]),
                    'allow_removing': True
                }),
                (["key3", re.compile(".*")], {
                    'type': forms.ChoiceField(choices=[(0, u"value3.1"), (1, u"value3.2"), (2, u"value3.3"), (3, u"value3.4")]),
                    'actions': []
                })
            ])
        }

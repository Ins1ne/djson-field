# -*- coding: utf-8 -*-

from app.models import JSONModel
from django import forms
from djson_field import JSONWidget


class JSONModelAdminForm(forms.ModelForm):
    """
    Admin form for JSONModel
    """
    class Meta:
        model = JSONModel
        widgets = {
            'json_field': JSONWidget
        }

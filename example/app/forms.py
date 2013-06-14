# -*- coding: utf-8 -*-

from app.models import JSONModel
from django import forms


class JSONModelAdminForm(forms.ModelForm):
    """
    Admin form for JSONModel
    """

    def __init__(self, *args, **kwargs):
        super(JSONModelAdminForm, self).__init__(*args, **kwargs)

    class Meta:
        model = JSONModel

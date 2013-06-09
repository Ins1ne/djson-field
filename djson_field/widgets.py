# -*- coding: utf-8 -*-
from django.template.loader import render_to_string
from django.forms.widgets import Textarea


class JSONWidget(Textarea):
    def __init__(self, rules=None, **kwargs):
        super(JSONWidget, self).__init__(**kwargs)

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        import pdb;pdb.set_trace()
        return render_to_string('djson_field/djson_widget.html', {
            'final_attrs': final_attrs,
            'value': value
        })

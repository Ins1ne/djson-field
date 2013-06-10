# -*- coding: utf-8 -*-
from django.forms.widgets import Textarea
from django.utils.safestring import mark_safe

import json
import re


def update_tree(tree, path, value):
    if len(path) > 0:
        if path[0].isdigit() and (not tree or type(tree) == list):
            if not tree:
                tree = []
            index = int(path[0])
            while len(tree) <= index:
                tree.append(None)
        else:
            if not tree:
                tree = {}
            index = path[0]
            if index not in tree:
                tree[index] = None
        if len(path) == 1:
            tree[index] = value
        else:
            tree[index] = update_tree(tree[index], path[1:], value)
    return tree


class JSONWidget(Textarea):
    def __init__(self, rules=None, **kwargs):
        super(JSONWidget, self).__init__(**kwargs)

    def render_data(self, name, data):
        html = u""
        if type(data) == dict:
            for key, value in data.iteritems():
                field_name = "%s[%s]" % (name, key)
                label = u'<label for="id_%s">%s</label>' % (field_name, key)
                field = self.render_data(field_name, value)
                html += u"<li>" + label + field + u"</li>"
            html = u"<ul>" + html + u"</ul>"
        elif type(data) == list:
            for i in xrange(len(data)):
                html += u"<li>" + self.render_data("%s[%i]" % (name, i), data[i])
            html = u"<ol>" + html + u"</ol>"
        else:
            html = u'<input id="id_%(name)s" name="%(name)s" value="%(value)s" />' % {
                'name': name,
                'value': unicode(data)
            }
        return mark_safe(html)

    def render(self, name, value, attrs=None):
        json_dict = {}
        if value and len(value) > 0:
            json_dict = json.loads(value)
        return self.render_data(name, json_dict)

    def value_from_datadict(self, data, files, name):
        value = {}
        for key, val in data.iteritems():
            if key.startswith(name + "["):
                branch_keys = re.findall(r'\[([A-Za-z0-9_.]*)\]', key)
                value = update_tree(value, branch_keys, val)
        return json.dumps(value)

    class Media:
        css = {
            'all': ('css/djson_field.css',)
        }
        js = ('js/jquery.js', 'js/djson_field.js')

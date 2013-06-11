# -*- coding: utf-8 -*-
from django.forms import fields
from django.forms.widgets import Textarea
from django.template.loader import render_to_string

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
            if index.startswith("_"):
                index = index[1:]
            if index not in tree:
                tree[index] = None
        if len(path) == 1:
            tree[index] = value
        else:
            tree[index] = update_tree(tree[index], path[1:], value)
    return tree


def remove_empty_items(tree):
    if type(tree) == list:
        return [remove_empty_items(ob) for ob in tree if ob is not None]
    elif type(tree) == dict:
        for key, value in tree.iteritems():
            tree[key] = remove_empty_items(value)
    return tree


class JSONWidget(Textarea):
    def __init__(self, rules=None, **kwargs):
        rules = rules or []
        self.rules = [
            ([r".*"], {
                'type': fields.CharField()
            }),
            ([r"key3", r".*"], {
                'type': fields.IntegerField()
            })
        ] + rules
        super(JSONWidget, self).__init__(**kwargs)

    def add_links_template(self):
        separator = " | "
        added_links = {
            "plain": u'<a class="plain" href="#">простое значение</a>',
            "list": u'<a class="list" href="#">список</a>',
            "dict": u'<a class="dict" href="#">словарь</a>',
        }
        add_link = u'<li class="jsonFieldAddLink">Добавить: '
        for i, link in enumerate(added_links.values()):
            add_link += link
            if i < len(added_links) - 1:
                add_link += separator
        add_link += u'</li>'
        return add_link

    def render_dict(self, name, data):
        items = {}
        for key, value in data.iteritems():
            items[key] = self.render_data("%s[%s]" % (name, "_" + key), value)
        return render_to_string("djson_field/dictionary_item.html", {
            'name': name,
            'items': items,
            'controls': self.add_links_template()
        })

    def render_list(self, name, data):
        items = []
        for i in xrange(len(data)):
            items.append(self.render_data("%s[%i]" % (name, i), data[i]))
        return render_to_string("djson_field/list_item.html", {
            'name': name,
            'items': items,
            'controls': self.add_links_template()
        })

    def render_plain(self, name, data):
        return render_to_string("djson_field/plain_item.html", {
            'name': name,
            'value': unicode(data)
        })

    def render_data(self, name, data):
        if type(data) == dict:
            return self.render_dict(name, data)
        elif type(data) == list:
            return self.render_list(name, data)
        else:
            return self.render_plain(name, data)

    def render(self, name, value, attrs=None):
        json_dict = {}
        if value and len(value) > 0:
            json_dict = json.loads(value)
        html = self.render_data(name, json_dict)
        templates = {
            'dict': self.render_dict('%%NAME%%', {}),
            'list': self.render_list('%%NAME%%', []),
            'plain': self.render_plain('%%NAME%%', u"")
        }
        return render_to_string("djson_field/base.html", {
            'content': html,
            'templates': templates
        })

    def value_from_datadict(self, data, files, name):
        value = {}
        for key, val in data.iteritems():
            if key.startswith(name + "["):
                branch_keys = re.findall(r'\[([A-Za-z0-9_.]*)\]', key)
                value = update_tree(value, branch_keys, val)
        value = remove_empty_items(value)
        return json.dumps(value)

    class Media:
        css = {
            'all': ('css/djson_field.css',)
        }
        js = ('js/jquery.js', 'js/djson_field.js')

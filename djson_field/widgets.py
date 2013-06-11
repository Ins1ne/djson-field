# -*- coding: utf-8 -*-
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

    def render_data(self, name, data):
        html = u""

        if type(data) == dict:
            items = {}
            for key, value in data.iteritems():
                items[key] = self.render_data("%s[%s]" % (name, "_" + key), value)
            html = render_to_string("djson_field/dictionary_item.html", {
                'name': name,
                'items': items,
                'controls': self.add_links_template()
            })
        elif type(data) == list:
            items = []
            for i in xrange(len(data)):
                items.append(self.render_data("%s[%i]" % (name, i), data[i]))
            html = render_to_string("djson_field/list_item.html", {
                'name': name,
                'items': items,
                'controls': self.add_links_template()
            })
        else:
            html = render_to_string("djson_field/plain_item.html", {
                'name': name,
                'value': unicode(data)
            })
        return html

    def render(self, name, value, attrs=None):
        json_dict = {}
        if value and len(value) > 0:
            json_dict = json.loads(value)
        html = self.render_data(name, json_dict)
        templates = {
            'dict': render_to_string("djson_field/dictionary_item.html", {
                'name': '%%NAME%%',
                'items': {},
                'controls': self.add_links_template()
            }),
            'list': render_to_string("djson_field/list_item.html", {
                'name': '%%NAME%%',
                'items': [],
                'controls': self.add_links_template()
            }),
            'plain': render_to_string("djson_field/plain_item.html", {
                'name': '%%NAME%%',
                'value': ""
            })
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

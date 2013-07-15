# -*- coding: utf-8 -*-
from collections import OrderedDict
from django.forms.widgets import Textarea
from django.template.loader import render_to_string

import json
import string
import re


def update_tree(tree, path, value):
    if len(path) > 0:
        is_add = value not in ["__KEEP_LIST__", "__KEEP_DICT__"]
        if path[0].startswith("_"):
            if not tree:
                tree = {}
            if is_add or len(path) > 1:
                index = path[0][1:]
                tree[index] = None
        else:
            if not tree:
                tree = []
            if is_add or len(path) > 1:
                index = int(path[0])
                while len(tree) <= index:
                    tree.append(None)
        if len(path) == 1:
            if is_add:
                tree[index] = value
        else:
            tree[index] = update_tree(tree[index], path[1:], value)
    return tree


def parse_name(name):
    nodes = []
    node = u""
    is_start = False
    for char in name:
        if char == "[":
            is_start = True
        elif char == "]":
            nodes.append(node)
            node = u""
            is_start = False
        elif is_start:
            node += char
    return nodes


def get_name_by_path(base, path):
    return base + string.join(["[%s]" % ob for ob in path], '')


def remove_empty_items(tree):
    if type(tree) == list:
        return [remove_empty_items(ob) for ob in tree if ob is not None]
    elif type(tree) == dict:
        for key, value in tree.iteritems():
            tree[key] = remove_empty_items(value)
    return tree


def is_satisfy_selectors(selectors, path):
    if len(selectors) == 0:
        return True
    if len(path) == 0:
        return False
    for i in xrange(1, len(path) + 1):
        if type(selectors[-1]) in [unicode, str, int, long]:
            condition = selectors[-1] == path[-i]
        else:
            node = path[-i]
            if type(node) in [int, long]:
                node = str(node)
            match = re.match(selectors[-1], node)
            condition = match and match.end() == len(node)
        if condition:
            return is_satisfy_selectors(selectors[:-1], path[:-i])
    return False


class JSONWidget(Textarea):

    ADD_ACTIONS = {
        "add_plain": u"простое значение",
        "add_list": u"список",
        "add_dict": u"словарь",
    }

    def __init__(self, rules=[], *args, **kwargs):
        self.rules = rules
        super(JSONWidget, self).__init__(*args, **kwargs)

    def add_links_template(self, rules):
        actions = rules.get('actions', [])
        link_actions = [ob for ob in actions if ob in self.ADD_ACTIONS]
        links = {key: value for key, value in self.ADD_ACTIONS.iteritems()
                 if key in link_actions}
        if len(link_actions) > 0:
            return render_to_string("djson_field/add_links.html", {
                'links': links,
            })
        return ""

    def get_rules(self, path):
        rules = {}
        if len(path) > 0:
            for selectors, _rules in self.rules[::-1]:
                if is_satisfy_selectors(selectors, path):
                    for key, rule in _rules.iteritems():
                        if key not in rules:
                            rules[key] = rule
        else:
            return self.rules[0][1]
        return rules

    def get_templates(self, path):
        return {
            'dict': self.render_dict('%%NAME%%', path=path,
                                     with_templates=False),
            'list': self.render_list('%%NAME%%', path=path,
                                     with_templates=False),
            'plain': self.render_plain('%%NAME%%', path=path,
                                       with_templates=False)
        }

    def render_dict(self, name, data={}, path=[], rules=None,
                    with_templates=True, with_name=False, field_key=None):
        rules = rules or self.get_rules(path)
        items = {}
        for key, value in data.iteritems():
            _ = self.get_rules(path + [key])
            if not _.get('hidden'):
                _field_key = rules['type_key'] and\
                    rules['type_key'].formfield().widget.render("field_key",
                                                                key)
                items[key] = self.render_data("%s[%s]" % (name, "_" + key),
                                              value, path + [key], with_templates=with_templates, with_name=True,
                                              rules=_, field_key=_field_key)
        return render_to_string("djson_field/dictionary_item.html", {
            'field_key': field_key,
            'with_name': with_name,
            'name': name,
            'key': path[-1] if len(path) > 0 else None,
            'items': items,
            'controls': self.add_links_template(rules),
            'templates': with_templates and self.get_templates(path),
            'rules': rules
        })

    def render_list(self, name, data=[], path=[], rules=None,
                    with_templates=True, with_name=False, field_key=None):
        rules = rules or self.get_rules(path)
        items = []
        for i in xrange(len(data)):
            items.append(self.render_data("%s[%i]" % (name, i), data[i], path, with_templates=with_templates))
        return render_to_string("djson_field/list_item.html", {
            'field_key': field_key,
            'with_name': with_name,
            'name': name,
            'items': items,
            'key': path[-1] if len(path) > 0 else None,
            'controls': self.add_links_template(rules),
            'templates': with_templates and self.get_templates(path),
            'rules': rules
        })

    def render_plain(self, name, data=u"", path=[], rules=None, with_templates=True, with_name=False, field_key=None):
        rules = rules or self.get_rules(path)
        field = rules['type'].formfield().widget.render(name, unicode(data))
        if not with_templates:
            field = field.replace('name="%%NAME%%"', '_name="%%NAME%%"')
        match = re.match(r'<[a-zA-Z0-9._]+\s+', field)
        if match:
            field = field[:match.end()] + ' class="jsonFieldItemValue" ' +\
                field[match.end():]
        return render_to_string("djson_field/plain_item.html", {
            'field_key': field_key,
            'with_name': with_name,
            'name': name,
            'key': path[-1] if len(path) > 0 else name,
            'field': field,
            'value': unicode(data),
            'rules': rules,
        })

    def render_data(self, name, data, path=[], with_templates=True):
        rules = self.get_rules(path)
        key = path[-1] if len(path) > 0 else None
        field_name = get_name_by_path(name, path)
        field = rules['type'].formfield().widget.render(field_name, unicode(data))
        match = re.match(r'<[a-zA-Z0-9._]+\s+', field)
        if match:
            field = field[:match.end()] + ' class="jsonFieldItemValue" ' + field[match.end():]
        field_key = rules['type_key'] and rules['type_key'].formfield().widget.render("__%s" % field_name, key)
        match = re.match(r'<[a-zA-Z0-9._]+\s+', field_key)
        if match:
            field_key = field_key[:match.end()] + ' class="jsonFieldItemKey" ' + field_key[match.end():]
        params = {
            'field': field,
            'field_key': field_key,
            'name': field_name,
            'key': key if not isinstance(key, int) else None,
            'controls': self.add_links_template(rules),
            'rules': rules,
            'templates': with_templates and self.get_templates(path + (isinstance(key, int) and [0] or ['']))
        }
        if isinstance(data, dict):
            params['items'] = OrderedDict(
                [(key, self.render_data(name, ob, path + [key])) for key, ob in data.iteritems()])
            template = "djson_field/dictionary_item.html"
        elif isinstance(data, list):
            params['items'] = ((None, self.render_data(name, ob, path + [i])) for i, ob in enumerate(data))
            template = "djson_field/list_item.html"
        else:
            params['value'] = data
            template = "djson_field/plain_item.html"
        return render_to_string(template, params)

    def render(self, name, value, attrs=None):
        json_dict = {}
        if value and len(value) > 0:
            json_dict = json.loads(value)
        json_dict = OrderedDict([
            ('a', 1),
            ('b', [2, 3, 4]),
            ('c', {"c.1": 5, "c.2": 6})
        ])
        html = self.render_data(name, json_dict)
        return render_to_string("djson_field/base.html", {
            'content': html
        })

    def value_from_datadict(self, data, files, name):
        value = {}
        for key, val in data.iteritems():
            if key.startswith(name + "["):
                branch_keys = parse_name(key)
                value = update_tree(value, branch_keys, val)
        value = remove_empty_items(value)
        return json.dumps(value)

    class Media:
        css = {
            'all': ('css/djson_field.css',)
        }
        js = ('js/jquery.js', 'js/djson_field.js')

# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'JSONModel'
        db.create_table('app_jsonmodel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('default_field', self.gf('django.db.models.fields.TextField')()),
            ('plain_field', self.gf('django.db.models.fields.TextField')()),
            ('list_field', self.gf('django.db.models.fields.TextField')()),
            ('dict_field', self.gf('django.db.models.fields.TextField')()),
            ('complex_field', self.gf('django.db.models.fields.TextField')()),
            ('masked_json_field', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('app', ['JSONModel'])


    def backwards(self, orm):
        # Deleting model 'JSONModel'
        db.delete_table('app_jsonmodel')


    models = {
        'app.jsonmodel': {
            'Meta': {'object_name': 'JSONModel'},
            'complex_field': ('django.db.models.fields.TextField', [], {}),
            'default_field': ('django.db.models.fields.TextField', [], {}),
            'dict_field': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'list_field': ('django.db.models.fields.TextField', [], {}),
            'masked_json_field': ('django.db.models.fields.TextField', [], {}),
            'plain_field': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['app']
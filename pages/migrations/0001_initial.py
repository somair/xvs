# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Link'
        db.create_table('pages_link', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('href', self.gf('django.db.models.fields.URLField')(max_length=400)),
        ))
        db.send_create_signal('pages', ['Link'])


    def backwards(self, orm):
        # Deleting model 'Link'
        db.delete_table('pages_link')


    models = {
        'pages.link': {
            'Meta': {'object_name': 'Link'},
            'href': ('django.db.models.fields.URLField', [], {'max_length': '400'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['pages']
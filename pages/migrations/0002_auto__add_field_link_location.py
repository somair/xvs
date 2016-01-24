# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Link.location'
        db.add_column('pages_link', 'location',
                      self.gf('django.db.models.fields.CharField')(default='header', max_length=30),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Link.location'
        db.delete_column('pages_link', 'location')


    models = {
        'pages.link': {
            'Meta': {'object_name': 'Link'},
            'href': ('django.db.models.fields.URLField', [], {'max_length': '400'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'default': "'header'", 'max_length': '30'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['pages']
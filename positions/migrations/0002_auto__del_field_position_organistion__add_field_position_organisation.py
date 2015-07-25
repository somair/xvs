# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):

        db.rename_column('positions_position', 'organistion_id', 'organisation_id')
        
    def backwards(self, orm):
        
        db.rename_column('positions_position', 'organisation_id', 'organistion_id')

    models = {
        'positions.organisation': {
            'Meta': {'object_name': 'Organisation'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '31'})
        },
        'positions.position': {
            'Meta': {'object_name': 'Position'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'hours': ('weekgrid.WeekgridField', [], {'max_length': '127'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '63'}),
            'organisation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['positions.Organisation']"})
        }
    }

    complete_apps = ['positions']

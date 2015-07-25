# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Organisation'
        db.create_table('positions_organisation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=31)),
        ))
        db.send_create_signal('positions', ['Organisation'])

        # Adding model 'Position'
        db.create_table('positions_position', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('organistion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['positions.Organisation'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=63)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('hours', self.gf('weekgrid.WeekgridField')(max_length=127)),
        ))
        db.send_create_signal('positions', ['Position'])


    def backwards(self, orm):
        
        # Deleting model 'Organisation'
        db.delete_table('positions_organisation')

        # Deleting model 'Position'
        db.delete_table('positions_position')


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
            'organistion': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['positions.Organisation']"})
        }
    }

    complete_apps = ['positions']

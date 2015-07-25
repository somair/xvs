# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Position.oneoff'
        db.add_column('positions_position', 'oneoff', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'Position.date_start'
        db.add_column('positions_position', 'date_start', self.gf('django.db.models.fields.DateField')(null=True, blank=True), keep_default=False)

        # Adding field 'Position.date_end'
        db.add_column('positions_position', 'date_end', self.gf('django.db.models.fields.DateField')(null=True, blank=True), keep_default=False)

        # Changing field 'Position.hours'
        db.alter_column('positions_position', 'hours', self.gf('volunteering.weekgrid.WeekgridField')(max_length=127))


    def backwards(self, orm):
        
        # Deleting field 'Position.oneoff'
        db.delete_column('positions_position', 'oneoff')

        # Deleting field 'Position.date_start'
        db.delete_column('positions_position', 'date_start')

        # Deleting field 'Position.date_end'
        db.delete_column('positions_position', 'date_end')

        # Changing field 'Position.hours'
        db.alter_column('positions_position', 'hours', self.gf('weekgrid.WeekgridField')(max_length=127))


    models = {
        'positions.organisation': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Organisation'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '31'})
        },
        'positions.position': {
            'Meta': {'object_name': 'Position'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'date_end': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_start': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'hours': ('volunteering.weekgrid.WeekgridField', [], {'max_length': '127'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '63'}),
            'oneoff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'organisation': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'positions'", 'to': "orm['positions.Organisation']"})
        }
    }

    complete_apps = ['positions']

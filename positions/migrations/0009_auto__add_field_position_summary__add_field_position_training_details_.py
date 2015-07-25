# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Position.summary'
        db.add_column('positions_position', 'summary', self.gf('django.db.models.fields.CharField')(default='', max_length=140), keep_default=False)

        # Adding field 'Position.training_details'
        db.add_column('positions_position', 'training_details', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Position.spec_essential'
        db.add_column('positions_position', 'spec_essential', self.gf('django.db.models.fields.CharField')(default='', max_length=140), keep_default=False)

        # Adding field 'Position.spec_desirable'
        db.add_column('positions_position', 'spec_desirable', self.gf('django.db.models.fields.CharField')(default='', max_length=140), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Position.summary'
        db.delete_column('positions_position', 'summary')

        # Deleting field 'Position.training_details'
        db.delete_column('positions_position', 'training_details')

        # Deleting field 'Position.spec_essential'
        db.delete_column('positions_position', 'spec_essential')

        # Deleting field 'Position.spec_desirable'
        db.delete_column('positions_position', 'spec_desirable')


    models = {
        'positions.organisation': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Organisation'},
            'charity_number': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'directions': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '31'}),
            'purpose': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'positions.position': {
            'Meta': {'object_name': 'Position'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'date_end': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_start': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'hours': ('volunteering.weekgrid.WeekgridField', [], {'max_length': '127'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keywords': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'location': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '63'}),
            'oneoff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'organisation': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'positions'", 'to': "orm['positions.Organisation']"}),
            'skills_gained': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['positions.Skill']", 'symmetrical': 'False'}),
            'spec_desirable': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'spec_essential': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'training_details': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'training_provided': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'positions.skill': {
            'Meta': {'object_name': 'Skill'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '31'})
        }
    }

    complete_apps = ['positions']

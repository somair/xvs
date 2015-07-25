# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Organisation.charity_number'
        db.add_column('positions_organisation', 'charity_number', self.gf('django.db.models.fields.CharField')(default='', max_length=15, blank=True), keep_default=False)

        # Adding field 'Organisation.purpose'
        db.add_column('positions_organisation', 'purpose', self.gf('django.db.models.fields.TextField')(default='', blank=True), keep_default=False)

        # Adding field 'Organisation.address'
        db.add_column('positions_organisation', 'address', self.gf('django.db.models.fields.TextField')(default='', blank=True), keep_default=False)

        # Adding field 'Organisation.website'
        db.add_column('positions_organisation', 'website', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True), keep_default=False)

        # Adding field 'Organisation.directions'
        db.add_column('positions_organisation', 'directions', self.gf('django.db.models.fields.TextField')(default='', blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Organisation.charity_number'
        db.delete_column('positions_organisation', 'charity_number')

        # Deleting field 'Organisation.purpose'
        db.delete_column('positions_organisation', 'purpose')

        # Deleting field 'Organisation.address'
        db.delete_column('positions_organisation', 'address')

        # Deleting field 'Organisation.website'
        db.delete_column('positions_organisation', 'website')

        # Deleting field 'Organisation.directions'
        db.delete_column('positions_organisation', 'directions')


    models = {
        'positions.organisation': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Organisation'},
            'address': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'charity_number': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'directions': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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

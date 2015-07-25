# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Skill'
        db.create_table('positions_skill', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=31)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('positions', ['Skill'])

        # Adding field 'Position.location'
        db.add_column('positions_position', 'location', self.gf('django.db.models.fields.TextField')(default='Potterrow, EUSA'), keep_default=False)

        # Adding field 'Position.training_provided'
        db.add_column('positions_position', 'training_provided', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding M2M table for field skills_gained on 'Position'
        db.create_table('positions_position_skills_gained', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('position', models.ForeignKey(orm['positions.position'], null=False)),
            ('skill', models.ForeignKey(orm['positions.skill'], null=False))
        ))
        db.create_unique('positions_position_skills_gained', ['position_id', 'skill_id'])

        # Changing field 'Position.description'
        db.alter_column('positions_position', 'description', self.gf('django.db.models.fields.TextField')())


    def backwards(self, orm):
        
        # Deleting model 'Skill'
        db.delete_table('positions_skill')

        # Deleting field 'Position.location'
        db.delete_column('positions_position', 'location')

        # Deleting field 'Position.training_provided'
        db.delete_column('positions_position', 'training_provided')

        # Removing M2M table for field skills_gained on 'Position'
        db.delete_table('positions_position_skills_gained')

        # Changing field 'Position.description'
        db.alter_column('positions_position', 'description', self.gf('django.db.models.fields.TextField')(null=True))


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
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '31'})
        }
    }

    complete_apps = ['positions']

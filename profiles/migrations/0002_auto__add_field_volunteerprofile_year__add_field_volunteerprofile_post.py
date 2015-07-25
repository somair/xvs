# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'VolunteerProfile.year'
        db.add_column('profiles_volunteerprofile', 'year', self.gf('django.db.models.fields.PositiveIntegerField')(default=1), keep_default=False)

        # Adding field 'VolunteerProfile.postgrad'
        db.add_column('profiles_volunteerprofile', 'postgrad', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'VolunteerProfile.international'
        db.add_column('profiles_volunteerprofile', 'international', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'VolunteerProfile.address'
        db.add_column('profiles_volunteerprofile', 'address', self.gf('django.db.models.fields.TextField')(default=''), keep_default=False)

        # Adding field 'VolunteerProfile.phone_number'
        db.add_column('profiles_volunteerprofile', 'phone_number', self.gf('django.db.models.fields.CharField')(default='', max_length=31), keep_default=False)

        # Adding field 'VolunteerProfile.gender'
        db.add_column('profiles_volunteerprofile', 'gender', self.gf('django.db.models.fields.CharField')(default='U', max_length=1), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'VolunteerProfile.year'
        db.delete_column('profiles_volunteerprofile', 'year')

        # Deleting field 'VolunteerProfile.postgrad'
        db.delete_column('profiles_volunteerprofile', 'postgrad')

        # Deleting field 'VolunteerProfile.international'
        db.delete_column('profiles_volunteerprofile', 'international')

        # Deleting field 'VolunteerProfile.address'
        db.delete_column('profiles_volunteerprofile', 'address')

        # Deleting field 'VolunteerProfile.phone_number'
        db.delete_column('profiles_volunteerprofile', 'phone_number')

        # Deleting field 'VolunteerProfile.gender'
        db.delete_column('profiles_volunteerprofile', 'gender')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'positions.organisation': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Organisation'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '31'})
        },
        'profiles.baseprofile': {
            'Meta': {'object_name': 'BaseProfile'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_representative': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_volunteer': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'profiles.representativeprofile': {
            'Meta': {'object_name': 'RepresentativeProfile'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job_title': ('django.db.models.fields.CharField', [], {'max_length': '63'}),
            'organisation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['positions.Organisation']"}),
            'profile': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['profiles.BaseProfile']", 'unique': 'True'})
        },
        'profiles.volunteerprofile': {
            'Meta': {'object_name': 'VolunteerProfile'},
            'address': ('django.db.models.fields.TextField', [], {}),
            'bio': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'course': ('django.db.models.fields.CharField', [], {'max_length': '63'}),
            'gender': ('django.db.models.fields.CharField', [], {'default': "'U'", 'max_length': '1'}),
            'hours': ('weekgrid.WeekgridField', [], {'max_length': '127'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'international': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '31'}),
            'postgrad': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'profile': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['profiles.BaseProfile']", 'unique': 'True'}),
            'year': ('django.db.models.fields.PositiveIntegerField', [], {})
        }
    }

    complete_apps = ['profiles']

# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing M2M table for field training_required on 'Award'
        db.delete_table(db.shorten_name('profiles_award_training_required'))

        # Adding M2M table for field training_required on 'AwardType'
        m2m_table_name = db.shorten_name('profiles_awardtype_training_required')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('awardtype', models.ForeignKey(orm['profiles.awardtype'], null=False)),
            ('training', models.ForeignKey(orm['training.training'], null=False))
        ))
        db.create_unique(m2m_table_name, ['awardtype_id', 'training_id'])


    def backwards(self, orm):
        # Adding M2M table for field training_required on 'Award'
        m2m_table_name = db.shorten_name('profiles_award_training_required')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('award', models.ForeignKey(orm['profiles.award'], null=False)),
            ('training', models.ForeignKey(orm['training.training'], null=False))
        ))
        db.create_unique(m2m_table_name, ['award_id', 'training_id'])

        # Removing M2M table for field training_required on 'AwardType'
        db.delete_table(db.shorten_name('profiles_awardtype_training_required'))


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
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['positions.OrganisationCategory']", 'null': 'True', 'blank': 'True'}),
            'charity_number': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'department': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['profiles.Department']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'directions': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '127'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '31', 'blank': 'True'}),
            'primary_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'purpose': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'volunteer_policy': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'positions.organisationcategory': {
            'Meta': {'ordering': "('name',)", 'object_name': 'OrganisationCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'positions.positioncategory': {
            'Meta': {'ordering': "('name',)", 'object_name': 'PositionCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'positions.skill': {
            'Meta': {'object_name': 'Skill'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '31'})
        },
        'profiles.award': {
            'Meta': {'object_name': 'Award'},
            'award': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['profiles.AwardType']"}),
            'date_awarded': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'profiles.awardtype': {
            'Meta': {'object_name': 'AwardType'},
            'hours_required': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'plus': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'training_required': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['training.Training']", 'symmetrical': 'False'})
        },
        'profiles.baseprofile': {
            'Meta': {'object_name': 'BaseProfile'},
            'archived': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'communication': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'department': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['profiles.Department']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_representative': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_volunteer': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slas': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['profiles.ServiceLevelAgreement']", 'symmetrical': 'False', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'profiles.course': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Course'},
            'faculty': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['profiles.Faculty']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'profiles.department': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Department'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'profiles.faculty': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Faculty'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'profiles.howdidyouhear': {
            'Meta': {'object_name': 'HowDidYouHear'},
            'how': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'profiles.representativeprofile': {
            'Meta': {'object_name': 'RepresentativeProfile'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job_title': ('django.db.models.fields.CharField', [], {'max_length': '63'}),
            'organisation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['positions.Organisation']"}),
            'profile': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['profiles.BaseProfile']", 'unique': 'True'})
        },
        'profiles.servicelevelagreement': {
            'Meta': {'ordering': "('order',)", 'object_name': 'ServiceLevelAgreement'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'preferred_answer': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'statement': ('django.db.models.fields.TextField', [], {})
        },
        'profiles.volunteerprofile': {
            'Meta': {'object_name': 'VolunteerProfile'},
            'address': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'bio': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['positions.PositionCategory']", 'null': 'True', 'blank': 'True'}),
            'contact_email': ('django.db.models.fields.EmailField', [], {'max_length': '127', 'null': 'True', 'blank': 'True'}),
            'course': ('django.db.models.fields.CharField', [], {'max_length': '63'}),
            'cv': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'hours': ('weekgrid.WeekgridField', [], {'max_length': '127'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'international': ('django.db.models.fields.CharField', [], {'default': "'H'", 'max_length': '1'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '31'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'postgrad': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'profile': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['profiles.BaseProfile']", 'unique': 'True'}),
            'referencefile': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'referrer': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'school': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '127', 'blank': 'True'}),
            'student_id': ('django.db.models.fields.CharField', [], {'max_length': '31', 'null': 'True', 'blank': 'True'}),
            'year': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'training.training': {
            'Meta': {'object_name': 'Training'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'skills': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['positions.Skill']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        }
    }

    complete_apps = ['profiles']
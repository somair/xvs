# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Certification'
        db.create_table('work_experience_certification', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('work_experience', ['Certification'])

        # Adding model 'VolunteerSkill'
        db.create_table('work_experience_volunteerskill', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('work_experience', ['VolunteerSkill'])

        # Adding model 'WorkExperience'
        db.create_table('work_experience_workexperience', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('volunteer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['profiles.VolunteerProfile'])),
            ('role', self.gf('django.db.models.fields.CharField')(max_length=511)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('hours', self.gf('django.db.models.fields.FloatField')()),
            ('reference_email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('confirmation_code', self.gf('django.db.models.fields.CharField')(default='e91337f3-1ca7-4149-b4b8-b527cabcf6fd', max_length=255)),
        ))
        db.send_create_signal('work_experience', ['WorkExperience'])

        # Adding M2M table for field skills on 'WorkExperience'
        m2m_table_name = db.shorten_name('work_experience_workexperience_skills')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('workexperience', models.ForeignKey(orm['work_experience.workexperience'], null=False)),
            ('volunteerskill', models.ForeignKey(orm['work_experience.volunteerskill'], null=False))
        ))
        db.create_unique(m2m_table_name, ['workexperience_id', 'volunteerskill_id'])

        # Adding M2M table for field certifications on 'WorkExperience'
        m2m_table_name = db.shorten_name('work_experience_workexperience_certifications')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('workexperience', models.ForeignKey(orm['work_experience.workexperience'], null=False)),
            ('certification', models.ForeignKey(orm['work_experience.certification'], null=False))
        ))
        db.create_unique(m2m_table_name, ['workexperience_id', 'certification_id'])


    def backwards(self, orm):
        # Deleting model 'Certification'
        db.delete_table('work_experience_certification')

        # Deleting model 'VolunteerSkill'
        db.delete_table('work_experience_volunteerskill')

        # Deleting model 'WorkExperience'
        db.delete_table('work_experience_workexperience')

        # Removing M2M table for field skills on 'WorkExperience'
        db.delete_table(db.shorten_name('work_experience_workexperience_skills'))

        # Removing M2M table for field certifications on 'WorkExperience'
        db.delete_table(db.shorten_name('work_experience_workexperience_certifications'))


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
        'positions.positioncategory': {
            'Meta': {'ordering': "('name',)", 'object_name': 'PositionCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
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
        'profiles.department': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Department'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
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
        'work_experience.certification': {
            'Meta': {'object_name': 'Certification'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'work_experience.volunteerskill': {
            'Meta': {'object_name': 'VolunteerSkill'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'work_experience.workexperience': {
            'Meta': {'object_name': 'WorkExperience'},
            'certifications': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['work_experience.Certification']", 'symmetrical': 'False'}),
            'confirmation_code': ('django.db.models.fields.CharField', [], {'default': "'e91337f3-1ca7-4149-b4b8-b527cabcf6fd'", 'max_length': '255'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'hours': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reference_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '511'}),
            'skills': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['work_experience.VolunteerSkill']", 'symmetrical': 'False'}),
            'volunteer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['profiles.VolunteerProfile']"})
        }
    }

    complete_apps = ['work_experience']
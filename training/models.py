from django.db import models
from django.contrib.auth.models import User

class Training(models.Model):
	title = models.CharField(max_length=250)
	description = models.TextField()
	skills = models.ManyToManyField('positions.Skill')

	def __unicode__(self):
		return u'%s' % self.title

class Event(models.Model):
	training = models.ForeignKey(Training)
	date_time = models.DateTimeField()
	location = models.TextField()

	def __unicode__(self):
		return u'%s - %s' % (self.training.title, self.date_time)

class Attendee(models.Model):
	event = models.ForeignKey(Event)
	user = models.ForeignKey(User)
	date_time = models.DateTimeField(auto_now_add=True)
	confirmed = models.BooleanField(default=False)
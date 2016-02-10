from django.db import models
from profiles.models import VolunteerProfile

from uuid import uuid4


 
class Certification(models.Model):
	name = models.CharField(max_length=255)

	def __str__(self):
		return self.name


class VolunteerSkill(models.Model):
	name = models.CharField(max_length=255)

	def __str__(self):
		return self.name

def make_new_uuid():
	return str(uuid4())

class WorkExperience(models.Model):

	volunteer_profile = models.ForeignKey(VolunteerProfile)
	role = models.CharField(max_length=511)
	description = models.TextField()
	hours = models.FloatField(verbose_name="Hours per week")
	skills = models.ManyToManyField(VolunteerSkill, null=True, blank=True)
	certifications = models.ManyToManyField(Certification, null=True, blank=True)
	reference_email = models.EmailField()
	confirmation_code = models.CharField(max_length=255, editable=False, default=make_new_uuid)
	confirmed = models.BooleanField(default=False)

	def __str__(self):
		return "%s %s" % (self.volunteer_profile.profile.user.username, self.role) 





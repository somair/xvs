from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings

from profiles import models

def send_email(awarded):
	super_users = User.objects.filter(is_staff=True)
	emails = [u.email for u in super_users]
		
	if awarded:
		content = 'The following awards were issued automatically.\n\n'
		for award in awarded:
			content += '%s %s - %s (%s)\n' % (award[0], award[1], award[2], award[3])
	else:
		content = "No new awards were issued automatically today."

	send_mail('Awards Issued', content, settings.SERVER_EMAIL, emails, fail_silently=False)

class Command(BaseCommand):

	help = 'Pulls AwardTypes and then works out who should have which awards.'

	def handle(self, *args, **options):
		if settings.FEATURE_AWARD:

			awarded = list()
			award_types = models.AwardType.objects.all()
			volunteer_list = User.objects.filter(baseprofile__is_volunteer=True)

			for v in volunteer_list:
				print 'Checking: %s' % v.username
				timerecords = v.timerecord_set.all()

				minutes = 0
				for tr in timerecords:
					minutes += (60*tr.hours + tr.minutes) 
				
				hours = int(minutes/60)
	   			minutes = minutes%60

	   			training_list = set(attendee.event.training for attendee in v.attendee_set.all() if attendee.confirmed)

	   			for award in award_types:
	   				if hours > award.hours_required:

	   					if settings.FEATURE_TRAINING_EVENT:

	   						training_required = set(training for training in award.training_required.all())

	   						if training_required.issubset(training_list):
		   						print '%s: %s' % (v.username, award.name)
			   					a, created = models.Award.objects.get_or_create(award=award, user=v)
			   					if created:
			   						awarded.append([v.first_name, v.last_name, award, hours])
			   					else:
			   						print 'This award already existed.'

			   				else:

			   					print 'Volunteer has not attended required training.'

	   					else:

		   					print '%s: %s' % (v.username, award.name)
		   					a, created = models.Award.objects.get_or_create(award=award, user=v)
		   					if created:
		   						awarded.append([v.first_name, v.last_name, award, hours])
		   					else:
		   						print 'This award already existed.'

	   		send_email(awarded=awarded)
	   	else:
	   		print 'The award feature is disabled.'
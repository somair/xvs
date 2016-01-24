from django.core.mail import send_mail
from django.conf import settings

import models

def add_skills(work_experience_item, skill_list):
	''' Updates the skills attached to a work experience item '''

	work_experience_item.skills.clear()
	for skill in skill_list:
		try:
			skill_object = models.VolunteerSkill.objects.get(name='skill')
		except:
			skill_object = models.VolunteerSkill(name=skill)
			skill_object.save()
		work_experience_item.skills.add(skill_object)
	work_experience_item.save()
	return work_experience_item

def send_referral_email(work_experience_item, request):
	subject = 'Work experience - Confirmation required'
	message = '''
		Hi, \n %s %s (%s) has recently added the following work experience to our volunteer registration system:

		- Role: %s \n
		- Description: %s \n 
		- Hours per week: %s \n
		%s would like you to verify these details by visiting this link: http://%s/work_experience/confirm/%s \n

		Thanks, \n %s
	''' % (
		work_experience_item.volunteer_profile.profile.user.first_name,
		work_experience_item.volunteer_profile.profile.user.last_name,
		work_experience_item.volunteer_profile.profile.user.email,
		work_experience_item.role,
		work_experience_item.description,
		work_experience_item.hours,
		work_experience_item.volunteer_profile.profile.user.first_name,
		request.META.get('HTTP_HOST'),
		work_experience_item.confirmation_code,
		settings.INSTANCE_NAME,
		)

	recipient_list = [work_experience_item.reference_email]
	return send_mail(subject = subject, message = message, from_email=None, recipient_list = recipient_list, fail_silently=False)


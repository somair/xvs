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

def send_confirmation_email(work_experience_item):
	#TODO:All
	pass

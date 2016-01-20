from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from decorators import is_volunteer

from work_experience import models, forms, logic

from pprint import pprint 

@is_volunteer
def work_experience(request, we_id=None):
	'''Allows a volunteer to add, edit, browse and delete his work experience items'''

	if we_id:
		work_experience_item = models.WorkExperience.objects.get(pk=we_id)
		view='edit'
	else:
		work_experience_item = None
		view='new'

	form = forms.WorkExperienceForm(instance=work_experience_item)
	volunteer = request.user.get_profile().try_get_volunteer_profile()
	print volunteer.pk
	recorded_experiences = models.WorkExperience.objects.filter(volunteer=volunteer.id)

	if request.POST:
		pprint (request.POST)
		form = forms.WorkExperienceForm(request.POST)
		if form.is_valid():
			new_work_experience = form.save(commit=False)
			new_work_experience.volunteer = volunteer
			new_work_experience.save()
			if request.POST.getlist('tags'):
				new_work_experience = logic.add_skills(new_work_experience, request.POST.getlist('tags'))


	template = 'work_experience/new.html'

	context = {
		'form': form,
		'view':view,
		'recorded_experiences': recorded_experiences,
	}

	return render(request, template, context)


@is_volunteer
def work_experience_delete(request, we_id=None):
	'''Deletes a work_experience_record'''

	work_experience_item = models.WorkExperience.objects.get(pk=we_id)
	volunteer = request.user.get_profile().try_get_volunteer_profile()
	if work_experience_item.volunteer == volunteer:
		work_experience_item.delete()

	return redirect(request, 'we_dashboard')




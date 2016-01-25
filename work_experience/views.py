from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib import messages
from decorators import is_volunteer, representative_or_staff

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
		view = 'new'

	form = forms.WorkExperienceForm(instance=work_experience_item)
	volunteer = request.user.get_profile().try_get_volunteer_profile()

	recorded_experiences = models.WorkExperience.objects.filter(volunteer_profile=volunteer)

	if request.POST:

		form = forms.WorkExperienceForm(request.POST)
		if form.is_valid():
			new_work_experience = form.save(commit=False)
			new_work_experience.volunteer_profile = volunteer
			new_work_experience.save()
			if request.POST.getlist('tags'):
				new_work_experience = logic.add_skills(new_work_experience, request.POST.getlist('tags'))
				send_email = logic.send_referral_email(new_work_experience, request)
				messages.info(request, "New work experience record added")
				return redirect(reverse('work_experience'))


	template = 'work_experience/new.html'

	context = {
		'form': form,
		'view':view,
		'recorded_experiences': recorded_experiences,
	}

	return render(request, template, context)


@is_volunteer
def work_experience_delete(request, we_id=None):
	'''Deletes a work experience record'''

	work_experience_item = models.WorkExperience.objects.get(pk=we_id)
	volunteer_profile = request.user.get_profile().try_get_volunteer_profile()
	if work_experience_item.volunteer_profile == volunteer_profile:
		work_experience_item.delete()
	else:
		raise Http404()

	return redirect(reverse('work_experience'))

def work_experience_confirm(request, confirmation_code):
	'''Work experience record is confirmed by the referrer through the confirmation code sent'''

	work_experience_item = get_object_or_404(models.WorkExperience, confirmation_code = confirmation_code)
	work_experience_item.confirmed = True
	work_experience_item.save()

	messages.info(request, 'Thank you for your confirmation')

	return redirect('/')

@representative_or_staff
def report(request):

	work_experience_items = models.WorkExperience.objects.all().order_by('-pk')

	template = 'work_experience/report.html'

	context = {
		'work_experience_items': work_experience_items,
	}

	return render(request, template, context)





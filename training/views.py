from training import models, forms

from mailer import models as mailer_models

from decorators import staff_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib import messages

from datetime import datetime, timedelta

@login_required
def index(request):
	'''Training index page. Lists events and links to add them'''

	template = 'training/index.html'
	context = {
		'events': models.Event.objects.filter(date_time__gte=datetime.now()),
		'user_events': models.Attendee.objects.filter(user=request.user).order_by('event__date_time')
	}

	return render(request, template, context)

@login_required
def view(request, event_id):
	'''Displayes info on one event'''

	event = get_object_or_404(models.Event, pk=event_id, date_time__gte=datetime.now())
	attendee_check = models.Attendee.objects.filter(event=event, user=request.user)

	template = 'training/view.html'
	context = {
		'event': event,
		'attendee_check': attendee_check,
	}

	return render(request, template, context)

@login_required
def attend(request, event_id):
	'''Adds the current user as an attendee to the given event'''

	event = get_object_or_404(models.Event, pk=event_id, date_time__gte=datetime.now())
	attendee = models.Attendee(event=event, user=request.user)
	attendee.save()

	return redirect(reverse('training_view', kwargs={'event_id': event_id}))

@login_required
def withdraw(request, event_id):
	'''Drops the user from attendance sheet for this event, only if more than 24hrs before the event, notifies staff'''

	event = get_object_or_404(models.Event, pk=event_id)
	attendee = get_object_or_404(models.Attendee, event=event, user=request.user)

	tf_hours = datetime.now() + timedelta(hours=24)

	if tf_hours < event.date_time:
		attendee.delete()
		messages.add_message(request, messages.INFO, 'You have been withdrawn from this event.')
	else:
		messages.add_message(request, messages.INFO, 'This event is within the next 24 hours. You cannot withdraw.')

	return redirect(reverse('training_view', kwargs={'event_id': event_id}))

@staff_required
def admin(request):
	'''Simple admin page for training module'''

	template = 'training/admin/index.html'
	context = {
		'future_events': models.Event.objects.filter(date_time__gte=datetime.now()).order_by('-date_time'),
		'past_events': models.Event.objects.filter(date_time__lt=datetime.now()).order_by('date_time'),
		'training': models.Training.objects.all()
	}

	return render(request, template, context)

@staff_required
def new_training(request, training_id=None):
	'''Staff can add a new training module'''

	if training_id:
		training = get_object_or_404(models.Training, pk=training_id)
		form = forms.TrainingForm(instance=training)
	else:
		training = None
		form = forms.TrainingForm()

	if request.POST:
		if training_id:
			form = forms.TrainingForm(request.POST, instance=training)
		else:
			form = forms.TrainingForm(request.POST)

		if form.is_valid():
			form.save()

		if training_id:
			messages.add_message(request, messages.INFO, 'Scheme updated.')
		else:
			messages.add_message(request, messages.INFO, 'Scheme added.')

		return redirect(reverse('training_admin'))


	template = 'training/admin/new_training.html'
	context = {
		'form': form,
		'training': training,
	}

	return render(request, template, context)

@staff_required
def new_event(request, event_id=None):
	'''Staff can add a new event'''

	if event_id:
		event = get_object_or_404(models.Event, pk=event_id)
		form = forms.EventForm(instance=event)
	else:
		event = None
		form = forms.EventForm()

	if request.POST:
		if event_id:
			form =  forms.EventForm(request.POST, instance=event)
		else:
			form = forms.EventForm(request.POST)

		if form.is_valid():
			form.save()

			if event_id:
				messages.add_message(request, messages.INFO, 'Event updated.')
			else:
				messages.add_message(request, messages.INFO, 'Event added.')

			return redirect(reverse('training_admin'))

	template = 'training/admin/new_event.html'
	context = {
		'form': form,
		'event': event,
	}

	return render(request, template, context)

@staff_required
def delete_event(request, event_id):
	'''Staff can delete an existing event'''

	event = get_object_or_404(models.Event, pk=event_id)
	event.delete()

	return redirect(reverse('training_admin')) 

@staff_required
def attendance_register(request, event_id):
	'''Staff can view a register of those signed up to an event'''

	event = get_object_or_404(models.Event, pk=event_id)

	template = 'training/admin/register.html'
	context = {
		'event': event,
	}

	return render(request, template, context)

@staff_required
def confirm_attendance(request, event_id, attendee_id):
	'''Staff can confirm an attendee was at an event'''

	attendee = get_object_or_404(models.Attendee, pk=attendee_id, event__pk=event_id)

	attendee.confirmed = True
	attendee.save()

	return redirect(reverse('event_register', kwargs={'event_id': event_id}))

@staff_required
def remove_attendance(request, event_id, attendee_id):
	'''Marks attendance as false'''

	attendee = get_object_or_404(models.Attendee, pk=attendee_id, event__pk=event_id)

	attendee.confirmed = False
	attendee.save()

	return redirect(reverse('event_register', kwargs={'event_id': event_id}))

@staff_required
def non_attendee_contact(request, event_id):
	'''Staff can contact all of the people who did not attend the event'''
	event = get_object_or_404(models.Event, pk=event_id)

	new_mailout = mailer_models.Mailout(subject='%s - Event Attendance' % event.training.title , created_by=request.user)
	new_mailout.save()

	non_attendees = models.Attendee.objects.filter(event=event, confirmed=False)

	for r in non_attendees:
		new_recipient = mailer_models.Recipient(mailout=new_mailout, user=r.user)
		new_recipient.save()

	return redirect(reverse('mailout-detail', kwargs={'mailout_id': new_mailout.pk}))

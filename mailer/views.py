import datetime

from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

from lib.json import JsonResponse

from decorators import staff_required, representative_or_staff

import logic
import forms
from models import Mailout, Recipient

from positions.models import Organisation

@representative_or_staff
def mailouts(request, organisation_id=None):
  if not request.user.is_staff:
    organisation_id = request.user.get_profile().representativeprofile.organisation.id

  filter = request.GET.get('filter', "all")

  if filter == "all":
    mailouts = Mailout.objects.all()
  elif filter == "unsent":
    mailouts = Mailout.objects.filter(sent__isnull=True)

  organisation = None
  if organisation_id:
    mailouts = mailouts.filter(organisation=organisation_id)
    organisation = Organisation.objects.get(pk=organisation_id)

  return render_to_response("mailouts/mailouts.html", {
    'mailouts': mailouts,
    'organisation': organisation,
    'filter': filter,
    }, context_instance=RequestContext(request))

@representative_or_staff
def user_autocomplete(request):
  organisation_id = None
  if not request.user.is_staff:
    organisation_id = request.user.get_profile().representativeprofile.organisation.id

  query = request.REQUEST["term"]

  first_name_users = User.objects.filter(first_name__icontains=query)
  last_name_users = User.objects.filter(last_name__icontains=query)
  email_users = User.objects.filter(email__icontains=query)

  all_users = last_name_users | first_name_users | email_users

  if organisation_id:
      all_users = all_users.filter(commitment__organisation__id=organisation_id)

  all_users = all_users.distinct()[:20]

  return JsonResponse([
    {"label": u.get_full_name() + " <" + u.email + ">", "value": u.id}
    for u in all_users
    ])

@representative_or_staff
def new(request):
  mailout = logic.new([], request.user)
  return redirect(mailout)

@representative_or_staff
def copy(request, mailout_id):
  mailout = Mailout.objects.get(pk=mailout_id)

  if request.user.is_staff:
    pass
  elif request.user.get_profile().representativeprofile.organisation == mailout.organisation:
    pass
  else:
    raise Exception("You don't have permission to copy this mailer.")

  pk = logic.copy(mailout, request.user)
  return redirect('mailer.views.mailout', mailout_id=pk)

@representative_or_staff
def mailout(request, mailout_id):
  mailout = get_object_or_404(Mailout, pk=mailout_id)

  if request.method == "POST":
    if "delete" in request.POST:
      if mailout.sent:
        messages.info(request, "Cannot delete a mailout that has already been sent.")
      else:
        mailout.delete()
        messages.info(request, "Mailout deleted.")
        return redirect("/mailouts/")
    elif "send" in request.POST:
      # Don't save changes in the form.
      form = forms.MailoutForm(instance=mailout)
      if mailout.sent:
        messages.info(request, "Mailout could not be sent because it has already been sent. This could happen if you accidentally click 'send' twice.")
      else:
        logic.send(mailout, request)
        mailout.sent = datetime.datetime.now()
        mailout.sent_by = request.user
        mailout.save()
        messages.info(request, "Your mailout has been dispatched.")
    elif "save" in request.POST:
      form = forms.MailoutForm(request.POST)
      if mailout.sent:
        messages.info(request, "Mailout could not be saved because it has already been sent.")
      elif form.is_valid():
        mailout.subject = form.cleaned_data['subject']
        mailout.body = form.cleaned_data['body']
        mailout.save()
        form = forms.MailoutForm(instance=mailout)
        messages.info(request, "Mailout updated. Check the preview and, if the mailout is ready, click 'send' below the preview to dispatch the mailout.")
      else:
        messages.info(request, "There is a problem with your mailout. Check the error messages below and try again.")
    elif "delete_recipient" in request.POST:
      form = forms.MailoutForm(instance=mailout)
      if mailout.sent:
        messages.info(request, "Cannot delete recipient once mailout has been sent.")
      else:
        recipient = get_object_or_404(Recipient, pk=int(request.POST['recipient_id']))
        recipient.delete()
        messages.info(request, "%s removed from recipient list" % recipient.user.get_full_name())
    elif "new_recipient" in request.POST:
      form = forms.MailoutForm(instance=mailout)
      if mailout.sent:
        messages.info(request, "Cannot add recipient once mailout has been sent.")
      else:
        user = get_object_or_404(User, pk=int(request.POST['recipient_id']))
        recipient = Recipient(user=user, mailout=mailout)
        recipient.save()
        messages.info(request, user.get_full_name() + " added to the recipient list.")
    else:
      form = forms.MailoutForm(request.POST, instance=mailout)
      messages.info(request, "Unrecognised action!")
  else:
    form = forms.MailoutForm(instance=mailout)

  return render_to_response("mailouts/mailout.html", {
    'mailout': mailout,
    'form': form,
    }, context_instance=RequestContext(request))
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.contrib import messages
from django.template import RequestContext

import settings

from profiles.models import BaseProfile
from models import Mailout, Recipient

from positions.models import Organisation

def new(users, user, organisation_id=None):
    """Make and return a new mailout to be sent to the given list of users."""

    if not user.is_staff:
        organisation_id = user.get_profile().representativeprofile.organisation.id

    organisation = None
    if organisation_id:
        organisation = Organisation.objects.get(pk=organisation_id)

    mailout = Mailout(created_by=user, organisation=organisation)
    mailout.save()

    for u in users:
        r = Recipient(user=u)
        r.mailout = mailout
        r.save()

    return mailout

def send(mailout, request):
    subject = mailout.full_subject()
    body = mailout.full_body()

    text_body = strip_tags(body)

    for r in mailout.recipient_set.all():
        base_profile = BaseProfile.objects.get(user=r.user)

        if base_profile.communication:
            msg = EmailMultiAlternatives(subject, text_body, settings.SERVER_EMAIL, [r.user.email])
            msg.attach_alternative(body, "text/html")
            msg.send()
        else:
            recipient = Recipient.objects.get(mailout=mailout, user=r.user)
            recipient.delete()
            messages.info(request, "Message not sent to: %s, the user is unsubscribed." % r.user.email)

def copy(mailout, user):
    recipients = mailout.recipient_set.all()

    new_mailout = Mailout(subject=mailout.subject, body=mailout.body, organisation=mailout.organisation, created_by=user)
    new_mailout.save()
    for r in recipients:
        new_recipient = Recipient(mailout=new_mailout, user=r.user)
        new_recipient.save()

    return new_mailout.pk

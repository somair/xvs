import datetime

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.template.loader import render_to_string

import email_helpers
import settings

from hours.models import Commitment

from models import OfferLogEntry
from profiles.models import BaseProfile

class Action(object):
    class NotPermitted(Exception):
        pass

    @classmethod
    def name(cls):
        return cls.__name__.lower()

    def do_action(self, user, reason):
        self.check_permissions(user)
        self._act(user, reason)

    def check_permissions(self, user):
        if not self.is_permitted(user):
            raise Action.NotPermitted("The current user is not allowed to perform this action.")

    def email(self, users, subject, message):
        if not isinstance(users, list):
            users = [users]
        
        # Strip whitespace from each line of the message.
        message = "\n".join([line.strip() for line in message.strip().splitlines()])

        # Insert the base URL
        current_site = Site.objects.get(id=settings.SITE_ID)
        message = message.replace("{{ HOME_PAGE }}", settings.HOME_PAGE)
        
        # This is the default instruction.
        staff_email_instruction = "email the volunteering admin staff"
        if settings.STAFF_EMAIL:
            # If settings.py includes a staff email address we can customise
            # the staff email instruction with it.  
            staff_email_instruction = "email %s" % settings.STAFF_EMAIL
        message = message.replace("{{ STAFF_EMAIL_INSTRUCTION }}", staff_email_instruction)

        for user in users:
            body = render_to_string('layout/action_email.txt', {
                    'instance': email_helpers.instance_dictionary(),
                    'recipient': user,
                    'message': message,
            })

            user_email = user.email
            try:
                if user.get_profile().is_volunteer and user.get_profile().volunteerprofile.contact_email:
                    user_email = user.get_profile().volunteerprofile.contact_email
            except BaseProfile.DoesNotExist:
                pass

            send_mail("[Volunteering] %s" % subject, body, settings.SERVER_EMAIL, [user_email], fail_silently=True)

class OfferAction(Action):
    
    def __init__(self, offer):
        self.offer = offer

    def log(self, user, reason):
        OfferLogEntry(
            user=user,
            offer=self.offer,
            reason=reason,
            action=self.name()
            ).save()

class PositionAction(Action):
    def __init__(self, position):
        self.position = position

class PendingAction(object):
    def __init__(self, subject):
        self.subject = subject

# Actions

VOLUNTEER_OFFER_MESSAGE = """
    A volunteer has offered to fill an opportunity in your organisation.
    
    View the volunteer's application by logging into the Volunteering website at:
    
    {{ HOME_PAGE }}
"""

VOLUNTEER_ACCEPTED_MESSAGE = """
    Thanks for your interest in %s. The organisation has sent the following welcome message:
    
    ===
    %s
    ===    

    You can contact the organisation representative at %s
"""

class ApproveNewPosition(PositionAction):
    """Staff approve a new position created by an organisation representative."""
    log_message = "approved position advert"
    option_text = "Approve this position advert."
    reason_reason = None
    short_action = "Approve"

    def is_permitted(self, user):
        return user.is_staff

    def _act(self, user, reason):
        self.position.approved = True
        self.position.save()

    def response(self):
        return 'The position has been approved and is now open for applications.'

class EmailRepresentative(PositionAction):
    """Staff email the representative with regards to the position."""
    log_message = "emailed the organisation representative about the position"
    option_text = "Email the organisation representative regarding this position."
    reason_reason = "Enter the message you'd like to send to the organisation regarding this position below."
    short_action = "Send Email"

    def is_permitted(self, user):
        return user.is_staff

    def _act(self, user, reason):
        #reps = [rp.profile.user for rp in self.position.organisation.representativeprofile_set.all()]
        self.email(self.position.representative, "Your advert on Volunteering", """
            You recently added an advert to the volunteering website, but it cannot be approved yet. The reason is shown below.

            ===
            %s
            ===
           
            To edit the position, visit the Volunteering website at {{ HOME_PAGE }}, click "view my current adverts", and then select the advert under the "unapproved" heading. Click "edit position" in the box at the bottom of the position summary. If you have any questions, {{ STAFF_EMAIL_INSTRUCTION }}
 
            {{ HOME_PAGE }}
            """ % reason)

    def response(self):
        return 'The organisation representative has been emailed.'

class RequestPosition(OfferAction):
    """A volunteer requests a position with an organisation."""
    log_message = "applied for the position"

    def is_permitted(self, user):
        # Check user is a volunteer
        return user.get_profile().try_get_volunteer_profile() != None

    def _act(self, user, reason):
        self.offer.time_volunteer_accepted=datetime.datetime.now()
        self.offer.volunteer = user
        self.offer.save()
        self.log(user, reason)
        
    def response(self):
        return 'Thanks! We have sent your details to the organisation, who should contact you within 5 working days. Let us know if you don\'t hear from them in this timescale.'

class SuggestPosition(OfferAction):
    """A staff member suggests a position to a volunteer."""
    log_message = "recommended the position"

    def is_permitted(self, user):
        return user.is_staff

    def _act(self, user, reason):
        self.offer.time_staff_accepted=datetime.datetime.now()
        self.offer.staff = user
        self.offer.save()
        self.log(user, "")
        self.email(self.offer.volunteer, "Opportunity recommendation", """
            A position has been recommended to you by the volunteering staff.
            
            Find out more information about the position by logging into the Volunteering website at:
            
            {{ HOME_PAGE }}
        """)

    def response(self):
        return 'A recommendation for "%s" at %s has been sent to %s.' % (self.offer.position.name, self.offer.position.organisation.name, self.offer.volunteer.get_full_name(),)

    def response_plural(self, count):
        return 'A recommendation for "%s" at %s has been sent to %d volunteers.' % (self.offer.position.name, self.offer.position.organisation.name, count)


class AgreeSuggestedPosition(OfferAction):
    """A volunteer agrees to a position suggested by staff."""
    log_message = "agreed to the position"
    option_text = "Looks good! I'd like to apply for this opportunity."
    reason_reason = "Introduce yourself in the box below. Say a bit about why you've applied, and why you'd be good for the position." if settings.FEATURE_COVER_LETTER else None
    short_action = "Apply Now"

    def is_permitted(self, user):
        return user == self.offer.volunteer

    def _act(self, user, reason):
        self.offer.time_volunteer_accepted = datetime.datetime.now()
        self.offer.save()
        self.log(user, reason)

        reps = self.offer.position.representative
        if settings.NOTIFY_ALL_REPS:
            reps = [rp.profile.user for rp in self.offer.position.organisation.representativeprofile_set.all()]
        
        self.email(reps, "Volunteer request", VOLUNTEER_OFFER_MESSAGE)

    def response(self):
        return "You have agreed to this opportunity and your application has been forwarded to the organisation."

class DeclineSuggestedPosition(OfferAction):
    """A volunteer declines a position suggested by staff."""
    log_message = "declined the position"
    option_text = "No thanks."
    reason_reason = "Enter your reason for declining the opportunity below. You don't need to enter a reason if you don't want to."
    short_action = "Decline"

    def is_permitted(self, user):
        return user == self.offer.volunteer

    def _act(self, user, reason):
        self.offer.time_withdrawn = datetime.datetime.now()
        self.offer.save()
        self.log(user, reason)
        self.email(self.offer.staff, "Volunteer turned down recommendation", """
            %s turned down your recommendation for %s.
            
            They provided the following reason:
            
            %s
        """ % (self.offer.volunteer.get_full_name(), self.offer.position, reason if len(reason) else "(No reason given)"))

    def response(self):
        return "You have declined this suggested position."

class ApproveRequestedPosition(OfferAction):
    """A staff member approves a volunteer request."""
    log_message = "approved the volunteer's application"
    option_text = "Approve the volunteer for this position."
    reason_reason = None
    short_action = "Approve"

    def is_permitted(self, user):
        return user.is_staff

    def _act(self, user, reason):
        self.offer.staff = user
        self.offer.time_staff_accepted = datetime.datetime.now()
        self.offer.save()
        self.log(user, reason)

        reps = self.offer.position.representative
        if settings.NOTIFY_ALL_REPS:
            reps = [rp.profile.user for rp in self.offer.position.organisation.representativeprofile_set.all()]
        self.email(reps, "Volunteer request", VOLUNTEER_OFFER_MESSAGE)

    def response(self):
        return "%s's application has been approved and forwarded to the %s representative." % (self.offer.volunteer.get_full_name(), self.offer.position.organisation,)

class RejectRequestedPosition(OfferAction):
    """A staff member rejects a volunteer request."""
    log_message = "withdrew the volunteer's application"
    option_text = "Withdraw this application."
    reason_reason = "Enter your reason for withdrawing the application below. Your reason will be emailed to the volunteer."
    short_action = "Withdraw"

    def is_permitted(self, user):
        return user.is_staff

    def _act(self, user, reason):
        self.offer.staff = user
        self.offer.time_withdrawn = datetime.datetime.now()
        self.offer.save()
        self.log(user, reason)
        self.email(self.offer.volunteer, "Application withdrawn by staff", """
            Your volunteering application for %s has been withdrawn by the Volunteering staff for the following reason:
            
            %s
            
            If this is in error, please {{ STAFF_EMAIL_INSTRUCTION }}.
            
            We are sorry that your application was unsuccessful, please keep volunteering!
        """ % (self.offer.position, reason))

    def response(self):
        return "The volunteer has been emailed to inform them that their application has been withdrawn."

class AcceptVolunteer(OfferAction):
    """An organisation representative accepts a volunteer (the position remains open)."""
    log_message = "accepted the referral"
    option_text = "Accept the referral - keep advertising the position."
    reason_reason = "Enter a message to send to the volunteer below. The message should include instructions on what the volunteer should do next."
    short_action = "Accept"

    def is_permitted(self, user):
        return (user.get_profile().representativeprofile.organisation == self.offer.position.organisation) or (user == self.offer.position.representative)

    def _act(self, user, reason):
        self.offer.representative = user
        self.offer.time_representative_accepted = datetime.datetime.now()
        self.offer.save()
        self.log(user, reason)
        
        if not settings.FEATURE_ORGANISATION_CONFIRMS_START:
            # Organisation doesn't need to confirm, so we auto-confirm.
            self.offer.time_confirmed_started = self.offer.time_representative_accepted 
            self.offer.save()

            # Create a commitment between the volunteer and the organisation
            commitment = Commitment(
                started = datetime.datetime.now(),
                organisation = self.offer.position.organisation,
                position = self.offer.position,
                volunteer = self.offer.volunteer,
            )
            commitment.save()
        
        self.email(self.offer.volunteer, "An organisation would like to discuss your offer", VOLUNTEER_ACCEPTED_MESSAGE % (self.offer.position, reason, self.offer.representative.email))

    def response(self):
        return "You have accepted %s's referral and your message has been sent." % (self.offer.volunteer.get_full_name(),)

class AcceptLastVolunteer(OfferAction):
    """An organisation representative accepts a volunteer and de-lists the position."""
    log_message = "accepted the referral"
    option_text = "Accept the referral - de-list the advert."
    reason_reason = "Enter a message to send to the volunteer below. The message should include instructions on what the volunteer should do next."
    short_action = "Accept and de-list"

    def is_permitted(self, user):
        return (user.get_profile().representativeprofile.organisation == self.offer.position.organisation) or (user == self.offer.position.representative)

    def _act(self, user, reason):
        self.offer.representative = user
        self.offer.time_representative_accepted = datetime.datetime.now()
        self.offer.save()
        self.log(user, reason)
        
        if not settings.FEATURE_ORGANISATION_CONFIRMS_START:
            # Organisation doesn't need to confirm, so we auto-confirm.
            self.offer.time_confirmed_started = self.offer.time_representative_accepted 
            self.offer.save()

            # Create a commitment between the volunteer and the organisation
            commitment = Commitment(
                started = datetime.datetime.now(),
                organisation = self.offer.position.organisation,
                position = self.offer.position,
                volunteer = self.offer.volunteer,
            )
            commitment.save()

        self.offer.position.active = False
        self.offer.position.save()

        self.email(self.offer.volunteer, "An organisation would like to discuss your offer", VOLUNTEER_ACCEPTED_MESSAGE % (self.offer.position, reason, self.offer.representative.email))

    def response(self):
        return "You have accepted %s's referral and your message has been sent." % (self.offer.volunteer.get_full_name(),)

class RejectVolunteer(OfferAction):
    """An organisation representative rejects a volunteer."""
    log_message = "did not accept the referral"
    option_text = "Do not accept this referral."
    reason_reason = "Enter your reason for declining the referral below. Your reason will be emailed to the volunteer and the admin staff."
    short_action = "Decline"

    def is_permitted(self, user):
        return (user.get_profile().representativeprofile.organisation == self.offer.position.organisation) or (user == self.offer.position.representative)

    def _act(self, user, reason):
        self.offer.representative = user
        self.offer.time_withdrawn = datetime.datetime.now()
        self.offer.save()
        self.log(user, reason)
        self.email(self.offer.staff, "Organisation declined application", """
            %s turned down %s's %s application.
            
            They provided the following reason:
            
            %s
        """ % (self.offer.position.organisation, self.offer.volunteer.get_full_name(), self.offer.position.name, reason if len(reason) else "(No reason given)"))
        self.email(self.offer.volunteer, "Your application was declined", """
            Sorry, %s turned down your %s application.
        
            They provided the following reason:
        
            %s
            
            Please contact the volunteering staff for more information, and don't stop volunteering!
        """ % (self.offer.position.organisation, self.offer.position.name, reason if len(reason) else "(No reason given)"))
        
    def response(self):
        return "Thanks, the volunteer and volunteering staff have been emailed."

class ConfirmVolunteerStarted(OfferAction):
    """An organisation representative confirms that a volunteer showed up and committed time to an opportunity."""
    log_message = "confirmed the volunteer started"
    option_text = "Confirm the volunteer started."
    reason_reason = None
    short_action = "Confirm"

    def is_permitted(self, user):
        return user.get_profile().representativeprofile.organisation == self.offer.position.organisation

    def _act(self, user, reason):
        self.offer.time_confirmed_started = datetime.datetime.now()
        self.offer.save()
        self.log(user, reason)

        # Create a commitment between the volunteer and the organisation
        commitment = Commitment(
            started = datetime.datetime.now(),
            organisation = self.offer.position.organisation,
            position = self.offer.position,
            volunteer = self.offer.volunteer,
        )
        commitment.save()

    def response(self):
        return "%s has been confirmed as started." % (self.offer.volunteer.get_full_name(),)

class MarkVolunteerNotStarted(OfferAction):
    """An organisation representative indicates that a volunteer did not show up, or did not start for some other reason."""
    log_message = "indicated that the volunteer did not start"
    option_text = "Record that the volunteer did not start."
    reason_reason = "Enter your reason for recording that the volunteer did not start. This is especially important if the reason the volunteer did not start is not their fault! Your reason will be emailed to the admin staff."
    short_action = "Record not started"

    def is_permitted(self, user):
        return user.get_profile().representativeprofile.organisation == self.offer.position.organisation

    def _act(self, user, reason):
        self.offer.time_withdrawn = datetime.datetime.now()
        self.offer.save()
        self.log(user, reason)
        self.email(self.offer.staff, "Organisation marked volunteer not started", """
            %s indicated that %s did not start the opportunity "%s".
            
            They provided the following reason:
            
            %s
        """ % (self.offer.position.organisation, self.offer.volunteer.get_full_name(), self.offer.position.name, reason if len(reason) else "(No reason given)"))

    def response(self):
        return "Thanks for your feedback. It has been emailed to the volunteering staff administrators."

# Pending Actions / Requests for Action

class AgreeOfferPendingAction(PendingAction):
    kind = "offer"
    message = "The Volunteering staff have recommended an opportunity to you."
    actions = [
        AgreeSuggestedPosition(None),
        DeclineSuggestedPosition(None),
        ]

class ApproveOfferPendingAction(PendingAction):
    kind = "offer"
    message = "A volunteer is interested in a position in an organisation."
    actions = [
        ApproveRequestedPosition(None),
        RejectRequestedPosition(None),
        ]

class AcceptOfferPendingAction(PendingAction):
    kind = "offer"
    message = "A volunteer is interested in the opportunity you're advertising. Click 'view application details' to review the volunteer and position, and to see the volunteer's contact information. Please contact the volunteer within five working days."
    actions = [
        AcceptVolunteer(None),
        AcceptLastVolunteer(None),
        RejectVolunteer(None),
        ]

class ApproveNewPositionPendingAction(PendingAction):
    kind = "position"
    message = "A representative has created a new position."
    actions = [
        ApproveNewPosition(None),
        EmailRepresentative(None),
        ]

class ApproveRepresentativePendingAction(PendingAction):
    kind = "baseprofile"
    message = "A new organisation representative registration requires approval."
    actions = []

class ConfirmStartedPendingAction(PendingAction):
    kind = "offer"
    message = "Please let us know if a volunteer you accepted has begun contributing their time."
    actions = [
        ConfirmVolunteerStarted(None),
        MarkVolunteerNotStarted(None),
    ]
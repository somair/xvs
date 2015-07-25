import datetime

from django.db import models
from django.contrib.auth.models import User

from south.modelsinspector import add_introspection_rules

from weekgrid import WeekgridField
# Explain WeekgridFields to south
add_introspection_rules([],[".*\.WeekgridField"])

class Offer(models.Model):
    position = models.ForeignKey('positions.Position')

    # The volunteer who will do the job - this is always set.
    volunteer = models.ForeignKey(User, related_name="offers_made")

    # The company representative who agrees to take on the volunteer - set when a representative acknowledges.
    representative = models.ForeignKey(User, related_name="offers_recieved", null=True, blank=True)

    # The Volunteering staff member who either approves or instigates the offer - set when a staff approves or instigates.
    staff = models.ForeignKey(User, related_name="offers_confirmed", null=True, blank=True)

    # The times that the three parties signed off on the offer.
    time_volunteer_accepted = models.DateTimeField(null=True, blank=True)
    time_representative_accepted = models.DateTimeField(null=True, blank=True)
    time_staff_accepted = models.DateTimeField(null=True, blank=True)

    # The time that the organisation confirmed that the volunteer started.
    # If this is not a separate step on this instance then the time will
    # be the same as the time_representative_accepted timestamp. 
    time_confirmed_started = models.DateTimeField(null=True, blank=True)

    time_withdrawn = models.DateTimeField(null=True, blank=True)

    def days_since_time_staff_accepted(self):
        return (datetime.datetime.now() - self.time_staff_accepted).days
    
    def get_application_reason(self):
        """Gets the volunteer's application message, regardless of
        whether they applied, or the position was recommended."""
        logentries = self.logentries.all()
        for logentry in logentries:
            if logentry.action == "agreesuggestedposition" or logentry.action == "requestposition":
                return logentry.reason
        return None

    @models.permalink
    def get_absolute_url(self):
        return ('offers.views.offer', (self.id,))

    def __unicode__(self):
        return "%s at %s" % (self.volunteer.get_full_name(), self.position.organisation.name)

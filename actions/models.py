from django.contrib.auth.models import User
from django.db import models

from offers.models import Offer

class OfferLogEntry(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    offer = models.ForeignKey(Offer, related_name="logentries")
    action = models.CharField(max_length=31)
    reason = models.TextField()

    def __unicode__(self):
        return "%s: %s %s (%s)" % (self.time, self.user, self.action, self.reason)

    def get_action_string(self):
        import actions
        for thing in actions.__dict__.values():
            try:
                if isinstance(thing, actions.Action.__class__):
                    if thing.name() == self.action:
                        return thing.log_message
            except:
                pass
        return "Unknown action (%s)" % self.action
            


import settings
from offers.models import Offer
from positions.models import Position
from profiles.models import BaseProfile
from actions import *

class NoProfile(object):
    """A dummy profile that has no content."""
    is_volunteer = False
    is_representative = False


def get_pending_actions(user):
    """For a given user, get all of the items that are actionable by them."""

    actions = []

    # Get the user's profile.
    try:
        profile = user.get_profile()
    except Exception:
        profile = NoProfile

    # If volunteer, get all unagreed admin suggestions
    if profile.is_volunteer:
        unagreed_offers = Offer.objects.filter(
            volunteer=user,
            time_volunteer_accepted__isnull=True,
            time_staff_accepted__isnull=False,
            time_withdrawn__isnull=True,
            )
        for offer in unagreed_offers:
            actions.append(AgreeOfferPendingAction(offer))

    # If admin...
    if user.is_staff:

        # Get all unapproved volunteer requests
        unapproved_offers = Offer.objects.filter(
            time_volunteer_accepted__isnull=False,
            time_staff_accepted__isnull=True,
            time_withdrawn__isnull=True,
            )
        for offer in unapproved_offers:
            actions.append(ApproveOfferPendingAction(offer))
        
        # Get all unapproved positions
        unapproved_positions = Position.objects.filter(
            approved=False,
            )
        for position in unapproved_positions:
            actions.append(ApproveNewPositionPendingAction(position))

        unapproved_representatives = BaseProfile.objects.filter(
            is_representative=True,
            representativeprofile=None,
            )
        for rep in unapproved_representatives:
            actions.append(ApproveRepresentativePendingAction(rep))

    # If representative... 
    if profile.is_representative:
        rprofile = profile.try_get_representative_profile()
        if rprofile:

            # Get all unaccepted approved and agreed connections for our positions.
            unaccepted_offers = Offer.objects.filter(
                    time_volunteer_accepted__isnull = False,
                    time_staff_accepted__isnull = False,
                    time_representative_accepted__isnull = True,
                    time_withdrawn__isnull = True,
                    )

            if settings.NOTIFY_ALL_REPS:
                unaccepted_offers = unaccepted_offers.filter(position__organisation=rprofile.organisation)
            else:
                unaccepted_offers = unaccepted_offers.filter(position__representative=user)

            for offer in unaccepted_offers:
                actions.append(AcceptOfferPendingAction(offer))

            # Get all approved, agreed, accepted but unstarted offers for our positions.
            unstarted_offers = Offer.objects.filter(
                time_volunteer_accepted__isnull=False,
                time_staff_accepted__isnull=False,
                time_representative_accepted__isnull=False,
                time_withdrawn__isnull=True,
                time_confirmed_started__isnull=True
                )

            if settings.NOTIFY_ALL_REPS:
                unstarted_offers = unstarted_offers.filter(position__organisation=rprofile.organisation)
            else:
                unstarted_offers = unstarted_offers.filter(position__representative=user)

            for offer in unstarted_offers:
                actions.append(ConfirmStartedPendingAction(offer))

    return actions

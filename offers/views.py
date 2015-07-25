from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from models import Offer

from notes.logic import get_notes

from decorators import staff_required

@staff_required
def recent(request):
    last_activity__column = {'last_activity': """
      GREATEST(
        IFNULL(time_staff_accepted, "1000-01-01"), 
        IFNULL(time_volunteer_accepted, "1000-01-01"),
        IFNULL(time_representative_accepted, "1000-01-01"),
        IFNULL(time_withdrawn, "1000-01-01"),
        IFNULL(time_confirmed_started, "1000-01-01")
        )
    """}
    offers = Offer.objects.extra(select=last_activity__column).order_by("-last_activity")[:50]

    return render_to_response("offers/offers.html", {
            'offers': offers,
            }, context_instance=RequestContext(request))


@login_required
def representative_offers(request):
    """Lists successful offers made to a given representative."""
    # You must be a representative of the organisation in order to view this list.
    if request.user.get_profile().is_representative:
        pass
    else:
        raise Exception("You must be a representative to use this function.")

    return render_to_response("offers/representative_offers.html", {
            'offers': Offer.objects.filter(representative=request.user, time_representative_accepted__isnull=False),
            }, context_instance=RequestContext(request))    


@login_required
def offer(request, offer_id):
    offer = get_object_or_404(Offer, pk=offer_id)

    # You may only view information about an offer if you are the user, a representative of the company or a staff member.
    if request.user.is_staff:
        pass
    elif request.user == offer.volunteer:
        pass
    elif request.user.get_profile().is_representative and request.user.get_profile().representativeprofile.organisation == offer.position.organisation:
        pass
    else:
        raise Exception("You don't have permission to see details on this offer. You must either be the volunteer making the offer, a representative of the organisation that is advertising the position or a member of staff in order to view offer details.")

    return render_to_response("offers/offer.html", {
            'offer': offer,
            'notes': get_notes(request, offer),
            'v_user': offer.volunteer,
            }, context_instance=RequestContext(request))

from django.contrib import messages
from django.shortcuts import redirect

from actions.actions import SuggestPosition
from offers.models import Offer

from decorators import staff_required


@staff_required
def recommend_position(request, position, volunteers):
    """Recommend a position to a group of volunteers"""

    action = None

    recommended_volunteers = []
    # The offer won't be made to volunteers who already have offers for this position.
    skipped_volunteers = []

    for volunteer in volunteers:

        action = SuggestPosition(Offer(
                position=position,
                volunteer=volunteer,
                ))

        # Only act if there isn't an existing offer for this volunteer.
        if volunteer not in position.offerers():
            action.do_action(request.user, "")
            recommended_volunteers.append(volunteer)
        else:
            skipped_volunteers.append(volunteer)


    if len(volunteers) == 1:
        if len(skipped_volunteers) == 0:
            message = action.response()
        else:
            message = """\"%s\" could not be recommended to %s 
            because the volunteer has already made or received
            an offer for this opportunity.""" % (
                position.name, skipped_volunteers[0].get_full_name()
            )
    else:
        message = action.response_plural(len(recommended_volunteers))

        if len(skipped_volunteers) > 0:
            message += """
            <br/><br/>
            The recommendation could not be made to %d volunteer(s) because
            they have already made or received offers for this opportunity.""" % len(skipped_volunteers)

    messages.info(request, message, extra_tags='safe')

    return redirect('/')
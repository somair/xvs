from lib.json import JsonResponse, exception_to_json_error
from offers.models import Offer
from django.http import HttpResponse
from positions.models import Position
from actions import *

actions = [
    AgreeSuggestedPosition,
    DeclineSuggestedPosition,
    ApproveRequestedPosition,
    RejectRequestedPosition,
    AcceptVolunteer,
    AcceptLastVolunteer,
    RejectVolunteer,
    ApproveNewPosition,
    EmailRepresentative,
    ConfirmVolunteerStarted,
    MarkVolunteerNotStarted,
]

def find_action(action_name):
    for action in actions:
        if action.name() == action_name:
            return action

    raise Exception("Couldn't find an action with this name.")

#@exception_to_json_error
def do(request):
    if request.method != "POST":
        return HttpResponse(status=405)

    action_name = request.POST['action']
    reason = request.POST['reason']
    subject_id = int(request.POST['subject_id'])
    kind = request.POST['kind']

    if kind == "offer":
        subject = Offer.objects.get(pk=subject_id)
    elif kind == "position":
        subject = Position.objects.get(pk=subject_id)

    # Construct the action object.
    action = find_action(action_name)(subject)
    
    # Do the action.
    action.do_action(request.user, reason)

    return JsonResponse({"result": action.response()})

import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse

from django.views.decorators.http import require_POST

from decorators import staff_required

from positions.models import Organisation

from logic import get_unconfirmed_hours
from models import Commitment, TimeRecord, Endorsement
from forms import DateForm, TimeRecordForm, EndorsementForm

@login_required
def organisation_volunteers(request, organisation_id):
    """Lists all volunteers that are considered active for an organisation."""
    organisation = get_object_or_404(Organisation, pk=organisation_id)

    # You must be a representative of the organisation in order to view this list.
    profile = request.user.get_profile()
    if profile.is_representative or request.user.is_staff:
        pass
    else:
        raise Exception("You must be a representative to use this function.")

    representative_organisation = None

    if profile.is_representative:
        representative_organisation = profile.representativeprofile.organisation

    if request.user.is_staff or representative_organisation == organisation:
        pass
    else:
        raise Exception("You must be a staff administrator or a representative of this organisation to view their volunteers.")

    volunteers = None
    if request.user.is_staff:
        # Valid volunteer list for manual adds.
        volunteers = User.objects.filter(baseprofile__volunteerprofile__id__isnull=False).order_by("last_name")

    return render_to_response("hours/organisation_volunteers.html", {
            'organisation': organisation,
            'volunteers': volunteers,
            }, context_instance=RequestContext(request))
            
@login_required
def commitment(request, commitment_id):
    """Shows all of the details for a given commitment by a volunteer to an organisation."""
    commitment = get_object_or_404(Commitment, pk=commitment_id)
    try:
        endorsement = Endorsement.objects.get(commitment=commitment)
    except Endorsement.DoesNotExist:
        endorsement = None

    # You may only view information about a commitment if you are the user, a representative of the company or a staff member.
    if request.user.is_staff:
        pass
    elif request.user == commitment.volunteer:
        pass
    elif request.user.get_profile().is_representative and request.user.get_profile().representativeprofile.organisation == commitment.organisation:
        pass
    else:
        raise Exception("You don't have permission to see details on this commitment. You must either be the committing volunteer, a representative of the organisation that is committed to, or a member of staff in order to view commitment details.")

    return render_to_response("hours/commitment.html", {
            'commitment': commitment,
            'v_user': commitment.volunteer,
            'date_form': DateForm(),
            'endorsement': endorsement,
            'endorsement_form': EndorsementForm(),
            }, context_instance=RequestContext(request))

@login_required
def volunteer_hours(request, user_id):
    """Shows all hours recorded for volunteers, and a form for the addition of new hours."""
    volunteer = get_object_or_404(User, pk=user_id)

    if request.user.is_staff:
        pass
    elif request.user == volunteer:
        pass
    else:
        raise Exception("You must be either this volunteer or a staff administrator to view this page.")

    hform = TimeRecordForm()
    # Limit the organisations to organisations that the volunteer is an
    # active member of. 
    hform.fields["organisation"].queryset = Organisation.objects.filter(commitment__volunteer=request.user)

    if request.method == "POST":
        hform = TimeRecordForm(request.POST)

        if hform.is_valid():
            record = hform.save(commit=False)
            record.volunteer = volunteer

            # If the manual_organisation matches an organisation, set the organisation.
            matching_organisations = Organisation.objects.filter(name=record.manual_organisation)
            if matching_organisations:
                record.organisation = matching_organisations[0]
                record.manual_organisation = None

            record.save()
            messages.info(request, "Your hours record has been added.")

    return render_to_response("hours/volunteer_hours.html", {
        'volunteer': volunteer,
        'v_user': volunteer,
        'hform': hform,
        'timerecords': volunteer.timerecord_set.all()
    }, context_instance=RequestContext(request))
    
@login_required
@require_POST
def set_finish_date(request, commitment_id):
    commitment = get_object_or_404(Commitment, pk=commitment_id)

    if (request.user.get_profile().is_representative and request.user.get_profile().representativeprofile.organisation == commitment.organisation) or request.user.is_staff:
        pass
    else:
        raise Exception("Only a representative of the organisation that is committed to (or a staff member) may set a finish date on a commitment.")
    
    date_form = DateForm(request.POST)
    if date_form.is_valid():
        date = date_form.cleaned_data['date']
        
        commitment.finished = date
        commitment.save()
    
        return redirect('hours.views.commitment', commitment_id=commitment.id)
    else:
        raise Exception("Invalid form data received. Please contact support.")

@login_required
@require_POST
def clear_finish_date(request, commitment_id):
    commitment = get_object_or_404(Commitment, pk=commitment_id)

    if (request.user.get_profile().is_representative and request.user.get_profile().representativeprofile.organisation == commitment.organisation) or request.user.is_staff:
        pass
    else:
        raise Exception("Only a representative of the organisation that is committed to (or a staff member) may set a finish date on a commitment.")
    
    commitment.finished = None
    commitment.save()
    return redirect('hours.views.commitment', commitment_id=commitment.id)

@login_required
def review(request, organisation_id=None):
    """Review all unreviewed hours, marking them as confirmed or optionally refusing to mark them at all."""
    
    if request.user.get_profile().is_representative and not request.user.is_staff:
        is_organisation = True
    elif request.user.is_staff:
        is_organisation = False
    else:
        raise Exception("Only organisation representatives and staff administrators can use this page.")
    
    records = sorted(get_unconfirmed_hours(request.user, organisation_id), key=lambda r: r.date_worked)
    
    # Group the records by person
    volunteers = {}
    for record in records:
        if record.volunteer not in volunteers:
            volunteers[record.volunteer] = []
        volunteers[record.volunteer].append(record)
    
    # Create an ordered list of volunteer/list-of-timerecord tuples.
    volunteer_list = []
    for volunteer in sorted(volunteers.keys(), key=lambda v: v.get_full_name().lower()):
        volunteer_list.append((volunteer, volunteers[volunteer]))

    return render_to_response("hours/review.html", {
        'volunteers': volunteer_list,
        'timerecords': records,
        'is_organisation': is_organisation,
        'organisation': Organisation.objects.get(pk=organisation_id) if (organisation_id and request.user.is_staff) else None
    }, context_instance=RequestContext(request))
    
@login_required
def mark_record(request):
    timerecord = get_object_or_404(TimeRecord, pk=int(request.POST['record_id']))
    
    if request.user.get_profile().is_representative and request.user.get_profile().try_get_representative_profile().organisation == timerecord.organisation:
        pass
    elif request.user.is_staff:
        pass
    else:
        raise Exception("Only organisation representatives and staff administrators can mark records.")
    
    status = request.POST['status']
    
    response = None
    
    if status == "correct":
        timerecord.confirmed = 1
        response = "The record has been marked as correct."
    elif status == "unconfirmable":
        timerecord.confirmed = 0
        response = "The record has been marked as unconfirmable."
    else:
        raise Exception("Unrecognised status")
    
    timerecord.reviewed = datetime.datetime.now()
    timerecord.reviewed_by = request.user
    timerecord.save()
    
    return HttpResponse(response)
    
@login_required
def delete(request):
    timerecord_id = int(request.POST['timerecord_id'])
    timerecord = get_object_or_404(TimeRecord, pk=timerecord_id)

    if timerecord.volunteer == request.user or request.user.is_staff:
        timerecord.delete()
        return HttpResponse("Record deleted.")
    else:
        return HttpResponse("Sorry, only volunteers and staff administrators can delete time records.")

    
@staff_required
def add_volunteer(request):
    organisation = get_object_or_404(Organisation, pk=int(request.POST['organisation_id']))
    volunteer = get_object_or_404(User, pk=int(request.POST['user_id']))
    
    commitment = Commitment(
        organisation=organisation,
        volunteer=volunteer,
        started=datetime.datetime.now()
        )
    commitment.save()
    
    messages.info(request, volunteer.get_full_name() + " has been added to this organisation's volunteer list.")
    return redirect('hours.views.organisation_volunteers', organisation_id=organisation.id)

@login_required
def add_endorsement(request, commitment_id):

    commitment = get_object_or_404(Commitment, pk=commitment_id)

    if request.user.get_profile().is_representative and request.user.get_profile().representativeprofile.organisation == commitment.organisation:
        pass
    elif request.user.is_staff:
        pass
    else:
        raise Exception("Only organisation representatives and staff administrators make endorsements.")

    if request.POST:
        user = request.user
        text = request.POST.get('endorsement_text')

        endorsement = Endorsement(commitment=commitment, representative=user, endorsement_text=text)
        endorsement.save()

        messages.info(request, "Endorsement has been recorded.")
    else:
        messages.info(request, "Endorsement not saved, request must be post.")

    return redirect('hours.views.commitment', commitment_id=commitment.id)


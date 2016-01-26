import datetime

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
from django.db.models import Max
from lib import xls

from decorators import staff_required

import settings

from offers.models import Offer
from positions.models import Organisation, Position
from hours.models import TimeRecord
from profiles.models import Faculty, Award, AwardType
import forms

@staff_required
def sla_check(request, filter):

    # Get all volunteers and the number of offers against their name.
    offers = Offer.objects.filter(
        time_staff_accepted__isnull=False, 
        time_representative_accepted__isnull=True, 
        time_volunteer_accepted__isnull=False,
        time_withdrawn__isnull=True)

    if filter == 'recent':
        # Filter by volunteers who have never been accepted by a representative.
        offers = offers.filter(time_staff_accepted__gte=datetime.datetime.now() - datetime.timedelta(days=31))

    export_filename = "sla-export.xls"
    if 'export' in request.REQUEST:
        if request.REQUEST['export'] == 'xls':
            return xls.XlsResponse([
                xls.Column("Volunteer", lambda x: x.volunteer.get_full_name() ),
                xls.Column("Organisation", lambda x: x.position.organisation.name),
                xls.Column("Offer Received", lambda x: x.time_staff_accepted),
                xls.Column("Days Awaiting Response", lambda x: x.days_since_time_staff_accepted()),
                ], offers, export_filename)

    return render_to_response("reports/sla.html", {
            'offers': offers,
            'filter': filter,
            }, context_instance=RequestContext(request))

@staff_required
def user_breakdown(request):
    volunteers = User.objects.filter(baseprofile__is_volunteer=True)

    volunteer_count = volunteers.count()

    class Count:
        def __init__(self, name, query):
            self.name = name
            self.count = query.count()
            self.percentage = "%.2f%%" % ((float(query.count())/float(volunteer_count)) * 100)

    class Break:
        is_break = True

    counts = [
        Break,
        Count('All Volunteers', volunteers),
        Break,
    ]

    def format_label(label):
        return label[0].upper() + label[1:] + "s"

    for value, label in settings.GRAD_CHOICES:
        counts.append(
            Count(format_label(label), volunteers.filter(baseprofile__volunteerprofile__postgrad=value))
            )

    counts.append(Break)

    for value, label in settings.INTERNATIONAL_CHOICES:
        counts.append(
            Count(format_label(label), volunteers.filter(baseprofile__volunteerprofile__international=value))
            )

    counts.append(Break)

    counts += [
        Count('Gender: Male', volunteers.filter(baseprofile__volunteerprofile__gender='M')),
        Count('Gender: Female', volunteers.filter(baseprofile__volunteerprofile__gender='F')),
        Count('Gender: Unspecified', volunteers.filter(baseprofile__volunteerprofile__gender='U')),
    ]

    counts.append(Break)

    for faculty in Faculty.objects.all().order_by("name"):
        counts.append(
            Count(faculty.name, volunteers.filter(baseprofile__volunteerprofile__school=faculty.name))
            )
    counts.append(
            Count("No school specified", volunteers.filter(baseprofile__volunteerprofile__school=""))
        )

    return render_to_response("profiles/breakdown.html", {
            'counts': counts,
        }, context_instance=RequestContext(request))
    

@staff_required
def inactive_volunteers(request):
    volunteers = User.objects\
        .filter(baseprofile__is_volunteer=True, baseprofile__archived=False)\
        .annotate(last_offer=Max('offers_made__time_volunteer_accepted'))\
        .filter(last_offer__isnull=True)\
        .order_by('date_joined')
    
    now = datetime.datetime.now()
    for volunteer in volunteers:
        volunteer.age = (now - volunteer.date_joined).days
        volunteer.received_offer_count = Offer.objects\
            .filter(volunteer=volunteer)\
            .filter(time_volunteer_accepted__isnull=True)\
            .count()

    export_filename = "inactive-volunteers-export.xls"
    if 'export' in request.REQUEST:
        if request.REQUEST['export'] == 'xls':
            return xls.XlsResponse([
                xls.Column("Volunteer", lambda x: x.get_full_name() ),
                xls.Column("Registered", lambda x: x.date_joined),
                xls.Column("Account Age", lambda x: x.age),
                xls.Column("# Recommendations", lambda x: x.received_offer_count),
                ], volunteers, export_filename)

    return render_to_response("reports/inactive_volunteers.html", {
            'volunteers': volunteers,
            }, context_instance=RequestContext(request))

@staff_required
def time_records(request):
    dform = forms.DateRangeForm(request.GET)
    start = None
    end = None
    actual_end = None

    if dform.is_valid():
        start = dform.cleaned_data['date_start']
        end = dform.cleaned_data['date_end']
        actual_end = end + datetime.timedelta(days=1)
        
    time_records = TimeRecord.objects.filter(
        date_worked__gte=start,
        date_worked__lt=actual_end,
        )

    volunteers = {}
    class VolunteerInfo:
        pass

    totalmins = 0

    for time_record in time_records:
        if time_record.volunteer not in volunteers:
            vi = VolunteerInfo()
            vi.name = time_record.volunteer.get_full_name()
            vi.mins = 0
            vi.records = 0
            volunteers[time_record.volunteer] = vi

        mins = (time_record.hours*60) + time_record.minutes
        volunteers[time_record.volunteer].mins += mins
        volunteers[time_record.volunteer].records += 1
        totalmins += mins


    for vi in volunteers.values():
        vi.hours = int(vi.mins / 60)
        vi.minutes = vi.mins % 60

    totalhours = int(totalmins / 60)
    totalminutes = totalmins % 60

    return render_to_response("reports/time_records.html", {
        'start': start,
        'end': end,
        'time_records': time_records,
        'volunteerinfos': sorted(volunteers.values(), key=(lambda vi: vi.name.lower())),
        'totalhours': totalhours,
        'totalminutes': totalminutes,
    }, context_instance=RequestContext(request))

@staff_required
def activity(request):
    dform = forms.DateRangeForm(request.GET)
    start = None
    end = None
    actual_end = None
    if dform.is_valid():
        start = dform.cleaned_data['date_start']
        end = dform.cleaned_data['date_end']
        actual_end = end + datetime.timedelta(days=1)
    
    new_volunteers = User.objects.filter(
        baseprofile__is_volunteer=True,
        date_joined__gte=start,
        date_joined__lt=actual_end,
        is_active=True,
        )
    
    # Fetch all organisations for which all their representatives joined in this period
    new_organisations = Organisation.objects.filter(
        date_created__gte=start,
        date_created__lt=actual_end,
    )

    new_representatives = User.objects.filter(
        baseprofile__is_representative=True,
        date_joined__gte=start,
        date_joined__lt=actual_end,
        )
        
    new_positions = Position.objects.filter(
        date_created__gte=start,
        date_created__lt=actual_end
    )

    offers_made = Offer.objects.filter(
        time_volunteer_accepted__gte=start,
        time_volunteer_accepted__lt=actual_end
    )

    offers_accepted = Offer.objects.filter(
        time_representative_accepted__isnull=False,
        time_volunteer_accepted__gte=start,
        time_volunteer_accepted__lt=actual_end
    )

    offers_started = Offer.objects.filter(
        time_confirmed_started__isnull=False,
        time_volunteer_accepted__gte=start,
        time_volunteer_accepted__lt=actual_end
    )
    
    return render_to_response("reports/activity.html", {
        'start': start,
        'end': end,
        'new_volunteers': new_volunteers,
        'new_organisations': new_organisations,
        'new_representatives': new_representatives,
        'new_positions': new_positions,
        'offers_made': offers_made,
        'offers_accepted': offers_accepted,
        'offers_started': offers_started,
    }, context_instance=RequestContext(request)) 

@staff_required
def awards(request):
    awards = Award.objects.all()

    export_filename = "awards-export.xls"

    if 'export' in request.REQUEST:
        if request.REQUEST['export'] == 'xls':
            return xls.XlsResponse([
                xls.Column("Award", lambda x: x.award.name),
                xls.Column("First name", lambda x: x.user.first_name),
                xls.Column("Last name", lambda x: x.user.last_name),
                xls.Column("Date", lambda x: x.date_awarded),
                ], awards, export_filename)

    return render_to_response("reports/awards.html", {
        'awards': awards,
    }, context_instance=RequestContext(request))


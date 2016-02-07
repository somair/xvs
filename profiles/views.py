import datetime
import mimetypes
import os

from django.shortcuts import get_object_or_404, render_to_response, redirect, HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db.models import Count, Max
from django.db.models import Q
from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse
from django.contrib.auth import login, authenticate

from lib import xls
from lib.ximage import ImageProcessor, ImageCache
import lib.ximage.operations as ops

import mailer.logic
from mailer.models import Recipient
import positions.logic
from decorators import staff_required, representative_or_staff

from models import *
from positions.models import Organisation, Position
from notes.logic import get_notes
from forms import *

from hours.models import Endorsement

from actions.actions import Action

import logic
import settings


# Volunteer photos
cache = ImageCache(settings.MEDIA_ROOT + "/cache/")
process = [ops.square(), ops.resize(200, 200)]
processor = ImageProcessor(cache, process)

thumb_process = [ops.square(), ops.resize(150, 150)]
thumb_processor = ImageProcessor(cache, thumb_process)


def all_of(choices):
    return [unicode(c[0]) for c in choices]

def booleanise(choices):
    return [c == u'True' for c in choices]


class DummyForm(object):
    """Pretends to be a form. Allows multiple forms to be handled
    and validated when some of the forms may not actually be in use."""
    def __init__(self, *args, **kwargs):
        pass

    def is_valid(self):
        return True

    def save(self, commit=False):
        pass

def email_approved_representative(profile):
    message = """Your representative profile has been approved. You can now log into the volunteering website and start adding opportunity adverts."""
    Action().email(profile.user, "Representative profile approved", message)

@staff_required
def approve(request, user_id):
    profile = get_object_or_404(BaseProfile, user__id=user_id)

    if request.method == "POST":
        if "organisation_id" in request.POST:
            organisation = Organisation.objects.get(pk=int(request.POST["organisation_id"]))
            RepresentativeProfile.objects.create(
                profile=profile,
                organisation=organisation,
                )
            messages.info(request, "You have approved %s." % profile.user.get_full_name())
            email_approved_representative(profile)
            return redirect("/")
        if "organisation_name" in request.POST:
            organisation = Organisation(
                name=request.POST['organisation_name'],
                department=profile.department,
            )
            organisation.save()

            RepresentativeProfile.objects.create(
                profile=profile,
                organisation=organisation,
                )
            messages.info(request, "You have approved %s." % profile.user.get_full_name())
            email_approved_representative(profile)
            return redirect("/")



    return render_to_response("profiles/approve.html", {
            'slas': ServiceLevelAgreement.objects.all(),
            'profile': profile,
            'v_user': profile.user,
            'organisations': Organisation.objects.all()
            }, context_instance=RequestContext(request))

@login_required
def profile(request, user_id):
    profile = get_object_or_404(BaseProfile, user__id=user_id)
    timerecords = profile.user.timerecord_set.all()
    endorsements = Endorsement.objects.filter(commitment__volunteer__id=user_id)
    mailouts = Recipient.objects.filter(user__id=user_id).exclude(mailout__sent=None)

    minutes = 0
    for tr in timerecords:
        minutes += (60*tr.hours + tr.minutes)
    hours = int(minutes/60)
    minutes = minutes%60

    # You may only view a profile if you are the user, a representative of a company receiving an offer or a staff member.
    if request.user.is_staff:
        pass
    elif request.user == profile.user:
        pass
    elif request.user.get_profile().is_representative:
        # Get the organisations this user has made offers to.
        offers = profile.user.offers_made.all()
        rep_organisation = request.user.get_profile().try_get_representative_profile().organisation
        organisations = [offer.position.organisation for offer in offers]
        if rep_organisation in organisations:
            # This user has made an offer to this organisation.
            # Only show time records for this organisation
            timerecords = profile.user.timerecord_set.filter(organisation=rep_organisation)
            pass
        else:
            raise Exception("You don't have permission to see this profile. You must either be the profile owner, a representative of an organisation that is advertising a position that this volunteer is applying to, or a member of staff in order to view offer details.")
    else:
        raise Exception("You don't have permission to see this profile. You must either be the profile owner, a representative of an organisation that is advertising a position that this volunteer is applying to, or a member of staff in order to view offer details.")

    # Get a list of currently active positions
    positions = Position.objects.filter(approved=True, active=True)

    awards = Award.objects.filter(user=profile.user)

    skill_set = set(s.name for p in positions for s in p.skills_gained.all())

    if settings.FEATURE_PROFILE_V2:
        template_name = "profiles/profilev2.html"
    else:
        template_name = "profiles/profile.html"

    if "print" in request.REQUEST and settings.FEATURE_PROFILE_V2:
        template_name = "profiles/printv2.html"
    elif "print" in request.REQUEST:
        template_name = "profiles/print.html"

    return render_to_response(template_name, {
            'profile': profile,
            'endorsements': endorsements,
            'awards': awards,
            'mailouts': mailouts,
            'notes': get_notes(request, profile.user, redirect=reverse('profiles.views.profile', args=(profile.user.id,))),
            'v_user': profile.user,
            'timerecords': timerecords,
            'total_hours': hours,
            'total_minutes': minutes,
            'positions': positions,
            'readonly': 'print' in request.REQUEST,
            'skill_set': skill_set,
            }, context_instance=RequestContext(request))

@login_required
def volunteer_photo(request, user_id):
    profile = get_object_or_404(VolunteerProfile, profile__user__id=user_id)

    path = settings.MEDIA_ROOT+"/img/no-photo.jpg"
    if profile.photo:
        path = profile.photo.path

    data = processor.process(path)

    return HttpResponse(data, mimetype="image/jpeg")

@login_required
def volunteer_photo_thumb(request, user_id):
    profile = get_object_or_404(VolunteerProfile, profile__user__id=user_id)

    path = settings.MEDIA_ROOT+"/img/no-photo.jpg"
    if profile.photo:
        path = profile.photo.path

    data = thumb_processor.process(path)

    return HttpResponse(data, mimetype="image/jpeg")

@login_required
def offers(request, user_id):
    """Shows all of the offers relating to this volunteer."""
    user = get_object_or_404(User, pk=user_id)

    # You may only view a profile if you are the user, a representative of a company receiving an offer or a staff member.
    if request.user.is_staff:
        pass
    elif request.user == user:
        pass
    elif request.user.get_profile().is_representative:
        # Get the organisations this user has made offers to.
        offers = user.offers_made.all()
        organisations = [offer.position.organisation for offer in offers]
        if request.user.get_profile().representativeprofile.organisation in organisations:
            pass
        else:
            raise Exception("You don't have permission to see this profile. You must either be the profile owner, a representative of an organisation that is advertising a position that this volunteer is applying to, or a member of staff in order to view offer details.")
    else:
        raise Exception("You don't have permission to see this profile. You must either be the profile owner, a representative of an organisation that is advertising a position that this volunteer is applying to, or a member of staff in order to view offer details.")

    return render_to_response("profiles/offers.html", {
            'v_user': user,
            }, context_instance=RequestContext(request))

@staff_required
def representatives(request, filter=None, action=None):

    if action:
        if action == "mailout":
            if request.method == "POST":
                representative_ids = logic.get_action_ids(request)
                representatives = [get_object_or_404(User, pk=rid) for rid in representative_ids]
                return redirect(mailer.logic.new(representatives, request.user))

    representatives = User.objects\
        .select_related('baseprofile', 'baseprofile__representativeprofile__organisation__name')\
        .filter(baseprofile__representativeprofile__isnull=False)\
        .order_by('first_name')

    export_filename = "representatives-export.xls"

    if ("mailer_new" in request.GET):
        return redirect(mailer.logic.new(representatives, request.user))

    if 'export' in request.REQUEST:
        if request.REQUEST['export'] == 'xls':
            return xls.XlsResponse([
                xls.Column("First name", lambda x: x.first_name),
                xls.Column("Last name", lambda x: x.last_name),
                xls.Column("Email", lambda x: x.email),
                xls.Column("Organisation", lambda x: x.baseprofile.representativeprofile.organisation.name),
                ], representatives, export_filename)

    return render_to_response("profiles/representatives.html", {
        'representatives': representatives,
        'filter': filter,
        'action': action,
        }, context_instance=RequestContext(request))

@staff_required
def bulk_deactivate(request):
    # For each year, count how many students are graduating in this year.

    if (request.method == "POST"):
        year = int(request.REQUEST.get('year', 0))
        students_to_deactivate = User.objects.filter(baseprofile__volunteerprofile__year__exact=year)
        for student in students_to_deactivate:
            profile = student.get_profile()
            profile.archived = True
            profile.save()

    current_year = datetime.datetime.now().year
    years = range(2010, current_year+3)

    class SchoolYear:
        pass

    schoolyears = []
    for year in years:
        schoolyear = SchoolYear()
        schoolyear.year = year
        schoolyear.all_students = User.objects.filter(baseprofile__volunteerprofile__year__exact=year)
        schoolyear.active_students = schoolyear.all_students.filter(baseprofile__archived=False)
        schoolyear.inactive_students = schoolyear.all_students.filter(baseprofile__archived=True)
        schoolyears.append(schoolyear)

    return render_to_response("profiles/bulk_deactivate.html", {
        'schoolyears': schoolyears
        }, context_instance=RequestContext(request))

@representative_or_staff
def volunteers(request, position_id=None, filter=None, action=None, organisation_id=''):

    if not request.user.is_staff:
        organisation_id = request.user.get_profile().representativeprofile.organisation.id

    position = None

    if action:
        if action == "recommend":
            position = get_object_or_404(Position, pk=position_id)
            if request.method == "POST":
                volunteer_ids = logic.get_action_ids(request)
                volunteers = [get_object_or_404(User, pk=vid) for vid in volunteer_ids]
                positions.logic.recommend_position(request, position, volunteers)
        if action == "mailout":
            if request.method == "POST":
                volunteer_ids = logic.get_action_ids(request)
                volunteers = [get_object_or_404(User, pk=vid) for vid in volunteer_ids]
                return redirect(mailer.logic.new(volunteers, request.user, organisation_id))

    type_filter_form = VolunteerTypeFilterForm(request.GET)
    type_filter_form.is_valid()
    grad_filter = type_filter_form.cleaned_data['postgrad']
    international_filter = type_filter_form.cleaned_data['international']
    course_filter = type_filter_form.cleaned_data['course']
    category_filter = type_filter_form.cleaned_data['category']
    faculty_filter = type_filter_form.cleaned_data['faculty']
    hours_filter = type_filter_form.cleaned_data['hours']
    year_filter = type_filter_form.cleaned_data['year']

    column_filter_form = ColumnFilterForm(request.GET)
    column_filter_form.is_valid()
    columns = column_filter_form.cleaned_data['columns']

    if grad_filter == []:
        grad_filter = all_of(GRAD_CHOICES)
    if international_filter == []:
        international_filter = all_of(INTERNATIONAL_CHOICES)
    if columns == []:
        columns = VOLUNTEER_COLUMN_CHOICES_DEFAULT

    type_filter_form.data = {
        'postgrad': grad_filter,
        'international': international_filter,
        'course': course_filter,
        'faculty': faculty_filter,
        'category': category_filter,
        'hours': hours_filter,
        'year': year_filter,
    }

    column_filter_form.data = {
        'columns': columns,
    }

    # The __in operator doesn't work for NULL. Instead, __isnull must be used.
    grad_filter_exp = Q(baseprofile__volunteerprofile__postgrad__in=booleanise(grad_filter))
    if 'None' in grad_filter:
         grad_filter_exp |= Q(baseprofile__volunteerprofile__postgrad__isnull=True)

    # In the special case that all ineternational choices are chosen, we also select records
    # for students who don't have an international status.
    if set(international_filter) == set(all_of(INTERNATIONAL_CHOICES)):
        international_filter.append("")
    international_filter_exp = Q(baseprofile__volunteerprofile__international__in=international_filter)

    ### BASE QUERY ###

    volunteers = User.objects\
        .filter(baseprofile__is_volunteer=True, baseprofile__archived=(filter == 'deactivated'))\
        .filter(international_filter_exp)\
        .filter(grad_filter_exp)\
        .order_by('first_name')

    ### ORGANISATION FILTER ###
    organisation = None
    if organisation_id:
        volunteers = volunteers.filter(commitment__organisation__id=organisation_id)
        organisation = Organisation.objects.get(pk=organisation_id)

    ### ADD FILTERS ###

    if course_filter:
        volunteers = volunteers.filter(baseprofile__volunteerprofile__course__icontains=course_filter)

    if year_filter and year_filter != "ALL":
        volunteers = volunteers.filter(baseprofile__volunteerprofile__year__exact=int(year_filter))

    if faculty_filter:
        volunteers = volunteers.filter(baseprofile__volunteerprofile__school=faculty_filter.name)

    if category_filter:
        volunteers = volunteers.filter(baseprofile__volunteerprofile__categories=category_filter)

    if hours_filter == "HAS_HOURS":
        volunteers = volunteers.filter(timerecord__isnull=False)

    if hours_filter == "NO_HOURS":
        volunteers = volunteers.filter(timerecord__isnull=True)

    ### ADD FOREIGN COLUMNS ###

    if 'year' in columns:
        volunteers = volunteers.select_related('baseprofile__volunteerprofile__year')

    if 'course' in columns:
        volunteers = volunteers.select_related('baseprofile__volunteerprofile__course')

    ### ADD COMPLEX COLUMNS ###

    if 'offers' in columns:
        volunteers = volunteers.annotate(Count('offers_made'))

    if 'last_accepted' in columns or filter == 'uncommitted':
        volunteers = volunteers.annotate(last_accepted=Max('offers_made__time_representative_accepted'))

    if 'last_offered' in columns or filter == 'inactive':
        volunteers = volunteers.annotate(last_offered=Max('offers_made__time_volunteer_accepted'))

    ### ADDITIONAL FILTERING (should be converted to generic filters above) ###

    export_filename = "volunteers-export.xls"

    if filter == 'uncommitted':
        # Filter by volunteers who have never been accepted by a representative.
        volunteers = volunteers.filter(last_accepted__isnull=True)
        export_filename = "uncommitted-volunteers-export.xls"
    if filter == 'inactive':
        # Filter by volunteers who have never agreed to a position.
        volunteers = volunteers.filter(last_offered__isnull=True)
        export_filename = "inactive-volunteers-export.xls"

    if 'export' in request.REQUEST:
        if request.REQUEST['export'] == 'xls':
            xls_columns = [
                xls.Column("First name", lambda x: x.first_name),
                xls.Column("Last name", lambda x: x.last_name),
                xls.Column("Email", lambda x: x.email),
            ]

            if settings.FEATURE_DISPLAY_STUDENT_ID:
                xls_columns.append(xls.Column("Student ID", lambda x: x.get_profile().volunteerprofile.student_id))

            if "course" in columns:
                xls_columns.append(xls.Column("Course", lambda x: x.baseprofile.volunteerprofile.course))

            if "registered" in columns:
                xls_columns.append(xls.Column("Registered", lambda x: x.date_joined))

            if "grad_year" in columns:
                xls_columns.append(xls.Column("Grad. year", lambda x: x.baseprofile.volunteerprofile.year))

            if "offers" in columns:
                xls_columns.append(xls.Column("Offers", lambda x: x.offers_made__count))

            if "last_accepted" in columns:
                xls_columns.append(xls.Column("Last accepted", lambda x: x.last_accepted))

            if "hours_logged" in columns:
                xls_columns.append(xls.Column("Hours logged", lambda x: x.get_profile().total_hours()))
                xls_columns.append(xls.Column("Hours confirmed", lambda x: x.get_profile().total_confirmed_hours()))

            return xls.XlsResponse(xls_columns, volunteers, export_filename)

    ### POST_PROCESSING ###

    return render_to_response("profiles/volunteers.html", {
            'volunteers': volunteers,
            'organisation': organisation,
            'filter': filter,
            'tform': type_filter_form,
            'cform': column_filter_form,
            'columns': columns,
            'action': action,
            'position': position,
            }, context_instance=RequestContext(request))

@staff_required
def marketing(request, filter):

    # Get all volunteers and the number of offers against their name.
    volunteers = User.objects.filter(baseprofile__is_volunteer=True)\
        .select_related('baseprofile__volunteerprofile__referrer')\
        .order_by('-date_joined')

    export_filename = "marketing-export.xls"

    if 'export' in request.REQUEST:
        if request.REQUEST['export'] == 'xls':
            return xls.XlsResponse([
                xls.Column("Date joined", lambda x: x.date_joined),
                xls.Column("First name", lambda x: x.first_name),
                xls.Column("Last name", lambda x: x.last_name),
                xls.Column("How did you hear about...?", lambda x: x.baseprofile.volunteerprofile.referrer if x.baseprofile.volunteerprofile else ""),
                ], volunteers, export_filename)

    return render_to_response("profiles/marketing.html", {
            'volunteers': volunteers,
            'filter': filter,
            }, context_instance=RequestContext(request))

@login_required
def update(request):
    # Get profiles

    # The base profile should always exist for a user so we create it on the fly.
    profile, created = BaseProfile.objects.get_or_create(user=request.user)

    # Volunteer and Representative profiles may or may not exist.
    try:
        vprofile = profile.volunteerprofile
    except VolunteerProfile.DoesNotExist:
        vprofile = VolunteerProfile(profile=profile)
    try:
        rprofile = profile.representativeprofile
    except RepresentativeProfile.DoesNotExist:
        rprofile = RepresentativeProfile(profile=profile)


    if request.method == "POST":
        # Create dummy form objects so that if the user doesn't have
        # this profile nothing happens.
        vpform = DummyForm(auto_id='id_v_%s')
        rpform = DummyForm()
        opform = DummyForm(auto_id='id_o_%s')
        # If the profiles do exist, replace the dummy forms with
        # actual forms.
        if profile.is_volunteer:
            vpform = VolunteerProfileUpdateForm(request.POST, request.FILES, instance=vprofile, auto_id='id_v_%s')
        if profile.is_representative:
            rpform = RepresentativeProfileForm(request.POST, instance=rprofile)
            opform = OrganisationProfileForm(request.POST, request.FILES, instance=rprofile.organisation, auto_id='id_o_%s')

        if vpform.is_valid() and rpform.is_valid() and opform.is_valid():
            vprofile = vpform.save(commit=False)
            rpform.save()
            opform.save()
            if "delete_reference" in request.POST:
                if request.POST['delete_reference'] == "delete":
                    vprofile.referencefile.delete()
            if "delete_cv" in request.POST:
                if request.POST['delete_cv'] == "delete":
                    vprofile.cv.delete()
            if vprofile:
                vprofile.save()
                vpform.save_m2m()
            return redirect('/')

    else:
        vpform = VolunteerProfileUpdateForm(instance=vprofile)
        rpform = RepresentativeProfileForm(instance=rprofile)
        opform = OrganisationProfileForm(instance=rprofile.organisation if profile.is_representative else None)

    return render_to_response("profiles/update.html", {
            'vpform': vpform,
            'rpform': rpform,
            'opform': opform,
            'faculties': Faculty.objects.all(),
            'vprofile': vprofile,
            }, context_instance=RequestContext(request))

@login_required
def serve_reference_file(request, user_id):
    profile = get_object_or_404(BaseProfile, user__id=user_id)
    user = profile.user

    if user == request.user or request.user.is_staff:
        path = profile.volunteerprofile.referencefile.path
        wrapper = FileWrapper(file(path))
        response = HttpResponse(wrapper, content_type=mimetypes.guess_type(os.path.basename(path))[0])
        response['Content-Length'] = os.path.getsize(path)
        return response
    else:
        return HttpResponse("<p>You aren't allowed to view this document</p>")


@login_required
def serve_cv(request, user_id):
    profile = get_object_or_404(BaseProfile, user__id=user_id)
    user = profile.user

    if user == request.user or request.user.is_staff:
        path = profile.volunteerprofile.cv.path
        wrapper = FileWrapper(file(path))
        response = HttpResponse(wrapper, content_type=mimetypes.guess_type(os.path.basename(path))[0])
        response['Content-Length'] = os.path.getsize(path)
        return response
    else:
        return HttpResponse("<p>You aren't allowed to view this document</p>")

@login_required
def communication(request):
    base_profile = BaseProfile.objects.get(user=request.user)

    if request.POST:
        if base_profile.communication:
            base_profile.communication = False
        else:
            base_profile.communication = True
        base_profile.save()
        return redirect(communication)

    return render_to_response("profiles/comms.html", {
            'base_profile': base_profile,
            }, context_instance=RequestContext(request))

def login_as_user(request, user_id):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Exception("Only staff and administrators can use this function.")

    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        raise Exception("User with this ID does not exist.")

    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)

    return redirect("/")

@login_required
def my_awards(request):

    timerecords = request.user.timerecord_set.all()
    minutes = 0
    for tr in timerecords:
        minutes += (60*tr.hours + tr.minutes) 
    
    hours = int(minutes/60)
    minutes = minutes%60

    my_awards = Award.objects.filter(user=request.user)
    my_award_types = [award.award for award in my_awards]
    all_awards = AwardType.objects.all().order_by('hours_required')

    return render_to_response("profiles/my_awards.html", {
            'hours': hours,
            'my_awards': my_awards,
            'my_award_types': my_award_types,
            'all_awards': all_awards,
            }, context_instance=RequestContext(request))


import datetime
import json

from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.http import HttpResponse

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.contrib import messages
from django.contrib.syndication.views import Feed
from django.db.models import Count, Max
from django.core.urlresolvers import reverse
from django.http import HttpResponse

from lib import xls

from settings import MAX_OFFERS_PER_24_HOURS, REQUIRE_REGISTRATION_TO_VIEW_ADVERTS, FEATURE_REFERENCE_FILE, MEDIA_ROOT

from decorators import staff_required

from notes.logic import get_notes
from actions.actions import RequestPosition, SuggestPosition
from offers.models import Offer
from profiles.models import BaseProfile, VolunteerProfile

from models import *
from forms import *


from lib.ximage import ImageProcessor, ImageCache
import lib.ximage.operations as ops

cache = ImageCache(MEDIA_ROOT + "/cache/")
process = [ops.square(), ops.resize(300, 300)]
processor = ImageProcessor(cache, process)

class LatestPositionsFeed(Feed):
    title = "Latest Volunteering Opportunities"
    link = "/"
    description = "Latest Volunteering Opportunities"

    def items(self):
        return Position.objects.order_by('-date_created')[:10]

    def item_title(self, item):
        return "%s - %s" % (item.organisation.name, item.name)

    def item_description(self, item):
        return item.summary

    def item_link(self, item):
        return reverse('position-detail', args=[item.pk])

@login_required
def new(request):
    if request.method == "POST":
        position_form = PositionForm(request.POST)
        if position_form.is_valid():
            position = position_form.save(commit=False)
            # The organisation could be normalised out - we also keep a reference to the creating representative, who belongs to the organisation. 
            position.organisation = request.user.get_profile().representativeprofile.organisation
            position.representative = request.user
            position.save()
            position_form.save_m2m()
            messages.info(request, "Your advert has been added to the moderation queue and will be visible to volunteers once the Volunteering admin staff have approved it. If there are any problems with your advert we will contact you by email.")
            return redirect('/')
    else:
        position_form = PositionForm()

    return render_to_response("positions/new.html", {
            'position_form': position_form,
            }, context_instance=RequestContext(request))

@login_required
def edit(request, position_id):
    position = get_object_or_404(Position, pk=position_id)

    if not request.user.get_profile().representativeprofile.organisation == position.organisation and not request.user.is_staff:
        raise Exception("Cannot edit: not the owning organisation of this position.")

    if request.method == "POST":
        position_form = PositionForm(request.POST, instance=position)
        if position_form.is_valid():
            position = position_form.save(commit=False)
            position.approved = False
            position.active = True
            position.save()
            position_form.save_m2m()
            messages.info(request, "Your advert has been updated and resubmitted for approval.")
            return redirect('/')
    else:
        position_form = PositionForm(instance=position)

    return render_to_response("positions/new.html", {
            'position_form': position_form,
            'position': position,
            }, context_instance=RequestContext(request))

def all(request, filter):

    positions = Position.objects.all()

    filter_form = None

    # Columns
    column_filter_form = ColumnFilterForm(request.GET)
    column_filter_form.is_valid()
    columns = column_filter_form.cleaned_data['columns']
    if columns == []:
        columns = POSITION_COLUMN_CHOICES_DEFAULT
    column_filter_form.data = {'columns':columns}

    filter_form = PositionFilterForm()
    if 'filtered' in request.REQUEST:
        filter_form = PositionFilterForm(request.REQUEST)

    category_form = PositionCategoryForm(request.REQUEST)
    if category_form.is_valid():
        if category_form.cleaned_data['category']:
            positions = positions.filter(category__in=category_form.cleaned_data['category'])

    if not request.user.is_staff:
        # Don't show unapproved or delisted positions to non-staff.
        positions = positions.filter(approved=True, active=True)
        # Only allow default columns
        columns = POSITION_COLUMN_CHOICES_DEFAULT
    else:
        if filter_form.is_valid():
            # Approval filtering.
            au = filter_form.cleaned_data['approved']
            if 'a' in au and 'u' in au:
                pass
            elif 'a' in au:
                positions = positions.filter(approved=True)
            elif 'u' in au:
                positions = positions.filter(approved=False)

            # Listing filtering.
            ld = filter_form.cleaned_data['listed']
            if 'l' in ld and 'd' in ld:
                pass
            elif 'l' in ld:
                positions = positions.filter(active=True)
            elif 'd' in ld:
                positions = positions.filter(active=False)

            if settings.FEATURE_ORGANISATION_CATEGORIES and filter_form.cleaned_data['categories']:
                # Category filtering.
                positions = positions.filter(organisation__category__in=filter_form.cleaned_data['categories'])

        else:
            # When there is no filter form, apply defaults.
            positions = positions.filter(active=True)
                
    export_filename = "opportunities_export.xls"

    if filter == 'no-offers':
        # Count how many volunteer-accepted offers each position has,
        # and require the count to be 0.
        positions = positions\
            .exclude(offer__time_volunteer_accepted__isnull=False)
        export_filename = "no_offers_export.xls"

    elif filter == 'five-pending':
        # Count offers that the volunteer has accepted 
        # but the representative didn't accept
        # but that haven't been rejected.
        positions = positions\
            .filter(
                offer__time_volunteer_accepted__isnull=False,
                offer__time_representative_accepted__isnull=True,
                offer__time_withdrawn__isnull=True,
            )\
            .annotate(num_offers=Count('offer'))\
            .filter(num_offers__gte=5)
        export_filename = "five_offers_pending_export.xls"

    if 'export' in request.REQUEST and request.user.is_staff:
        if request.REQUEST['export'] == 'xls':
            return xls.XlsResponse([
                xls.Column("Opportunity", lambda x: x.name),
                xls.Column("Organisation", lambda x: x.organisation.name),
                xls.Column("Representative", lambda x: x.representative.get_full_name()),
                xls.Column("Email", lambda x: x.representative.email),
                ], positions, export_filename)

    return render_to_response("positions/all.html", {
            'positions': positions,
            'filter': filter,
            'filter_form': filter_form,
            'category_form': category_form,
            'cform': column_filter_form,
            'columns': columns,
            }, context_instance=RequestContext(request))

def calendar(request):
    # Get one-off positions ordered by their start date
    positions = Position.objects.filter(
        approved=True, 
        active=True, 
        oneoff=True, 
        date_start__gte=datetime.date.today()
        ).order_by('date_start')

    positions_week = []
    positions_month = []
    positions_later = []

    for position in positions:
        delta = position.date_start - datetime.date.today()

        if position.date_start == datetime.date.today() + datetime.timedelta(days=1):
            position.closeness = "Tomorrow"
            positions_week.append(position)
        elif delta < datetime.timedelta(days=6):
            position.closeness = position.date_start.strftime("%A")
            positions_week.append(position)
        elif delta < datetime.timedelta(days=30):
            positions_month.append(position)
        else:
            positions_later.append(position)

    return render_to_response("positions/calendar.html", {
            'positions': [
                    ['In the next 7 days', positions_week],
                    ['In the next 30 days', positions_month],
                    ['Later', positions_later],
                ],
            }, context_instance=RequestContext(request))

@login_required
def match(request):
    positions = Position.objects.filter(approved=True, active=True, oneoff=False)
    volunteer_hours = request.user.get_profile().volunteerprofile.hours
    
    # For each position, count the number of slots that the position and the volunteer share.
    for position in positions:
        position.matching_slots = position.hours & volunteer_hours
        position.matching_slots_render = position.hours.rendertiny(overlay=volunteer_hours)

    def rank_function(position):
        return position.matching_slots.count()

    # Sort by availability strength
    positions = sorted(positions, key=rank_function, reverse=True)
    # Filter by positions with at least one availability match
    positions = [position for position in positions if position.matching_slots.count() > 0]
    # Skim the top ten
    positions = positions[0:10]
    
    return render_to_response("positions/match.html", {
            'matches': positions,
            }, context_instance=RequestContext(request))

def position(request, position_id):
    position = get_object_or_404(Position, pk=position_id)

    if REQUIRE_REGISTRATION_TO_VIEW_ADVERTS and not request.user.is_authenticated():
        # Redirect the user to the must-register page.
        return redirect_to_login(position.get_absolute_url())

    if not position.approved:
        # The position is not approved, so it should not be publicly viewable.
        allowed = False
        if not request.user.is_authenticated():
            allowed = False
        elif request.user.is_staff:
            allowed = True
        elif request.user.get_profile().is_representative and request.user.get_profile().representativeprofile.organisation == position.organisation:
            allowed = True

        if not allowed:
            # raise Exception("Cannot view unapproved position unless staff admin or representative of organisation.")
            return redirect_to_login(position.get_absolute_url())

    if request.method == "POST":
        # Only a representative of the organisation is allowed to modify the position.
        if not request.user.is_staff and not request.user.get_profile().representativeprofile.organisation == position.organisation:
            raise Exception("Cannot edit: not the owning organisation of this position.")

        if "copy" in request.POST:
            position_form = PositionForm(instance=position)
            return render_to_response("positions/new.html", { 'position_form': position_form }, context_instance=RequestContext(request))

        else:
            # The POST is toggling the "active" property of the position to either de-list or re-list it.
            position.active = request.POST['active'] == "True"
            position.save()

    if request.user.is_staff:
        # Valid volunteer list for admin recommendations.
        volunteers = User.objects.filter(baseprofile__volunteerprofile__id__isnull=False, baseprofile__archived=False).order_by("last_name")
    else:
        volunteers = None

    return render_to_response("positions/position.html", {
            'position': position,
            'notes': get_notes(request, position),
            'volunteers': volunteers,
            }, context_instance=RequestContext(request))

@login_required
def organisations(request):
    return render_to_response("positions/organisations.html", {
            'organisations': Organisation.objects.all(),
            }, context_instance=RequestContext(request))

@login_required
def organisations_autocomplete(request):
    term = request.GET.get('term', '')
    organisations = Organisation.objects.filter(name__icontains=term)[:3]
    response = [ organisation.name for organisation in organisations ]
    httpresponse = HttpResponse(json.dumps(response))
    httpresponse['Content-Type'] = "application/json"
    return httpresponse

@login_required
def organisation(request, organisation_id):
    organisation = get_object_or_404(Organisation, pk=organisation_id)

    template_name = "positions/organisation.html"
    if "print" in request.REQUEST:
        template_name = "positions/organisation_print.html"

    return render_to_response(template_name, {
            'notes': get_notes(request, organisation),
            'organisation': organisation,
            }, context_instance=RequestContext(request))

@login_required
def organisation_primary_image(request, organisation_id):
    organisation = get_object_or_404(Organisation, id=organisation_id)

    path = MEDIA_ROOT+"/img/no-photo.jpg"
    if organisation.primary_image:
        path = organisation.primary_image.path

    data = processor.process(path)    

    return HttpResponse(data, mimetype="image/jpeg")

@login_required
def apply(request, position_id):
    position = get_object_or_404(Position, pk=position_id)
    
    reason = "[No cover letter written]"
    if 'reason' in request.REQUEST:
        reason = request.REQUEST['reason']

    # Count how many positions this volunteer has applied for in the last 24 hours.
    cutoff = datetime.datetime.now() - datetime.timedelta(days=1)
    offers = Offer.objects.filter(volunteer=request.user, time_volunteer_accepted__gt=cutoff)
    # We only count positions where the volunteer accepted BEFORE the staff accepted,
    # because staff recommendations shouldn't count against the limit.
    volunteer_offers = [offer for offer in offers 
        if offer.time_representative_accepted == None
        or offer.time_volunteer_accepted<offer.time_representative_accepted]

    base_profile = get_object_or_404(BaseProfile, user_id=request.user.id)
    volunteer_profile = get_object_or_404(VolunteerProfile, profile_id=base_profile.id)

    if FEATURE_REFERENCE_FILE and not volunteer_profile.referencefile:
        return render_to_response("positions/reference_required.html", locals(), context_instance=RequestContext(request))

    if len(volunteer_offers) >= MAX_OFFERS_PER_24_HOURS:
        # Too many offers.
        return render_to_response("positions/too_many_offers.html", {"MAX_OFFERS": MAX_OFFERS_PER_24_HOURS}, context_instance=RequestContext(request))

    else:
        # Perform the action on a new offer.
        action = RequestPosition(Offer(
                position=position,
                ))

        # Only act if there isn't an existing offer for this volunteer.
        # (This should fix bounce issues where volunteers send two requests accidentally.)
        if request.user not in position.pending_offerers() and request.user not in position.successful_offerers():
            action.do_action(request.user, reason)
        
        messages.info(request, action.response())

    return redirect('/')



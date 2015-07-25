import datetime
import time

from django.shortcuts import render_to_response
from django.template import RequestContext, TemplateDoesNotExist
from django.http import Http404
from reports.forms import DateRangeForm
from positions.models import Position
from blogs.models import Entry, PUBLISHED

def render_page(request, page_name):
    # Get the three newest positions on the site.
    newest_positions = Position.objects.filter(approved=True, active=True).order_by('-date_created', '-id')[:3]

    upcoming_positions = Position.objects.filter(approved=True, active=True, date_start__gt=datetime.date.today()).order_by('date_start')[:3]
    for position in upcoming_positions:
        if position.date_start == datetime.date.today() + datetime.timedelta(days=1):
            position.closeness = "Tomorrow"
        elif position.date_start - datetime.date.today() < datetime.timedelta(days=6):
            position.closeness = position.date_start.strftime("%A")

    blogs = Entry.objects.filter(status=PUBLISHED, publisher__is_staff=True).order_by('-published')[:3]

    try:
        return render_to_response('pages/%s.html' % page_name, {
            'newest_positions': newest_positions,
            'upcoming_positions': upcoming_positions,
            'blogs': blogs,
            'dform': DateRangeForm()
        }, context_instance=RequestContext(request))
    except TemplateDoesNotExist:
        raise Http404("Could not find a template for this page.")
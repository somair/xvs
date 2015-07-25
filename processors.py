from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm

from actions.controller import get_pending_actions
from hours.logic import get_unconfirmed_hours

def tandem_context(request):

    sla = { 'yes': {}, 'no': {} }
    # This helps us restore the SLA when there is an error on the 
    # registration form.
    for field in request.POST:
        if field.startswith("sla_"):
            if request.POST[field] == "yes":
                sla["yes"][field] = True
            else:
                sla["no"][field] = True

    context = { 

        # Deprecated. Use {% url %} instead.
        'BASE_URL': settings.BASE_URL,

        'FRIENDLY_NAME': settings.FRIENDLY_NAME,

        'SUPPORT_EMAIL': settings.SUPPORT_EMAIL,

        'SERVER_EMAIL': settings.SERVER_EMAIL,

        'GOOGLE_MAPS_KEY': settings.GOOGLE_MAPS_KEY,

        # For the login form in the header of every page.
        'loginform': AuthenticationForm(),

        # A list of things that the current user needs to do
        'actions': get_pending_actions(request.user),

        # Unconfirmed hours for the user, if they're a representative.
        'unconfirmed_hours': get_unconfirmed_hours(request.user),

        # Some parts of templates are rendered conditionally
        # based on features that are enabled in the site settings.
        'features': {
            'availability': settings.FEATURE_AVAILABILITY,
            'org_phone_numbers': settings.FEATURE_ORG_PHONE_NUMBERS,
            'cover_letter': settings.FEATURE_COVER_LETTER,
            'volunteer_photos': settings.FEATURE_VOLUNTEER_PHOTOS,
            'cms': settings.FEATURE_CMS,
            'reference_file': settings.FEATURE_REFERENCE_FILE,
            'volunteer_blogs': settings.FEATURE_VOLUNTEER_BLOGS,
            'organisation_blogs': settings.FEATURE_ORGANISATION_BLOGS,
            'site_blog': settings.FEATURE_SITE_BLOG,
            'organisation_header': settings.FEATURE_ORGANISATION_HEADER,
            'organisation_categories': settings.FEATURE_ORGANISATION_CATEGORIES,
            'organisation_volunteer_policies': settings.FEATURE_ORGANISATION_VOLUNTEER_POLICIES,
            'cv': settings.FEATURE_CV,
            'contact_email': settings.FEATURE_CONTACT_EMAIL,
            'how_did_you_hear_options': settings.FEATURE_HOW_DID_YOU_HEAR_OPTIONS,
            'course_list': settings.FEATURE_COURSE_LIST,
            'service_level_agreements': settings.FEATURE_SERVICE_LEVEL_AGREEMENTS,
            'volunteer_address': settings.FEATURE_VOLUNTEER_ADDRESS,
            'volunteer_student_id': settings.FEATURE_VOLUNTEER_STUDENT_ID,
            'volunteer_school': settings.FEATURE_VOLUNTEER_SCHOOL,
            'position_number_of_volunteers': settings.FEATURE_POSITION_NUMBER_OF_VOLUNTEERS,
            'departments': settings.FEATURE_DEPARTMENTS,
            'position_map': settings.FEATURE_POSITION_MAP,
            'travel_expenses': settings.FEATURE_TRAVEL_EXPENSES,
            'organisation_mailouts': settings.FEATURE_ORGANISATION_MAILOUTS,
            'mailouts': settings.FEATURE_MAILOUTS,
            'organisation_confirms_start': settings.FEATURE_ORGANISATION_CONFIRMS_START,
            'allow_hours_for_any_organisation': settings.ALLOW_HOURS_FOR_ANY_ORGANISATION,
            'upcoming_positions': settings.FEATURE_UPCOMING_POSITIONS,
            'categories': settings.FEATURE_CATEGORIES,
            'endorsement': settings.FEATURE_ENDORSEMENT,
            'ga': settings.FEATURE_GA,
            'award': settings.FEATURE_AWARD,
            'login_as': settings.FEATURE_LOGIN_AS,
            'student_id': settings.FEATURE_DISPLAY_STUDENT_ID,
            },

        'sla_checked': sla,
        'dep': int(request.POST['dep']) if 'dep' in request.POST else 0

    }

    return context


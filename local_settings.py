
# Local settings go here. This allows you to override settings on your
# development server, where they need to be different from settings on
# your deployment server. You should never commit changes to this file
# to a remote repository.

import os

INSTANCE_NAME = 'canterbury'
PROJECT_NAME = 'xvs'

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': '%s' % INSTANCE_NAME,
            'USER': 'root',
            'PASSWORD': 'root',
            }
        }

PATH_PREFIX = os.path.dirname(os.path.dirname(__file__))
FEATURE_WORK_EXPERIENCE = True

MEDIA_URL = "http://localhost:8000/media/"

DEBUG = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

SECRET_KEY = '_%@8*2$*1*i&um4+#a6w(%xqa_19=tfmhu9u-l*7t(a$g(2)wg'

FEATURE_TRAINING = True
FEATURE_TRAINING_EVENT = True
FEATURE_MAILOUTS = True
FEATURE_PROFILE_V2 = True

# This is a list of domains that are used to validate student registrations.
# Students will only be allowed to register if their email address ends with
# a string in this list. This is a suffix check, not a domain check, so, for
# instance, 'ed.ac.uk' would allow 's0458553@sms.ed.ac.uk'.
#
# If the list is empty, everybody is allowed to register.
ONLY_ALLOW_EMAIL_ADDRESSES_ENDING_WITH = None

# Sometimes end users should always be referred to the admin staff, never
# XVS support. In that case, this email address is shown.
STAFF_EMAIL = None

# When links in emails encourage people to visit the site, if the link isn't
# a deep link, we use this URL. Normally this is a .xvs.org.uk domain
# but some universities have custom domains and some wrap the entire site
# in an iframe.
HOME_PAGE = None

# Some universities want to use the availability matcher, others don't.
FEATURE_AVAILABILITY = True

# Some universities want organisations to supply phone numbers.
FEATURE_ORG_PHONE_NUMBERS = True

# When students apply for positions, should they write a short covering
# letter to go with their application? A text box is shown with a short
# prompt inviting the volunteer to introduce themselves and explain
# why they'd be good for the position. 
FEATURE_COVER_LETTER = False

# Universities may or may not want it to be possible for unregistered
# visitors to be able to see positions.
REQUIRE_REGISTRATION_TO_VIEW_ADVERTS = False

# Set to True to enable Andy's TinyMCE-based content management system.
FEATURE_CMS = True

# The organisation header allows organisations to show a photo
# and write a rich text description of their organisation.
FEATURE_ORGANISATION_HEADER = True

# Requires organisations to be assigned to categories set by the university.
FEATURE_ORGANISATION_CATEGORIES = False

# Organisation volunteer policies
FEATURE_ORGANISATION_VOLUNTEER_POLICIES = False

# Volunteers can upload photos to their profiles if this feature is
# enabled. We currently warn volunteers that these photos will be
# publicly visible.
FEATURE_VOLUNTEER_PHOTOS = True

# Some universities require the student to upload additional supporting
# documentation before they can apply for opportunities.
FEATURE_REFERENCE_FILE = False

# Some universities want their students to be able to upload CVs.
# These are not mandatory.
FEATURE_CV = False

# Allow students to input an alternative email address to receive emails
# from XVS
FEATURE_CONTACT_EMAIL = False


FEATURE_SITE_BLOG = True

# Only allow phone numbers made of only numerals.
# This means you can't set a phone number with dashes, plus-signs, brackets, etc.
FEATURE_NUMERAL_PHONE_NUMBERS_ONLY = False

# Some universities only want to give a fixed set of options for
# how students heard about the volunteering site.
FEATURE_HOW_DID_YOU_HEAR_OPTIONS = False

# Some universities want students to only be able to select from a
# predefined list of courses.
FEATURE_COURSE_LIST = False

# This enables the advanced Service Level Agreements feature, which
# allows staff administrators to dynamically manage a checklist of
# SLA requirements and verify that reps guarantee the requirements
# when the rep is approved.
FEATURE_SERVICE_LEVEL_AGREEMENTS = False

# Enables and requires the student ID field.
FEATURE_VOLUNTEER_STUDENT_ID = True

# Enables and requires the student address field.
FEATURE_VOLUNTEER_ADDRESS = False

# Some universities want students to identify which school they belong to.
# The student chooses from a dropdown that is populated from the Faculty table.
# NOTE: This feature shouldn't be enabled at the same time as FEATURE_COURSE_LIST.
FEATURE_VOLUNTEER_SCHOOL = True

# Orgs should specify how many volunteers they are seeking when creating
# positions
FEATURE_POSITION_NUMBER_OF_VOLUNTEERS = False

# Some universities want registering organisations to assign themselves
# to parts of the university. We call them departments so that they can
# be different to the faculties that students are asked to choose from.
FEATURE_DEPARTMENTS = False

# Edinburgh University allows opportunity advertisers to show the location
# of the opportunity on a map. Don't enable this for any other universities,
# it needs a custom map key. 
FEATURE_POSITION_MAP = False
GOOGLE_MAPS_KEY = None

# Enables travel expense information for positions.
FEATURE_TRAVEL_EXPENSES = False

# Give organisations the power to send limitless amounts of spam 
# to their volunteers.
FEATURE_ORGANISATION_MAILOUTS = False

# Give staff administrators the power to send limitless amounts of spam 
# to registered users.
FEATURE_MAILOUTS = True

# Some instances require the organisations confirm the volunteer started
# before the volunteer is finally considered to have begun the commitment.
FEATURE_ORGANISATION_CONFIRMS_START = False

# Some instances require the positions to be grouped into categories to 
# help candidates to find suitable positions.
FEATURE_CATEGORIES = False

# The default is the only the representative that created the position
# is emailed about applicants, but some clients like Teesside want all
# representatives for an organisation to be emailed with these updates.
# Set to True to email all reps whenever someone applies to a position.
NOTIFY_ALL_REPS = False

# Allows all volunteers to log hours against any organisation in the
# database, regardless of whether or not they're registered as an
# active volunteer with that organisation.
ALLOW_HOURS_FOR_ANY_ORGANISATION = False

# Some universities want to show opportunities that are happening in
# the next couple of days on their front page.
FEATURE_UPCOMING_POSITIONS = True

# This feature allows reps to leave an endorsement for their volunteers.
FEATURE_ENDORSEMENT = True

# Ability to add Google Analytics. False if disabled, a GA Tracking code if enabled.
# EG. FEATURE_GA = 'UA-12345678-1'
FEATURE_GA = False

# Awards can be given to students based on amount of hours done.
FEATURE_AWARD = True

# New profile layout (for Tees, but can be used by others...)
FEATURE_PROFILE_V2 = True

# Some universities want to be able to login as other users.
FEATURE_LOGIN_AS = True

# Option adds the student ID to volunteer report and export
FEATURE_DISPLAY_STUDENT_ID = True

# Some instances wish to allow non-students to register. In this case,
# the 'R' and 'S' choices can be enabled in the international dropdown.
# If you enable 'R' and 'S' you *must* enable the "None" grad choice.
INTERNATIONAL_CHOICES = (
    ('H', "home student"),
    ('E', "EU student"),
    ('I', "international student"),
#    ('R', "recent graduate"),
    ('S', "staff member"),
)

# The "None" grad choice must be enabled if non-students are allowed
# to register on the system (see INTERNATIONAL_CHOICES)
GRAD_CHOICES = (
    (False, "undergraduate"),
    (True, "postgraduate"),
    (None, "non-student"),
)
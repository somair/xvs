



# Setting up your own XVS instance?
# DO NOT MAKE CHANGES TO THIS FILE
# DO NOT MAKE CHANGES TO THIS FILE
# DO NOT MAKE CHANGES TO THIS FILE
# DO NOT MAKE CHANGES TO THIS FILE
# Place your settings in instance_settings.py and local_settings.py instead.





#################
# SITE SETTINGS #
#################

# Override these settings in instance_settings.py.

# In most cases, the instance name is the name of the university
# and the name of the directory containing the volunteering directory.
# It is used for configuring paths and other defaults - see advanced site 
# settings below.
#
# If the instance is installed at '/srv/example/volunteering', the
# instance is 'example'.
INSTANCE_NAME = 'example'

# This is the friendly name of the XVS instance that is shown in various
# communications, for instance, on the front page, where it says 
# "Welcome to [FRIENDLY_NAME]!"
FRIENDLY_NAME = "XVS OS"

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
FEATURE_CMS = False

# The organisation header allows organisations to show a photo
# and write a rich text description of their organisation.
FEATURE_ORGANISATION_HEADER = False

# Requires organisations to be assigned to categories set by the university.
FEATURE_ORGANISATION_CATEGORIES = False

# Organisation volunteer policies
FEATURE_ORGANISATION_VOLUNTEER_POLICIES = False

# Volunteers can upload photos to their profiles if this feature is
# enabled. We currently warn volunteers that these photos will be
# publicly visible.
FEATURE_VOLUNTEER_PHOTOS = False

# Some universities require the student to upload additional supporting
# documentation before they can apply for opportunities.
FEATURE_REFERENCE_FILE = False

# Some universities want their students to be able to upload CVs.
# These are not mandatory.
FEATURE_CV = False

# Allow students to input an alternative email address to receive emails
# from XVS
FEATURE_CONTACT_EMAIL = False

# Blog features
FEATURE_VOLUNTEER_BLOGS = False
FEATURE_ORGANISATION_BLOGS = False
FEATURE_SITE_BLOG = False

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
FEATURE_VOLUNTEER_STUDENT_ID = False

# Enables and requires the student address field.
FEATURE_VOLUNTEER_ADDRESS = False

# Some universities want students to identify which school they belong to.
# The student chooses from a dropdown that is populated from the Faculty table.
# NOTE: This feature shouldn't be enabled at the same time as FEATURE_COURSE_LIST.
FEATURE_VOLUNTEER_SCHOOL = False

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
FEATURE_MAILOUTS = False

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
FEATURE_UPCOMING_POSITIONS = False

# This feature allows reps to leave an endorsement for their volunteers.
FEATURE_ENDORSEMENT = False

# Ability to add Google Analytics. False if disabled, a GA Tracking code if enabled.
# EG. FEATURE_GA = 'UA-12345678-1'
FEATURE_GA = False

# Awards can be given to students based on amount of hours done.
FEATURE_AWARD = True

# New profile layout (for Tees, but can be used by others...)
FEATURE_PROFILE_V2 = False

# Some universities want to be able to login as other users.
FEATURE_LOGIN_AS = False

# Option adds the student ID to volunteer report and export
FEATURE_DISPLAY_STUDENT_ID = False

# Setting this to true will enable the training module
FEATURE_TRAINING = False
FEATURE_TRAINING_EVENT = False

# Some instances wish to allow non-students to register. In this case,
# the 'R' and 'S' choices can be enabled in the international dropdown.
# If you enable 'R' and 'S' you *must* enable the "None" grad choice.
INTERNATIONAL_CHOICES = (
    ('H', "home student"),
    ('E', "EU student"),
    ('I', "international student"),
#    ('R', "recent graduate"),
#    ('S', "staff member"),
)

# The "None" grad choice must be enabled if non-students are allowed
# to register on the system (see INTERNATIONAL_CHOICES)
GRAD_CHOICES = (
    (False, "undergraduate"),
    (True, "postgraduate"),
#    (None, "non-student"),
)

# If a volunteer has made more than this number of offers
# in the last 24 hours they will not be allowed to make new offers.
MAX_OFFERS_PER_24_HOURS = 3

##########################
# ADVANCED SITE SETTINGS #
##########################

# Override these settings in instance_settings.py as appropriate

ADMINS = (
    #eg. ('Alex Macmillan', 'alex@x13n.com'),
)

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = 'http://localhost:8000/static/'

DATABASES = {}
    
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/London'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-gb'

EMAIL_HOST = "localhost"
EMAIL_PORT = 25
    
# This must match the name of the project directory.
PROJECT_NAME = 'volunteering'
    
# This imports your instance_settings overrides.
from instance_settings import *
from local_settings import *
    
# If the instance settings didn't supply an explicit database
# configuration, set up the default configuration using the instance
# name and database password.
if DATABASES == {}:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': '%s' % INSTANCE_NAME,
            'USER': '%s' % INSTANCE_NAME,
            'PASSWORD': DATABASE_PASSWORD,
            }
        }
    
########################
# DEVELOPMENT SETTINGS #
########################
    
# You should only override these settings in local_settings.py to aid you with
# development.

DEBUG = False

TEMPLATE_DEBUG = DEBUG
    
    
###########################################
# APPLICATION SETTINGS - DO NOT CHANGE!!! #
###########################################

# You should really not need to change these settings when installing an 
# instance of XVS.

MANAGERS = ADMINS

AUTH_PROFILE_MODULE = 'profiles.BaseProfile'

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '%s/%s/media' % (PATH_PREFIX, PROJECT_NAME,)

BASE_URL = '/'

STATIC_URL = "/static/"

STATIC_ROOT = "%s/%s/staticroot/" % (PATH_PREFIX, PROJECT_NAME,)

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = 'http://ws.x13n.com/media/'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.request",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.contrib.messages.context_processors.messages",
    "%s.processors.tandem_context" % PROJECT_NAME,
    "%s.processors.links" % PROJECT_NAME,

)

ROOT_URLCONF = '%s.urls' % PROJECT_NAME

TEMPLATE_DIRS = [
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    "%s/%s/templates" % (PATH_PREFIX, PROJECT_NAME,)
]

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
#    'raven.contrib.django.raven_compat',
#    'debug_toolbar',
    '%s.pages' % PROJECT_NAME,
    'south',
    'djrill',
    'positions',
    'profiles',
    'offers',
    'actions',
    'registration',
    'reports',
    'hours',
    'cms',
    'blogs',
    'mailer',
    'notes',
    'training',
)

ACCOUNT_ACTIVATION_DAYS = 21

# registration
DEFAULT_FROM_EMAIL = SERVER_EMAIL

RAVEN_CONFIG = None

from instance_settings import *
# This imports your local_settings overrides.
try:
    from local_settings import *
except ImportError:
    pass
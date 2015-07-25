

# Instance customisation goes here. This file should be committed to instance
# repos but changes should NOT be committed to the master repo unless you are
# adding new fields.



######################
# MANDATORY SETTINGS #
######################

# You almost certainly must provide new values for these settings in order to
# have a working, secure and usable installation.

INSTANCE_NAME = "example"

ADMINS = (
    # ('Your Name', 'you@example.com'),
)

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = "http://example.com/static/"

# Make this unique, and don't share it with anybody.
# The recommended format is 50 random printable characters.
SECRET_KEY = None

# By default, bot the database username and the database name are assumed
# to be the same as the instance name. Set the database password here.
# If the default database configuration doesn't suit your environment, just
# define DATABASES instead, as per standard Django configuration.
DATABASE_PASSWORD = None

# Anywhere that people are suggested to email support, they will be asked
# to email this address. If XVS is providing support to end users, this should
# be support@xvs.org.uk. Otherwise it should be a university address.
SUPPORT_EMAIL = "support@example.com"

# All emails sent by XVS will be sent from this address.
# All emails should be sent from xvs.org.uk to maximise deliverability.
SERVER_EMAIL = "%s@example.com" % INSTANCE_NAME

######################
# OPTIONAL OVERRIDES #
######################

# eg. ONLY_ALLOW_EMAIL_ADDRESSES_ENDING_WITH = ["aberdeen.ac.uk"]

#####################
# ADVANCED SETTINGS #
#####################

# This is the directory that the volunteering application is contained in.
# ie. if the volunteering application directory is /srv/aberdeen/volunteering,
# PATH_PREFIX should be set to '/srv/aberdeen'
PATH_PREFIX = '/srv/%s' % INSTANCE_NAME
UPLOAD_ROOT = PATH_PREFIX + '/volunteering/uploads'



# Local settings go here. This allows you to override settings on your
# development server, where they need to be different from settings on
# your deployment server. You should never commit changes to this file
# to a remote repository.

import os

INSTANCE_NAME = 'canterbury'
PROJECT_NAME = 'xvs'
PATH_PREFIX = '/home/mauro/BS/%s' % INSTANCE_NAME


DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': '%s' % INSTANCE_NAME,
            'USER': 'root',
            'PASSWORD': 'root',
            'OPTIONS': {
         		"init_command": "SET foreign_key_checks = 0;",
         		},
            }
        }

PATH_PREFIX = os.path.dirname(os.path.dirname(__file__))

MEDIA_URL = "http://ubuntu-vm:8000/media/"

DEBUG = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

SECRET_KEY = '_%@8*2$*1*i&um4+#a6w(%xqa_19=tfmhu9u-l*7t(a$g(2)wg'

FEATURE_TRAINING = True

FEATURE_WORK_EXPERIENCE = True


USE_I18N = False

ONLY_ALLOW_EMAIL_ADDRESSES_ENDING_WITH = 'com'

FEATURE_TRAINING_EVENT = True
FEATURE_MAILOUTS = True




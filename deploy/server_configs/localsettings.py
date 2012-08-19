# -*- coding: utf-8 -*-
import os

PROJECT_NAME = 'TryTry Project'

BASEDIR = os.path.dirname(os.path.realpath(__file__))
DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Roman Imankulov', 'roman.imankulov@gmail.com'),
    ('Pavel Vavilin', 'shtartora@gmail.com'),
)

DEFAULT_FROM_EMAIL = 'try@try-try.me'

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASEDIR, 'sqlite.db'),
    }
}
SECRET_KEY = 'z#@+2a=i&amp;dgckelr!sy340dl@&amp;&amp;j0k)^tny$=nb#%#8-jfztys'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

# Path to module with steps
TRYTRY_FLOWS = {
    'simple_python': 'trytry.simple_python.tests.simple_python',
}
# LXC settings
TRYTRY_LXC_ENABLED = True

# -*- coding: utf-8 -*-
import os

BASEDIR = os.path.dirname(os.path.realpath(__file__))
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Roman Imankulov', 'roman.imankulov@gmail.com'),
    ('Pavel Vavilin', 'shtartora@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASEDIR, 'sqlite.db'),
    }
}
SECRET_KEY = 'PSb3lIO8SIpHsIlq4axbxYRl1XPO6WsKuHlVur32'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

TRYTRY_LXC_ENABLED = False

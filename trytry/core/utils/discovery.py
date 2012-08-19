# -*- coding: utf-8 -*-
# The code is loosely based on django-celery implementation
import imp
import importlib
from django.conf import settings

def discover_flows():
    """
    Return the list of flows for all applications in INSTALLED_APPS
    """
    ret = []
    for app in settings.INSTALLED_APPS:
        app_path = importlib.import_module(app).__path__
        try:
            imp.find_module('steps', app_path)
        except ImportError:
            continue
        ret.append('{0}.steps'.format(app))

# -*- coding: utf-8 -*-
from django.conf import settings

def get_all_flows():
    return getattr(settings, 'TRYTRY_FLOWS', [])

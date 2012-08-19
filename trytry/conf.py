# -*- coding: utf-8 -*-
"""
Configuration settings for try-try
"""
from django.conf import settings
TRYTRY_FLOWS = getattr(settings, 'TRYTRY_FLOWS', {})
TRYTRY_SOFT_TIMEOUT = getattr(settings, 'TRYTRY_SOFT_TIMEOUT', 5)
TRYTRY_HARD_TIMEOUT = getattr(settings, 'TRYTRY_HARD_TIMEOUT', 10)

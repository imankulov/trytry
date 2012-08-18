# -*- coding: utf-8 -*-
from django.conf import settings
from trytry.core.models import Flow


def get_all_flows():
    return getattr(settings, 'TRYTRY_FLOWS', [])


def create_flow(flow_module):
    return Flow.objects.create(flow_module=flow_module)

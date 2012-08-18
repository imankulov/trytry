# -*- coding: utf-8 -*-
from django.conf import settings
from trytry.core.models import Flow


def get_all_flows():
    return getattr(settings, 'TRYTRY_FLOWS', {})


def create_flow(flow_module):
    return Flow.objects.create(flow_module=flow_module)


def get_progress(flow, step):
    step_list = flow.get_flow_settings().steps
    try:
        step_index = step_list.index(step) + 1
    except ValueError:
        return 0
    else:
        return int((float(step_index) / len(step_list)) * 100)

# -*- coding: utf-8 -*-
from django.conf import settings
from trytry.core.models import Flow


def get_all_flows():
    return settings.TRYTRY_FLOWS


def create_flow(flow_module):
    return Flow.objects.create(flow_module=flow_module)


def get_progress(flow):
    step = flow.get_current_step()
    step_list = flow.get_flow_settings().steps
    if flow.state == 'complete':
        return 100
    try:
        step_index = step_list.index(step.name)
    except ValueError:
        return 1
    else:
        result = int((float(step_index) / len(step_list)) * 100)
        if result > 0:
            return result
        return 1


def get_flow_name(module_name):
    reverse_dict = dict([(v, k) for (k, v) in get_all_flows().iteritems()])
    return reverse_dict.get(module_name, settings.TRYTRY_PROJECT_NAME)

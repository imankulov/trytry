# -*- coding: utf-8 -*-
from trytry.core.models import Flow
from trytry.conf import TRYTRY_FLOWS


def get_all_flows():
    return TRYTRY_FLOWS


def create_flow(flow_module):
    return Flow.objects.create(flow_module=flow_module)


def get_progress(flow, step):
    step_list = flow.get_flow_settings().steps
    try:
        step_index = step_list.index(step) + 1
    except ValueError:
        return 1
    else:
        result = int((float(step_index) / len(step_list)) * 100)
        if result > 0:
            return result
        return 1


def get_flow_name(module_name):
    print module_name
    reverse_dict = dict([(v, k) for (k, v) in TRYTRY_FLOWS.iteritems()])
    return reverse_dict.get(module_name)

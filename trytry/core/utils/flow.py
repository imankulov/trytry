# -*- coding: utf-8 -*-
import importlib
from django.conf import settings
from trytry.core.models import Flow


_flows = None
def get_all_flows():
    global _flows
    if _flows is None:
        _flows = []
        for app in settings.INSTALLED_APPS:
            steps_module_name = '{0}.steps'.format(app)
            try:
                mod = importlib.import_module(steps_module_name)
            except ImportError:
                continue
            if hasattr(mod, '__flow__'):
                _flows.append(steps_module_name)
    return _flows

def create_flow(flow_module):
    return Flow.objects.create(flow_module=flow_module)


def get_progress(flow):
    step = flow.get_current_step()
    step_list = flow.get_flow_settings().steps
    if flow.state in ('complete', 'destroyed'):
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

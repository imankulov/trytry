# -*- coding: utf-8 -*-
from trytry.core.models import Flow
from trytry.core.utils import create_flow, get_progress, wrap_json


def simple_python_get_task(request):
    id = request.session.get('simple_python_flow_id', None)
    if id:
        flow = Flow.objects.get(id=id)
    else:
        flow = create_flow('trytry.simple_python.steps')
    step = flow.get_current_step()
    return wrap_json({
        'task': step.get_task(),
        'progress': get_progress(flow, step),
        'flow_name': str(flow),
        'step_prompt': step.prompt
    })

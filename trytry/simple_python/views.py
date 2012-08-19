# -*- coding: utf-8 -*-
from trytry.core.models import Flow
from trytry.core.utils import create_flow, get_progress, wrap_json


def simple_python_get_task(request):
    id = request.session.get('simple_python_flow_id', None)
    if id:
        flow = Flow.objects.get(id=id)
    else:
        flow = create_flow('trytry.simple_python.steps')
        flow.setup_flow()
        request.session['simple_python_flow_id'] = flow.id
    command_result = {}
    if request.method == 'POST':
        data = request.POST.copy()
        command_result = flow.apply(data.get('command'))
    result = {
        'task': flow.get_task(),
        'progress': get_progress(flow),
        'flow_name': str(flow),
        'step_prompt': flow.get_prompt()
    }
    result.update(command_result)
    return wrap_json(result)

# -*- coding: utf-8 -*-
import importlib
from django.shortcuts import render
from trytry.core.utils import get_all_flows
from django.views.decorators.csrf import ensure_csrf_cookie


@ensure_csrf_cookie
def index(request):
    flow = request.GET.get('flow', None)
    all_flows = _generate_flow_dict()
    if not flow or flow not in all_flows:
        flow = None
    return render(request, 'core/index.html',
                  {'all_flows': all_flows, 'flow': all_flows.get(flow, None)})


from trytry.core.models import Flow
from trytry.core.utils import create_flow, get_progress, wrap_json


def get_task(request, ):
    id = request.session.get('simple_python_flow_id', None)
    try:
        flow = Flow.objects.get(id=id)
    except Flow.DoesNotExist:
        flow = create_flow('trytry.simple_python.steps')
        flow.setup_flow()
        request.session['simple_python_flow_id'] = flow.id
    command_result = {}
    if request.method == 'POST':
        data = request.POST.copy()
        # navigate through steps
        if data.get('navigate'):
            if data['navigate'] == 'prev':
                flow.current_step = flow.get_prev_step_name()
                flow.state = 'active'
            elif data['navigate'] == 'next':
                current_step = flow.get_next_step_name()
                if current_step is None:
                    flow.state = 'complete'
                else:
                    flow.current_step = current_step
                    flow.state = 'active'
            flow.save()
            print flow.__dict__
        if data.get('command'):
            command_result = flow.apply(data.get('command'))
    result = {
        'task': flow.get_task(),
        'progress': get_progress(flow),
        'flow_name': str(flow),
        'step_prompt': flow.get_prompt()
    }
    result.update(command_result)
    return wrap_json(result)


def _generate_flow_dict():
    all_flows = {}
    for module in get_all_flows():
        mod = importlib.import_module(module)
        settings = getattr(mod, '__flow__', dict())
        all_flows.update({settings['url']: settings})
    return all_flows

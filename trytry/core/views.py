# -*- coding: utf-8 -*-
import importlib
from trytry.core.models import Flow
from trytry.core.utils import get_all_flows
from django.shortcuts import render, redirect
from django.views.decorators.csrf import ensure_csrf_cookie
from trytry.core.utils import create_flow, get_progress, wrap_json


@ensure_csrf_cookie
def index(request):
    flow = request.GET.get('flow', None)
    all_flows = _generate_flow_dict()
    if not flow or flow not in all_flows:
        flow = None
    template = 'core/flow.html' if flow else 'core/dashboard.html'
    return render(request, template,
                  {'all_flows': all_flows,
                   'flow': all_flows.get(flow, None)})


def get_task(request, flow_name):
    flow = _get_flow(request, flow_name)
    if flow is None:
        flow = create_flow('trytry.{0}.steps'.format(flow_name))
        flow.setup_flow()
        request.session['{0}_flow_id'.format(flow_name)] = flow.id
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


def get_status(request, flow_name):
    flow = _get_flow(request, flow_name)
    if flow is None:
        return redirect('/')
    log_list = flow.log_set.all().order_by('timestamp')
    template = 'core/status.html'
    return render(request, template, {'log_list': log_list, 'progress': get_progress(flow)})


def _get_flow(request, flow_name):
    id = request.session.get('{0}_flow_id'.format(flow_name), None)
    try:
        flow = Flow.objects.get(id=id)
    except Flow.DoesNotExist:
        return None
    else:
        return flow


def _generate_flow_dict():
    all_flows = {}
    for module in get_all_flows():
        mod = importlib.import_module(module)
        settings = getattr(mod, '__flow__', dict())
        all_flows.update({settings['url']: settings})
    return all_flows

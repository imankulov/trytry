# -*- coding: utf-8 -*-
from django.shortcuts import render
from trytry.core.utils import get_all_flows
from django.views.decorators.csrf import ensure_csrf_cookie


@ensure_csrf_cookie
def index(request):
    flow = request.GET.get('flow', None)
    all_flows = get_all_flows().keys()
    if not flow or flow not in all_flows:
        flow = None
    return render(request, 'core/index.html',
                  {'all_flows': all_flows, 'flow_name': flow})

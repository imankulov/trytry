# -*- coding: utf-8 -*-
from django.shortcuts import render
from trytry.core.utils import get_all_flows


def index(request):
    flow = request.GET.get('flow', None)
    all_flows = get_all_flows().keys()
    flow_name = None
    if flow and flow in all_flows:
        flow_name = "trytry.{0}.views".format(flow)
    return render(request, 'core/index.html', {'all_flows': all_flows, 'flow_name': flow_name})

# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from trytry.core.utils import get_all_flows


def index(request):
    flow = request.GET.get('flow', None)
    all_flows = get_all_flows().keys()
    if flow and flow in all_flows:
        view = "trytry.%(flow)s.views.%(flow)s_get_task" % {'flow': flow}
        return HttpResponseRedirect(reverse(view))
    return render(request, 'core/index.html', {'all_flows': all_flows})

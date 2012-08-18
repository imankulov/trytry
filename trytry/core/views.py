# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from trytry.core.utils import get_all_flows


def index(request):
    flow = request.GET.get('flow', None)
    if flow and flow in get_all_flows().keys():
        view = "trytry.%(flow)s.views.%(flow)s_get_task" % {'flow': flow}
        return HttpResponseRedirect(reverse(view))
    return render(request, 'core/index.html', {})

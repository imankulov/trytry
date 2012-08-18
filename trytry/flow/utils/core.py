# -*- coding: utf-8 -*-
from trytry.flow.models import Flow


def create_flow(flow_module):
    return Flow.objects.create(flow_module=flow_module)

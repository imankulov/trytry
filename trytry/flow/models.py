# -*- coding: utf-8 -*-
import importlib
from django.db import models


class Flow(models.Model):

    flow_module = models.CharField(u'Module who have this flow', max_length=256)
    current_step = models.CharField(u'Step class name', max_length=256, default='Step1')

    def get_current_step(self):
        mod = importlib.import_module(self.flow_module)
        return getattr(mod, self.current_step)()

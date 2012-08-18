# -*- coding: utf-8 -*-
import importlib
from django.db import models
from dotdict import dotdict


class Flow(models.Model):

    STATE_CHOICES = (
        ('active', 'active'),
        ('complete', 'complete'),
    )

    flow_module = models.CharField(u'Module who have this flow', max_length=256)
    current_step = models.CharField(u'Step class name', max_length=256)
    state = models.CharField(u'Flow state', choices=STATE_CHOICES,
                             default='active', max_length=64)

    def apply(self, user_input):
        ret = self.get_current_step()(user_input)
        if ret['goto_next']:
            next_step_name = self.get_next_step_name()
            if next_step_name:
                self.current_step = next_step_name
            else:
                self.state = 'complete'
            self.save()
        return ret

    def get_current_step(self):
        mod = self.get_flow_module()
        return getattr(mod, self.current_step)()

    def get_prev_step(self):
        prev_step_name = self.get_prev_step_name()
        if prev_step_name:
            return getattr(self.get_flow_module(), prev_step_name)()

    def get_prev_step_name(self):
        steps = self.get_flow_settings().steps
        try:
            idx = steps.index(self.current_step)
        except ValueError:
            return None
        if idx == 0:
            return None
        return steps[idx - 1]

    def get_next_step(self):
        next_step_name = self.get_next_step_name()
        if next_step_name:
            return getattr(self.get_flow_module(), next_step_name)()

    def get_next_step_name(self):
        steps = self.get_flow_settings().steps
        try:
            idx = steps.index(self.current_step)
        except ValueError:
            return None
        if idx + 1 == len(steps):
            return None
        return steps[idx + 1]


    def get_flow_module(self):
        if not hasattr(self, '_mod'):
            self._mod = importlib.import_module(self.flow_module)
        return self._mod

    def get_flow_settings(self):
        flow = self.get_flow_module().__flow__
        return dotdict(flow)

    def save(self, *args, **kwargs):
        if not self.current_step:
            self.current_step = self.get_flow_settings().steps[0]
        super(Flow, self).save(*args, **kwargs)


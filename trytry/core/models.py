# -*- coding: utf-8 -*-
import importlib
from dotdict import dotdict
from django.db import models


class Flow(models.Model):

    STATE_CHOICES = (
        ('new', 'new'),
        ('active', 'active'),
        ('complete', 'complete'),
        ('destroyed', 'destroyed'),
    )

    flow_module = models.CharField(u'Module who have this flow', max_length=256)
    current_step = models.CharField(u'Step class name', max_length=256)
    state = models.CharField(u'Flow state', choices=STATE_CHOICES,
                             default='new', max_length=64)

    def __str__(self):
        from trytry.core.utils import get_flow_name
        return get_flow_name(self.flow_module)

    def apply(self, user_input):
        if self.state != 'active':
            raise RuntimeError('Unable to execute command, as the flow is '
                               'in {0} state'.format(self.state))
        ret = self.get_current_step()(user_input)
        if ret['goto_next']:
            next_step_name = self.get_next_step_name()
            if next_step_name:
                self.current_step = next_step_name
            else:
                self.state = 'complete'
            self.save()
        return ret

    def get_task(self):
        return self.get_current_step().get_task()

    def get_prompt(self):
        return self.get_current_step().prompt

    def get_current_step(self):
        mod = self.get_flow_module()
        return getattr(mod, self.current_step)(self)

    def get_prev_step(self):
        prev_step_name = self.get_prev_step_name()
        if prev_step_name:
            return getattr(self.get_flow_module(), prev_step_name)(self)

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
            return getattr(self.get_flow_module(), next_step_name)(self)

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

    def setup_flow(self):
        """
        Execute function defined in __flow__['setup']
        """
        self._exec_flow_function('setup', (self, ))
        self.state = 'active'
        self.save()

    def teardown_flow(self):
        """
        Execute function defined in __flow__['teardown']
        """
        self._exec_flow_function('teardown', (self, ))
        self.state = 'destroyed'
        self.save()

    def _exec_flow_function(self, func_key, args=None, kwargs=None):
        """
        Helper function. Execute function by its key in __flow__ dict
        """
        flow_mod = self.get_flow_module()
        flow_conf = flow_mod.__flow__
        if func_key in flow_conf:
            func = getattr(flow_mod, flow_conf[func_key])
            args = args or ()
            kwargs = kwargs or {}
            return func(*args, **kwargs)

    def save(self, *args, **kwargs):
        if not self.current_step:
            self.current_step = self.get_flow_settings().steps[0]
        super(Flow, self).save(*args, **kwargs)

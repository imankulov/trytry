# -*- coding: utf-8 -*-
from django.test import TestCase
from trytry.core.utils.flow import create_flow
from trytry.core.utils.lxc import lxc_wrap

class LXCTest(TestCase):

    def setUp(self):
        self.flow_obj = create_flow('trytry.simple_python.tests.simple_python')

    def test_lxc_wrap(self):
        cmd = ['bash', ]
        wrapped_cmd = lxc_wrap(self.flow_obj, cmd)
        expected_cmd = ['sudo', 'bash', '-c',
                        ('timelimit -p -q -t 5 -T 10 -- '
                        'lxc-wait -n flow_{0} -s STOPPED && '
                        'timelimit -t 5 -T 10 -- lxc-start -n flow_{0} -- bash'
                        ).format(self.flow_obj.id)]
        self.assertEqual(wrapped_cmd, expected_cmd)

    def tearDown(self):
        self.flow_obj.delete()

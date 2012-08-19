# -*- coding: utf-8 -*-
import os
from django.test import TestCase
from trytry.simple_bash.tests.simple_bash import Step1
from trytry.core.utils.flow import create_flow


class TimeoutTest(TestCase):

    def setUp(self):
        self.step = Step1()

    def test_timeout_ok(self):
        with self.settings(TRYTRY_SOFT_TIMEOUT=3,
                           TRYTRY_HARD_TIMEOUT=3):
            ret = self.step('sleep 0.3; echo "hello world"')
            self.assertEqual(ret.ok_text, 'hello world')

    def test_timeout_fail(self):
        with self.settings(TRYTRY_SOFT_TIMEOUT=0.1,
                           TRYTRY_HARD_TIMEOUT=0.2):
            ret = self.step('sleep 0.3 ; echo "hello world"')
            self.assertEqual(ret.ok_text, None)


class SetupTearDownTest(TestCase):

    def setUp(self):
        if os.path.isfile('.simple_bash'):
            os.unlink('.simple_bash')

    def tearDown(self):
        self.setUp()

    def test_setup_teardown(self):
        flow = create_flow('trytry.simple_bash.tests.simple_bash')
        flow.setup_flow()
        self.assertTrue(os.path.isfile('.simple_bash'))
        flow_id = int(open('.simple_bash').read())
        self.assertEqual(flow_id, flow.id)
        flow.teardown_flow()
        self.assertFalse(os.path.isfile('.simple_bash'))

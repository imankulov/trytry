# -*- coding: utf-8 -*-
from django.test import TestCase
from trytry.simple_bash.tests.simple_bash import Step1
from trytry.core.utils import get_all_flows


class TimeoutTest(TestCase):

    def setUp(self):
        self.step = Step1()

    def test_timeout_ok(self):
        with self.settings(TRYTRY_SOFT_TIMEOUT=3,
                           TRYTRY_HARD_TIMEOUT=3):
            ret = self.step('sleep 1; echo "hello world"')
            self.assertEqual(ret.ok_text, 'hello world')

    def test_timeout_fail(self):
        with self.settings(TRYTRY_SOFT_TIMEOUT=0.1,
                           TRYTRY_HARD_TIMEOUT=0.2):
            ret = self.step('sleep 0.3 ; echo "hello world"')
            self.assertEqual(ret.ok_text, None)

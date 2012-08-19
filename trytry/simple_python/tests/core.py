# -*- coding: utf-8 -*-
from django.test import TestCase
from trytry.core.utils import create_flow
from trytry.simple_python.tests.simple_python import Step1, Step2
from trytry.core.utils import get_all_flows


class PythonStep1Test(TestCase):

    def setUp(self):
        self.step = Step1()

    def test_step1_ok(self):
        ret = self.step('print "hello world"')
        self.assertEqual(ret.ok_text, 'hello world')
        self.assertEqual(ret.err_text, None)
        self.assertTrue(ret.goto_next)

    def test_step1_exception(self):
        ret = self.step('print hello world')
        self.assertEqual(ret.ok_text, None)
        self.assertNotEqual(ret.err_text, None)
        self.assertFalse(ret.goto_next)

    def test_step1_wrong_text(self):
        ret = self.step('print "hello world!"')
        self.assertEqual(ret.ok_text, 'hello world!')
        self.assertEqual(ret.err_text, None)
        self.assertFalse(ret.goto_next)


class StateSaveTest(TestCase):

    def setUp(self):
        self.step = Step1()

    def test_step1_ok(self):
        ret = self.step('a = 1')
        self.assertEqual(ret.err_text, None)
        ret = self.step('print a')
        self.assertEqual(ret.err_text, None)
        self.assertEqual(ret.ok_text, '1')


class FlowTest(TestCase):

    def test_create_flow(self):
        flow = create_flow('trytry.simple_python.tests.simple_python')
        self.assertIsInstance(flow.get_current_step(), Step1)
        self.assertIsInstance(flow.get_next_step(), Step2)
        self.assertEqual(flow.get_prev_step(), None)


class FlowPassTest(TestCase):

    def test_pass_flow(self):
        flow = create_flow('trytry.simple_python.tests.simple_python')
        # step 1
        result = flow.apply('print "hello world"')
        self.assertTrue(result.goto_next)
        self.assertEqual(flow.current_step, 'Step2')
        # step 2, wrong action
        result = flow.apply('print "hello world"')
        self.assertFalse(result.goto_next)
        self.assertEqual(flow.current_step, 'Step2')
        # step 2
        result = flow.apply('print 1 + 1')
        self.assertTrue(result.goto_next)
        self.assertEqual(flow.current_step, 'Step2')
        #self.assertEqual(flow.state, 'complete')


class FlowDiscoveryTest(TestCase):

    TRYTRY_FLOWS = {
        'simple_python': 'trytry.simple_python.tests.simple_python',
    }

    def test_all_flows(self):
        with self.settings(TRYTRY_FLOWS=self.TRYTRY_FLOWS):
            self.assertEqual(get_all_flows(), self.TRYTRY_FLOWS)
# -*- coding: utf-8 -*-
from django.utils.unittest import TestCase
from trytry.flow.utils import create_flow
from trytry.flow.tests.simple_python import Step1


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
        flow = create_flow('trytry.flow.tests.simple_python')
        current_step = flow.get_current_step()
        self.assertTrue(isinstance(current_step, Step1))

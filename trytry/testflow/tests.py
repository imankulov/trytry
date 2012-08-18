# -*- coding: utf-8 -*-
from django.utils.unittest import TestCase
from trytry.simple_python_flow.test_flow import SimplePythonFlow


class TestFlowTest(TestCase):

    def setUp(self):
        self.flow = SimplePythonFlow()
        self.flow.install()

    def test_step1_ok(self):
        ret = self.flow.step1('print "hello world"')
        self.assertEqual(ret.ok_text, 'hello world')
        self.assertEqual(ret.err_text, None)
        self.assertTrue(ret.goto_next)

    def test_step1_exception(self):
        ret = self.flow.step1('print hello world')
        self.assertEqual(ret.ok_text, None)
        self.assertNotEqual(ret.err_text, None)
        self.assertFalse(ret.goto_next)

    def test_step1_wrong_text(self):
        ret = self.flow.step1('print "hello world!"')
        self.assertEqual(ret.ok_text, 'hello world!')
        self.assertEqual(ret.err_text, None)
        self.assertFalse(ret.goto_next)

    def tearDown(self):
        self.flow.destroy()
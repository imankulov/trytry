from django.test import TestCase
from trytry.core.utils.call import call


class CallTest(TestCase):

    def test_call_string(self):
        cmd = "echo 'hello\"world'"
        out, _, _ = call(cmd)
        self.assertEqual(out, 'hello"world')

    def test_call_list(self):
        cmd = ['echo', 'hello"world']
        out, _, _ = call(cmd)
        self.assertEqual(out, 'hello"world')

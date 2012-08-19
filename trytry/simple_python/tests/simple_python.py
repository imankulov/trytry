# -*- coding: utf-8 -*-
from trytry.simple_python.steps import GenericPythonStep
from trytry.core.utils.lxc import lxc_setup, lxc_teardown


__flow__ = {
    'steps': ['Step1', 'Step2'],
    'lxc_container': 'python',
    'setup': 'lxc_setup',
    'teardown': 'lxc_teardown',
}


class Step1(GenericPythonStep):
    """
    Exersise #1
    ----

    * Write "hello world", son of a bitch!
        - print "hello world"
        - print("hello world")
    """

    expected_out = 'hello world'
    on_success_hint = ('Congratulations! You rules! '
                       'Your first Python program work! '
                       'Let\'s go to the next level of knowledge')
    on_wrong_out_hint = ("It's nice, but we asked you to write hello "
                         "world")


class Step2(GenericPythonStep):
    """
    Then show me what is 1 + 1, son of a bitch!
    """

    expected_out = '2'
    on_success_hint = ("Congratulations! You rules! "
                       "You know the maths. That's all for now")
    on_wrong_out_hint = ("It's nice, but we asked you to write 1 + 1")

# -*- coding: utf-8 -*-
from trytry.flow.steps import GenericPythonStep


class Step1(GenericPythonStep):
    """
    Write "hello world", son of a bitch!
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

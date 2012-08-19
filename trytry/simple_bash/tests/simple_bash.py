# -*- coding: utf-8 -*-
from trytry.simple_bash.steps import GenericBashStep


__flow__ = {
    'steps': ['Step1', ],
}


class Step1(GenericBashStep):
    """
    Write "hello world"
    """
    expected_out = 'hello world'
    on_success_hint = ('Congratulations! You rules! '
                       'Your first Bash program work! '
                       'Let\'s go to the next level of knowledge')
    on_wrong_out_hint = ("It's nice, but we asked you to write hello "
                         "world")

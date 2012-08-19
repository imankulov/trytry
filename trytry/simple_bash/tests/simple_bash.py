# -*- coding: utf-8 -*-
import os
from trytry.simple_bash.steps import GenericBashStep


__flow__ = {
    'steps': ['Step1', ],
    'setup': 'setup',
    'teardown': 'teardown',
    'lxc_container': 'bash',
}


def setup(flow_obj):
    with open('.simple_bash', 'w') as fd:
        fd.write(str(flow_obj.id))

def teardown(flow_obj):
    if os.path.isfile('.simple_bash'):
        os.unlink('.simple_bash')

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

# -*- coding: utf-8 -*-
from trytry.core.steps import GenericStep
from trytry.core.utils.lxc import lxc_setup, lxc_teardown

__flow__ = {
    'steps': ['Step1', ],
    'lxc_container': 'python',
    'setup': lxc_setup,
    'teardown': lxc_teardown,
    'name': 'Simple Bash',
    'url': 'simple_bash'
}


class GenericBashStep(GenericStep):
    prompt = u'$ '

    def get_command(self, user_input):
        return (['bash', ], user_input)


class Step1(GenericBashStep):
    """
    Excersise #1
    ----

    """
    name = "Step1"
    expected_out = "Hello World"
    on_success_hint = u'Well done!'
    on_wrong_out_hint = u"Let's try again!"

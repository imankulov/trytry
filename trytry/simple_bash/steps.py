# -*- coding: utf-8 -*-
"""
bash is a very exciting language. You probably cannot even imagine how
difficult and elegant it can be.

Let's play with some variables first, and then move on.
"""
from trytry.core.steps import GenericStep
from trytry.core.utils.lxc import lxc_setup, lxc_teardown

__flow__ = {
    'steps': ['Step1', ],
    'lxc_container': 'python',
    'setup': lxc_setup,
    'teardown': lxc_teardown,
    'name': 'Simple Bash',
    'url': 'simple_bash',
    'description': __doc__,
}


class GenericBashStep(GenericStep):
    prompt = u'# '

    def get_command(self, user_input):
        # if there is a pre-saved state, then make sure it
        # is loaded into the interpreter
        prefix_lines = [
            'test -f .bash_state && source .bash_state',
        ]
        # Make sure that we save the state to the file after the command
        # execution
        forbidden_variables = [
            'BASHOPTS',
            'BASH_VERSINFO',
            'EUID',
            'PPID',
            'SHELLOPTS',
            'UID'
        ]
        suffix_lines = [
            'set |egrep -v "{0}"  > .bash_state'.format('|'.join(forbidden_variables))
        ]
        command = prefix_lines + [user_input, ] + suffix_lines + ['', ]
        return (['bash', ], '\n'.join(command))


class Step1(GenericBashStep):
    """
    In the simplest case, a script is nothing more than a list of system commands stored in a file. At the very least, this saves the effort of retyping that particular sequence of commands each time it is invoked.

    Example 2-1. cleanup: A script to clean up log files in /var/log

    # Cleanup
    # Run as root, of course.

    cd /var/log
    cat /dev/null > messages
    cat /dev/null > wtmp
    echo "Log files cleaned up."

    There is nothing unusual here, only a set of commands that could just as easily have been invoked one by one from the command-line on the console or in a terminal window. The advantages of placing the commands in a script go far beyond not having to retype them time and again. The script becomes a program -- a tool -- and it can easily be modified or customized for a particular application.
    """
    name = "Step1"
    expected_out = "Hello World"
    on_success_hint = u'Well done!'
    on_wrong_out_hint = u"Let's try again!"

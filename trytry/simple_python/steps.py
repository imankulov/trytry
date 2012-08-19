# -*- coding: utf-8 -*-
from trytry.core.steps import GenericStep


__flow__ = {
    'steps': ['Step1', 'Step2'],
    'lxc_container': 'python',
}


class GenericPythonStep(GenericStep):
    prompt = u'>>> '

    def get_command(self, user_input):
        # if there is a pre-saved state, then make sure it
        # is loaded into the interpreter
        prefix_lines = [
            '# -*- coding: utf-8 -*-',
            'import os, cPickle as pickle',
            'if os.path.isfile(".python_state"):',
            '    _state = pickle.load(open(".python_state"))',
            '    locals().update(_state)',
            '    del _state',
        ]
        # Make sure that we save the state to the file after the command
        # execution
        suffix_lines = [
            '_state = {}',
            'for k, v in locals().items():',
            '    if k == "_state":',
            '        continue',
            '    try: pickle.dumps(v)',
            '    except Exception: continue',
            '    _state[k] = v',
            'fd = open(".python_state", "w")',
            'pickle.dump(_state, fd)',
            'fd.close()'
        ]
        command = prefix_lines + [user_input, ] + suffix_lines + ['', ]
        # return the command and stdin
        cmd = ['bash', '-c', 'PYTHONIOENCODING=UTF-8 python']
        return (cmd, '\n'.join(command))


class Step1(GenericPythonStep):
    """
    Exercise #1
    ----

    In this exercise, you will need to print "Hello World!".
    """
    step = "Step1"
    expected_out = "Hello World!"
    on_success_hint = u'Congratulation!'
    on_wrong_out_hint = u'Try to print "Hello World!"'


class Step2(GenericPythonStep):
    """
    Exercise #2
    ----

    In this excersise, you will need to calculate 2 + 2.
    """
    name = "Step2"
    expected_out = "4"
    on_success_hint = u'Well done!'
    on_wrong_out_hint = u'Try to print 2 + 2'

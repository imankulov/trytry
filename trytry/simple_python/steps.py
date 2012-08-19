# -*- coding: utf-8 -*-
from trytry.core.steps import GenericStep


__flow__ = {
    'steps': ['Step1', 'Step2'],
}


class GenericPythonStep(GenericStep):
    prompt = u'>>> '

    def get_command(self, user_input):
        # if there is a pre-saved state, then make sure it
        # is loaded into the interpreter
        prefix_lines = [
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
        return (['python', ], '\n'.join(command))


class Step1(GenericPythonStep):
    """
    Exercise #1
    ----

    In this exercise, you will need to change the code in the left box so it will print out "Hello, World!" instead of "Goodbye, World!".
    """
    pass

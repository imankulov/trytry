# -*- coding: utf-8 -*-
import os
import pickle
import tempfile
import subprocess as subp
from django.core.cache import cache
from trytry.core.steps import GenericStep


__flow__ = {
    'steps': ['Step1', 'Step2'],
}


class GenericPythonStep(GenericStep):
    on_err_hint = ("Oh my God! Something goes wrong. Try read "
                   "instruction more carefully and perform the "
                   "task more diligently. Remember, I'm watching "
                   "you.")

    def run_command(self, user_input):
        state_filename = self.restore_state_to_file()
        q_state_filename = repr(state_filename)
        # if there is a pre-saved state, then make sure it
        # is loaded into the interpreter
        prefix_lines = [
            'import cPickle as pickle',
            '_state = pickle.load(open({0}))'.format(q_state_filename),
            'locals().update(_state)',
            'del _state',
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
            'fd = open({0}, "w")'.format(q_state_filename),
            'pickle.dump(_state, fd)',
            'fd.close()'
        ]
        command = prefix_lines + [user_input, ] + suffix_lines + ['', ]
        # run the command
        pipe = subp.Popen(['python', ],
                          stdin=subp.PIPE,
                          stdout=subp.PIPE,
                          stderr=subp.PIPE)
        out, err = pipe.communicate('\n'.join(command))
        # save the new state to cache
        self.store_state_from_file(state_filename)
        # return the result
        out = out.rstrip() or None
        err = err.rstrip() or None
        return out, err, pipe.returncode

    def get_cache_key(self):
        cache_key = 'step_state:{0}'.format(self.get_uuid())
        return cache_key

    def restore_state_to_file(self):
        stored_state = cache.get(self.get_cache_key())
        if stored_state is None:
            stored_state = pickle.dumps({})
        fdesc, filename = tempfile.mkstemp()
        fd = os.fdopen(fdesc, 'w')
        fd.write(stored_state)
        fd.close()
        return filename

    def store_state_from_file(self, filename):
        with open(filename) as fd:
            cache.set(self.get_cache_key(), fd.read())
        os.unlink(filename)


class Step1(GenericPythonStep):
    """
    Exercise #1
    ----

    In this exercise, you will need to change the code in the left box so it will print out "Hello, World!" instead of "Goodbye, World!".
    """
    pass

# -*- coding: utf-8 -*-
from trytry.flow.steps import GenericStep
from django.core.cache import cache
import subprocess as subp
import tempfile
import os
import pickle


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
        command = prefix_lines + [user_input,] + suffix_lines + ['',]
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
        return 'hello'
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
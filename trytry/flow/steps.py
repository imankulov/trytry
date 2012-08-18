# -*- coding: utf-8 -*-
import os
import uuid
import pickle
import tempfile
import subprocess as subp
from dotdict import dotdict
from django.core.cache import cache


class GenericStep(object):

    expected_out = None
    on_success_hint = None
    on_wrong_out_hint = None
    on_err_hint = None

    def __call__(self, user_input):
        out, err, returncode = self.run_command(user_input)
        json_result = self.analyze(out, err, returncode)
        return json_result

    def get_uuid(self):
        if not hasattr(self, '_uuid'):
            self._uuid = str(uuid.uuid4())
        return self._uuid

    def run_command(self, user_input):
        command = self.get_command(user_input)
        pipe = subp.Popen(command, stdout=subp.PIPE, stderr=subp.PIPE)
        out, err = pipe.communicate()
        out = out.rstrip() or None
        err = err.rstrip() or None
        return out, err, pipe.returncode

    def get_command(self, user_input):
        """
        Return a tuple ([command, to, execute], "stdin")
        """
        raise NotImplementedError('Must be implemented in subclass')

    def analyze(self, out, err, returncode):
        ret = {
            'goto_next': False,
            'hint': None,
            'ok_text': out,
            'err_text': err,
        }
        if out and out.lower() == self.expected_out:
            ret['hint'] = self.on_success_hint
            ret['goto_next'] = True
        elif err:
            ret['hint'] = self.on_err_hint
        else:
            ret['hint'] = self.on_wrong_out_hint
        return dotdict(ret)

    def get_task(self):
        return self.__doc__


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

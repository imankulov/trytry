# -*- coding: utf-8 -*-
import re
import sys
import uuid
import markdown
import subprocess as subp
from dotdict import dotdict
from django.utils.encoding import smart_unicode


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
        docstring = self.__doc__
        return self.render(docstring)

    def render(self, context):
        def count_shiftlen(s):
            if s.strip():
                return len(r.match(s).group(0))
            else:
                return sys.maxint
        output = smart_unicode(context)
        # Отрезаем начало у каждой из строк
        # (пустые строки не учитываются при подсчете shiftlen)
        r = re.compile('^ *')
        lines = output.splitlines()
        if not lines:
            return ''
        shiftlen = min(
            map(count_shiftlen, lines)
        )
        lines = [l[shiftlen:] for l in lines]
        output = u'\n'.join(lines)
        return markdown.markdown(output)

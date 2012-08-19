# -*- coding: utf-8 -*-
import re
import sys
import uuid
import markdown
from dotdict import dotdict
from django.conf import settings
from django.utils.encoding import smart_unicode, smart_str
from trytry.core.utils.call import call
from trytry.core.utils.lxc import lxc_wrap


class GenericStep(object):

    expected_out = None
    on_success_hint = None
    on_wrong_out_hint = None
    prompt = u'> '
    on_err_hint = ("Oh my God! Something goes wrong. Try read "
                   "instruction more carefully and perform the "
                   "task more diligently. Remember, I'm watching "
                   "you.")

    def __init__(self, flow=None):
        self.flow = flow

    def __call__(self, user_input):
        out, err, returncode = self.run_command(user_input)
        json_result = self.analyze(out, err, returncode)
        return json_result

    def get_uuid(self):
        if not hasattr(self, '_uuid'):
            self._uuid = str(uuid.uuid4())
        return self._uuid

    def run_command(self, user_input):
        """
        Run user provided command, applying timeout constraints

        :returns: A tuple containing (stdout, stderr, returncode)
        """
        command, stdin = self.get_command(user_input)
        if self.flow and settings.TRYTRY_LXC_ENABLED:
            command = self.wrap_in_lxc(command)
        else:
            command = self.wrap_in_timeout(command)
        stdin = smart_str(stdin)
        command = [smart_str(c) for c in command]
        out, err, returncode = call(command, stdin)
        out = smart_unicode(out, strings_only=True)
        err = smart_unicode(err, strings_only=True)
        return (out, err, returncode)

    def get_command(self, user_input):
        """
        Return a tuple ([command, to, execute], "stdin")
        """
        raise NotImplementedError('Must be implemented in subclass')

    def wrap_in_timeout(self, command):
        command = ['timelimit',
                   '-p', '-q',
                   '-t', str(settings.TRYTRY_SOFT_TIMEOUT),
                   '-T', str(settings.TRYTRY_HARD_TIMEOUT),
                   '--'] + command
        return command

    def wrap_in_lxc(self, command):
        return lxc_wrap(self.flow, command)

    def analyze(self, out, err, returncode):
        ret = {
            'goto_next': False,
            'hint': None,
            'ok_text': out,
            'err_text': err,
        }
        if out and out.lower() == self.expected_out.lower():
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

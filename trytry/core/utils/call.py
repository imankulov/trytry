# -*- coding: utf-8 -*-
import shlex
import subprocess as subp


def call(command, stdin=None):
    """
    Call command by passing data to stdin,

    :param command: string or list of strings to execute

    :returns: (stdout, stderr, returncode)
    """
    if isinstance(command, basestring):
        command = shlex.split(command)
    pipe = subp.Popen(command, stdin=subp.PIPE, stdout=subp.PIPE,
                      stderr=subp.PIPE)
    out, err = pipe.communicate(stdin)
    out = out.rstrip() or None
    err = err.rstrip() or None
    return out, err, pipe.returncode


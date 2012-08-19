# -*- coding: utf-8 -*-
import textwrap
from django.conf import settings
from django.core.management.base import NoArgsCommand
from trytry.core.utils.call import call




class Command(NoArgsCommand):

    help = ("This command checks whether your current environment is fully "
            "conformed with the application requirements")

    def handle_noargs(self, **options):
        self.style.ERR = self.style.NOTICE
        self.style.OK = self.style.SQL_COLTYPE
        self.style.INFO = self.style.SQL_KEYWORD

        def _write_line(style, prefix, line):
            chunks = textwrap.wrap(line, break_on_hyphens=False)
            for chunk in chunks:
                self.stdout.write(style(prefix))
                self.stdout.write(style(chunk))
                self.stdout.write('\n')
                prefix = ' ' * len(prefix)

        for k in dir(self):
            if k.startswith('check_'):
                v = getattr(self, k)
                if not callable(v):
                    continue
                out = v()
                if not out:
                    continue  # test is not applicable
                status, result = out
                test_name = v.__doc__ and v.__doc__.strip() + ': ' or ''
                line = '{0}{1}'.format(test_name, result)
                if status is True:
                    _write_line(self.style.OK, '[ OK ] ', line)
                elif status is False:
                    _write_line(self.style.ERR, '[ ERR] ', line)
                else:
                    _write_line(self.style.INFO, '[INFO] ', line)

    def check_sudo(self):
        """ Sudo support """
        _, _, code = call('sudo whoami')
        reason = 'Feature is required to support LXC'
        if code == 0:
            return ok('User can execute command with sudo. {0}'.format(reason))
        else:
            if settings.TRYTRY_LXC_ENABLED:
                return err('User CANNOT execute command with sudo. {0}'.format(reason))
            else:
                return info('User cannot execute command with sudo. {0}'.format(reason))


    def check_lxc_enabled(self):
        enabled = 'enabled' if settings.TRYTRY_LXC_ENABLED else 'disabled'
        return info('You have settings.TRYTRY_LXC_ENABLED variable {0}. '
                    'You can change its value in your localsettings.py'.format(enabled))


    def check_timelimit(self):
        """ Command timelimit """
        out, _, code = call('which timelimit')
        reason = ('This command is used to limit the maximum time span '
                  'of command execution. ')
        if code == 0:
            return ok('Command {0} found. {1}'.format(out, reason))
        else:
            return err('Command "timelimit" is not found. {0}'
                       'Ubuntu and Debian users can set it up with '
                       '"apt-get install timeline"'.format(reason))

    def check_lxc_commands(self):
        """ LXC userspace support """
        if settings.TRYTRY_LXC_ENABLED:
            out, _, code = call('which lxc')
            reason = 'This command is the indicator whether the LXC module is set up'
            if code == 0:
                return ok('Command {0} found. {1}'.format(out, reason))
            else:
                return err('Command "lxc" is not found. {0}. Ubuntu and Debian '
                           'users can set it up with "apt-get install lxc". See '
                           'http://try-try.readthedocs.org/en/latest/lxc.html '
                           'for more details'.format(reason))

def ok(text):
    return (True, text)

def err(text):
    return (False, text)

def info(text):
    return (None, text)

# -*- coding: utf-8 -*-
import pipes
from django.conf import settings
from trytry.core.utils.call import call

#--- Setup and teardown functions


def lxc_setup(flow_obj):
    if not settings.TRYTRY_LXC_ENABLED:
        return
    name = 'flow_{0}'.format(flow_obj.id)
    if name in lxc_list():
        return
    source = flow_obj.get_flow_settings().get('lxc_container',
                                        settings.TRYTRY_LXC_DEFAULT_CONTAINER)
    lxc_clone(source, name)


def lxc_teardown(flow_obj):
    if not settings.TRYTRY_LXC_ENABLED:
        return
    name = 'flow_{0}'.format(flow_obj.id)
    if name not in lxc_list():
        return
    lxc_destroy(name)


#--- Wrap command to be executed in LXC container

def lxc_wrap(flow_obj, command):
    name = 'flow_{0}'.format(flow_obj.id)
    lxc_wait_command = _get_lxc_wait_command(name,
                                 timeout=settings.TRYTRY_HARD_TIMEOUT)
    lxc_start_command = [
        'timelimit',
        '-t', str(settings.TRYTRY_SOFT_TIMEOUT),
        '-T', str(settings.TRYTRY_HARD_TIMEOUT),
        '--',
        'lxc-start', '-n', name, '--'
    ] + command
    lxc_start_command_str = ' '.join(pipes.quote(c) for c in lxc_start_command)
    lxc_wait_command_str = ' '.join(pipes.quote(c) for c in lxc_wait_command)
    command_str = '{0} && {1}'.format(lxc_wait_command_str, lxc_start_command_str)
    command = ['sudo', 'bash', '-c', command_str]
    return command


#--- Low level LXC functions

def lxc_list():
    """
    Return the list of LXC containers
    """
    out, _, _ = call(['sudo', 'lxc-ls'])
    return out.strip().split()


def lxc_clone(source, name):
    """
    Clone the container source to target.

    Die with RuntimeError in case of a problem
    """
    command = ['sudo', 'lxc-clone', '-o', source, '-n', name]
    _, err, code = call(command)
    if code != 0:
        raise RuntimeError(err)


def lxc_destroy(name):
    """
    Destroy the LXC container

    Die with RuntimeError in case of a problem
    """
    lxc_wait(name)
    command = ['sudo', 'lxc-destroy', '-n', name]
    _, err, code = call(command)
    if code != 0:
        raise RuntimeError(err)


def lxc_wait(name, state='STOPPED', timeout=10):
    """
    Wait while LXC container reaches a defined state

    :raises: RuntimeError, if process was unable to wait for changing the state
             of container
    """
    command = ['sudo', ] + _get_lxc_wait_command(name, state, timeout)
    _, err, code = call(command)
    if code != 0:
        raise RuntimeError(err)


def _get_lxc_wait_command(name, state='STOPPED', timeout=10):
    command = [
        'timelimit',
        '-p', '-q',
        '-t', str(settings.TRYTRY_SOFT_TIMEOUT),
        '-T', str(settings.TRYTRY_HARD_TIMEOUT),
        '--', 'lxc-wait', '-n', name, '-s', state]
    return command

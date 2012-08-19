# -*- coding: utf-8 -*-
import cuisine
from fabric.api import settings, hide, run, sudo, cd, put
from fabric.contrib.files import append

packages = ['lxc', 'python-psycopg2', 'supervisor', 'nginx', 'uwsgi',
            'uwsgi-plugin-python', 'postfix', 'timelimit',
            'python-virtualenv', 'python-pip', 'git', 'memcached',
            'python-memcache']
repo_source = 'https://github.com/imankulov/trytry.git'
repo_path = '/home/try/trytry'
repo_branch = 'master'

lxc_pkg_list = {
    'bash': '',
    'python': '',
    'php': 'php5-cli',
    'ruby': 'ruby1.8',
}

#--- Base setup functions

def setup():
    setup_packages()
    setup_user()
    setup_virtualenv()
    setup_repo()
    setup_dependencies()
    setup_server_configs()
    setup_project()

def setup_packages():
    for pkg in packages:
        cuisine.package_ensure(pkg)

def setup_user():
    cuisine.user_ensure('try', home='/home/try', shell='/bin/bash')
    u_run('mkdir -p /home/try/etc /home/try/tmp')
    u_run('test -f /home/try/tmp/touchme || touch /home/try/tmp/touchme')
    append('/etc/sudoers', 'try ALL=(ALL) NOPASSWD: ALL')

def setup_virtualenv():
    if u_test('test -d /home/try/env').failed:
        with cd('/home/try'):
            u_run('virtualenv --system-site-packages /home/try/env')

def setup_repo():
    parent = '/home/try'
    basename = 'trytry'

    if u_test('test -d {0}'.format(repo_path)).succeeded:
        # it's a git repo
        with cd(repo_path):
            u_run('git checkout {0}'.format(repo_branch))
            u_run('git pull')
    else:
        # no directory exists
        u_run('mkdir -p {0}'.format(parent))
        with cd(parent):
            u_run('git clone {0} {1}'.format(repo_source, basename))
            with cd(basename):
                u_run('git checkout {0}'.format(repo_branch))

def setup_dependencies():
    with cd(repo_path):
        u_run('pip install -r requirements.pip -E /home/try/env')
        u_run('pip install -e . -E /home/try/env')

def setup_server_configs():
    # nginx
    put('server_configs/nginx.conf', '/etc/nginx/conf.d/trytry.conf')
    run('service nginx reload')
    # supervisor
    put('server_configs/supervisord.conf', '/etc/supervisor/conf.d/trytry.conf')
    run('supervisorctl update')
    # uwsgi
    u_put('server_configs/uwsgi.conf', '/home/try/etc/uwsgi.conf')
    u_run('touch /home/try/tmp/touchme')

def setup_project():
    u_put('server_configs/localsettings.py',
          '/home/try/trytry/trytry/localsettings.py')
    with cd('/home/try/trytry'):
        u_run('/home/try/env/bin/python manage.py syncdb --noinput --migrate')
        u_run('/home/try/env/bin/python manage.py collectstatic --noinput')
    u_run('touch /home/try/tmp/touchme')

#--- LXC snapshot management

def lxc_setup():
    lxc_setup_base()
    for name, extra_packages in lxc_pkg_list.iteritems():
        lxc_setup_child(name, extra_packages)

def lxc_setup_base():
    if 'try-try' not in lxc_ls():
        put('server_configs/lxc.conf', 'lxc.conf')
        run("lxc-create -n try-try -t ubuntu -f lxc.conf -- --trim")


def lxc_setup_child(name, extra_packages):
    """ Helper function. Creates a new child lxc container

    :param name: name of the container
    :extra_packages: space-separated list of packages to install within
                     the container
    """
    if name not in lxc_ls():
        run("lxc-clone -o try-try -n {0}".format(name))
        if extra_packages:
            run("chroot /var/lib/lxc/{0}/rootfs bash -c '"
                "apt-get update &&"
                "apt-get install --yes --force-yes {1} "
                "'".format(name, extra_packages))

def lxc_ls():
    """ Helper function. Return the list of LXC containers """
    res = test("lxc-ls")
    return res.strip().split()

#--- Utility functions

def test(cmd, use_sudo=None, sudo_user=None):
    with settings(hide('warnings', 'running', 'stdout', 'stderr'), warn_only=True):
        if use_sudo or (sudo_user and use_sudo is None):
            ret = sudo(cmd, user=sudo_user)
        else:
            ret = run(cmd)
    return ret

def u_run(*args, **kwargs):
    return sudo(user='try', *args, **kwargs)

def u_put(src, dst):
    put(src, dst)
    run('chown {0}:{0} {1}'.format('try', dst))

def u_test(cmd):
    return test(cmd, use_sudo=True, sudo_user='try')

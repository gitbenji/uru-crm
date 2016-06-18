# -*- coding: utf-8 -*-
"""
    fabfile
    ~~~~~~~

    fabric commands
"""

import os

from fabric.api import *
from fabric.contrib.project import rsync_project
from fabric.contrib import console
from fabric import utils
import fabric_gunicorn as gunicorn


project = "fbone"

# the user to use for the remote commands
env.user = ''
# the servers where the commands are executed
env.hosts = ['']

RSYNC_EXCLUDE = [
    'app_wsgi.py',
    '*.pyc',
    '.DS_Store',
    'config/',
    'conf/',
    'tmp/',
    '*.cfg',
    '*.conf',
    'LICENSE',
    '*.md',
    '.hg*',
    '.flow'
]


def bootstrap():
    """ initialize remote host environment (virtualenv, deploy, update) """
    create_virtualenv()
    deploy()
    update_requirements()


def create_virtualenv():
    """ setup virtualenv on remote host """
    with prefix("source ~/.bash_profile"):
        run('mkvirtualenv %s' % 'fbone')


def update_requirements():
    """ update external dependencies on remote host """
    with prefix('workon fbone'):
        requirements = os.path.join(env.path, 'requirements.txt')
        cmd = ['pip install -r %s' % requirements]
        run(' '.join(cmd))


def reset():
    """Reset local debug env.
    """
    local("rm -rf /tmp/instance")
    local("mkdir /tmp/instance")
    local("python manage.py initdb")


def apt_get(*packages):
    sudo('apt-get -y --no-upgrade install %s' % ' '.join(packages), shell=False)


def setup():
    """Setup virtual env.
    """
    apt_get("python-pip libmysqlclient-dev python-dev")
    local("virtualenv env")
    activate_this = "env/bin/activate_this.py"
    execfile(activate_this, dict(__file__=activate_this))
    local("python setup.py install")
    reset()


def deploy():
    """ rsync code to remote host """
    if env['roles'] == ['production']:
        if not console.confirm('Are you sure you want to deploy production?',
                               default=False):
            utils.abort('Production deployment aborted.')
    run('mkdir -p %s' % os.path.join(env.path, 'tmp/instance'))
    extra_opts = '--update'
    rsync_project(
        env.path,
        env.root,
        exclude=RSYNC_EXCLUDE,
        delete=True,
        extra_opts=extra_opts,)


def create_database():
    """Creates role and database"""
    pass


def d():
    """Debug.
    """
    reset()
    local("python manage.py runserver")


def babel():
    """Babel compile.
    """
    local("pybabel extract -F ../fbone/config -k lazy_gettext -o messages.pot fbone")
    local("pybabel init -i messages.pot -d fbone/translations -l es")
    local("pybabel init -i messages.pot -d fbone/translations -l en")
    local("pybabel compile -f -d fbone/translations")


def service(command=None):
    """ usage:  service:command
    ex:     fab -R production service:status
    commands: start, stop, status
    """
    if command:
        run('service fbone %s' % command)
    utils.error('invalid command')


def ps(name=None):
    """ usage:  ps:name
    ex:     fab -R production ps:name
    name: process name
    """
    if name:
        run('ps aux | grep %s' % name)
    utils.error('invalid command')



@task
def dev():
    # env.user = 'root'
    # env.hosts = ['localhost']
    env.gunicorn_wsgi_app = 'app_wsgi'
    # env.remote_workdir = '/root/lurcat-flask/lurcat'
    env.virtualenv_dir = os.environ['WORKON_HOME'] + 'env'
    env.gunicorn_workers = 1
    local("export LURCAT_CFG='config/server.cfg'")


@task
def deploy():
    local('hg pull')
    local('hg update')
    restart()


@task
def restart():
    gunicorn.restart()


@task
def start_app():
    gunicorn.start()


@task
def stop_app():
    gunicorn.stop()

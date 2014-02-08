#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
import sys
import subprocess
from pkg_resources import resource_string

PY3 = sys.version > '3'

if PY3:
    from subprocess import getstatusoutput
else:
    from commands import getstatusoutput


log = logging.getLogger(__name__)


def get_sublime_project_filename(project):
    return os.path.join(os.environ.get('PROJECT_HOME'), '{0}.sublime-project'.format(project))


def has_bin(name):
    status, _ = getstatusoutput('which {0}'.format(name))
    return status == 0


def build_path(virtualenv):
    return ':'.join([
        os.path.join(virtualenv, 'bin'),
        '/usr/local/bin',
        '/usr/bin',
        '/bin',
    ])


def template(args):
    '''
    Create a sublime text project file into the $PROJECT_HOME directory
    '''
    project, project_dir = args
    filename = get_sublime_project_filename(project)
    virtualenv = os.environ.get('VIRTUAL_ENV')

    log.info('Creating Sublime Text project file')

    template = resource_string(__name__, 'templates/sublime-project.json').decode('utf8')

    content = template.format(
        project=project,
        project_dir=project_dir,
        virtualenv=virtualenv,
        path=build_path(virtualenv)
    )

    with open(filename, 'wb') as sublime_project_file:
        sublime_project_file.write(content.encode('utf8'))

    for cmd in ('subl', 'subl3'):
        if has_bin(cmd):
            subprocess.call([cmd, '--project', filename], shell=False)
            break

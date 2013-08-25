#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
import subprocess
from pkg_resources import resource_string

log = logging.getLogger(__name__)


def get_sublime_project_filename(project):
    return os.path.join(os.environ.get('PROJECT_HOME'), '{0}.sublime-project'.format(project))


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

    template = resource_string(__name__, 'templates/sublime-project.json')

    content = template.format(
        project=project,
        project_dir=project_dir,
        virtualenv=virtualenv,
        path=build_path(virtualenv)
    )

    with open(filename, 'wb') as sublime_project_file:
        sublime_project_file.write(content.encode('utf8'))

    subprocess.call(['subl', filename], shell=False)

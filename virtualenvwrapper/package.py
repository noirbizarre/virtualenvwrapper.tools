#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
import shutil
import subprocess

from os.path import join
from pkg_resources import resource_string

log = logging.getLogger(__name__)


TEMPLATES = (
    'README.rst',
    'Makefile',
    'bumpr.rc',
    'coverage.rc',
    'setup.py',
)

FILES = (
    'CHANGELOG.rst',
    'MANIFEST.in',
    'pep8.rc',
    'pylint.rc',
    'tox.ini',
)

REQUIREMENTS = (
    'install',
    'test',
    'report',
)


def template(args):
    '''
    Create a project layout for Python packaging
    '''
    project, project_dir = args

    params = {
        'project': project,
        'project_dir': project_dir,
        'virtualenv': os.environ.get('VIRTUAL_ENV'),
        'user': os.environ.get('USER')
    }

    log.info('Creating a Python packaging layout')

    # Copy files
    for filename in FILES:
        content = resource_string(__name__, 'templates/{0}'.format(filename))
        with open(join(project_dir, filename), 'wb') as f:
            f.write(content.encode('utf8'))

    # Copy and render templates
    for filename in TEMPLATES:
        template = resource_string(__name__, 'templates/{0}'.format(filename))
        content = template.format(**params)
        with open(join(project_dir, filename), 'wb') as f:
            f.write(content.encode('utf8'))

    # Create an empty package
    os.mkdir(join(project_dir, project))
    template = resource_string(__name__, 'templates/__init__.py')
    content = template.format(**params)
    with open(join(project_dir, project, '__init__.py'), 'wb') as f:
        f.write(content.encode('utf8'))

    # Create requirements files
    requirements_dir = join(project_dir, 'requirements')
    os.mkdir(requirements_dir)
    for basename in REQUIREMENTS:
        filename = join(requirements_dir, '{0}.pip'.format(basename))
        with open(filename, 'w') as f:
            f.write('')

    with open(join(requirements_dir, 'all.pip'), 'wb') as f:
        f.write('\n'.join([
            '-r {0}.pip'.format(basename) for basename in REQUIREMENTS
        ]).encode('utf8'))
        f.write('\n')


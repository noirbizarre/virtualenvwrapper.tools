# -*- coding: utf-8 -*-
import logging
import os
import subprocess

log = logging.getLogger(__name__)


def get_url(project):
    user = os.environ.get('GITHUB_USER', os.environ.get('USER'))
    if not user:
        log.error('Set USER or GITHUB_USER')
        return None
    return 'ssh://git@github.com/{user}/{project}.git'.format(user=user, project=project)


def template(args):
    '''
    Clone the corresponding github repository as project root
    '''
    project, project_dir = args
    url = get_url(project)
    if url:
        log.info('Cloning %s', url)
        print 'Cloning {}'.format(url)
        subprocess.call(['git', 'clone', url, project_dir, '-o', 'github'], shell=False)
    return

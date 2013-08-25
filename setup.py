#!/usr/bin/env python
import os
import re
import sys

from setuptools import setup, find_packages

PROJECT = 'virtualenvwrapper.tools'
VERSION = '0.1'

PYPI_RST_FILTERS = (
    # Replace code-blocks
    (r'\.\.\s? code-block::\s*(\w|\+)+',  '::'),
    # Remove travis ci badge
    (r'.*travis-ci\.org/.*', ''),
    # Remove pypip.in badges
    (r'.*pypip\.in/.*', ''),
    (r'.*crate\.io/.*', ''),
    (r'.*coveralls\.io/.*', ''),
)


def rst(filename):
    '''
    Load rst file and sanitize it for PyPI.
    Remove unsupported github tags:
     - code-block directive
     - travis ci build badge
    '''
    content = open(filename).read()
    for regex, replacement in PYPI_RST_FILTERS:
        content = re.sub(regex, replacement, content)
    return content


description = 'Some virtualenvwrapper tools'


provides = (
    'virtualenvwrapper.sublime',
    'virtualenvwrapper.github',
    'virtualenvwrapper.package',
)


setup(
    name=PROJECT,
    version=VERSION,

    description=description,
    long_description=rst('README.rst'),

    author='Axel Haustant',
    author_email='noirbizarre@gmail.com',

    url='https://github.com/noirbizarre/virtualenvwrapper.tools',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Developers',
        'Environment :: Console',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
    ],

    platforms=['Any'],

    provides=provides,
    requires=['virtualenv', 'virtualenvwrapper (>=4.0)'],
    namespace_packages=['virtualenvwrapper'],
    packages=find_packages(),
    include_package_data=True,

    entry_points={
        'virtualenvwrapper.project.template': [
            'github = virtualenvwrapper.github:template',
            'sublime = virtualenvwrapper.sublime:template',
            'package = virtualenvwrapper.package:template',
        ],
    },

    zip_safe=False,
)

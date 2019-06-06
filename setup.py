#!/usr/bin/python
# -*- coding: utf-8 -*-

from puppeteer import __version__
from setuptools import setup, find_packages

setup(
    name='puppeteer',
    version=__version__,
    author='Haani Niyaz',
    author_email='haani.niyaz@gmail.com',
    url='https://github.com/haani-niyaz/puppeteer',
    license='MIT',
    description='An opionated way to manage your Ansible workflow',
    keywords='ansible development productivity workflow',
    packages=find_packages(exclude=['docs', 'tests']),
    entry_points={
        'console_scripts': [
            'puppeteer=puppeteer.cli:main',
        ],
    },
    install_requires=[
        "pyyaml >= 5.1",
    ],
)

#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='puppeteer',
    version='0.1',
    author='Haani Niyaz',
    author_email='haani.niyaz@gmail.com',
    keywords='ansible development productivity workflow',
    packages=find_packages(exclude=['docs', 'tests']),
    entry_points={
            'console_scripts': [
                'puppeteer=puppeteer:main',
            ],
    },

)

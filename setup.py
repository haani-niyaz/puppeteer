#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='puppeteer',
    version='0.1',
    packages=find_packages(),
    entry_points={
            'console_scripts': [
                'puppeteer=puppeteer:main',
            ],
    },

)

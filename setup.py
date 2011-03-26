#!/usr/bin/env python

from setuptools import setup, find_packages

files = ["taillogger/*"]

setup(
    name = 'taillogger',
    version = "0.1",
    description = "Monitors a list of files and sends the contents to syslog",
    author = "Mike Zupan",
    author_email = "mike@zcentric.com",
    packages = find_packages(),
    entry_points={
        'console_scripts': [
            'taillogger = taillogger.main:main',
        ]
    },
)

#!/usr/bin/env python3

# SPDX-License-Identifier: Apache-2.0
# Copyright 2020 Charles University

from setuptools import setup

def get_readme():
    ''' Return content of Readme file'''
    with open('README') as file_in:
        return file_in.read()

def get_install_requieres():
    '''Function to get content of requirements'''
    with open('requirements.txt') as reqs_file:
        install_reqs = reqs_file.read().split()
    return install_reqs


setup(
    name='Apolenka assistent',
    version='0.1',
    description='Simple voice assistent',
    long_description=get_readme(),
    classifiers=[
        '  Programming Language :: Python :: 3.5',
    ],
    keywords='assistent voice',
    include_package_data=True,
    zip_safe=False,
    install_requires=get_install_requieres(),
    entry_points={
        'console_scripts': [
            'assistant=google_calendar.add_event:main',
        ],
    },
)

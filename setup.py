#!/usr/bin/env python

from setuptools import setup
setup(
    name='granholm',
    version='0.1dev',
    author='Viktor Granholm',
    author_email='viktor.granholm@scilifelab.se',
    url='https.//github.com/viktorg/granholm',
    packages=['granholm',],
    scripts = ['scripts/getting_data.py', 'scripts/check_repo.py'],
    license='GPLv3',
    long_description=open('README.txt').read(),
)

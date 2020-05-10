#!/usr/bin/env python
from setuptools import setup, find_packages

setup(name='distro-doh',
      version='0.1',
      description='Tp1 Distro - DNS Over HTTP',
      author='Alejandro Pernin',
      author_email='apernin@fi.uba.ar',
      packages=find_packages(exclude=('tests', 'tests.*')),
      )


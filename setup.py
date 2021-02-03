#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup

classifiers = [
    "Environment :: Other Environment",
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
]

requirements = [line.strip() for line in open('requirements.txt').readlines()]

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(name='andebox',
      version='0.1',
      description="Ansible Developer's Box",
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='Alexei Znamensky',
      author_email='russoz@gmail.com',
      url='',
      scripts=['andebox'],
      install_requires=requirements,
      classifiers=classifiers,
      )

#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup

requirements = [line.strip() for line in open('requirements.txt').readlines()]

setup(name='andebox',
      version='0.9.0',
      scripts=['andebox'],
      install_requires=requirements,
      )

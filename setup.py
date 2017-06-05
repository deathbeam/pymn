#!/usr/bin/env python

from setuptools import setup

setup(
  name='pymn',
  entry_points = {
    'console_scripts': [
      'pymn = pymn:main',
    ],
  },
  packages = [
    'pymn',
    'pymn.switch',
    'pymn.topology'
  ]
)

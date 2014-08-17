#!/usr/bin/env python
from setuptools import setup, find_packages


long_description = '''
'''
VERSION = (0, 0, 0)
__version__ = '.'.join(str(p) for p in VERSION[0:3]) + ''.join(VERSION[3:])

setup(name='statelet',
      version='.'.join(map(str, VERSION)),
      packages=find_packages(),
      author='Thom Neale',
      author_email='twneale@gmail.com',
      url='http://github.com/twneale/statelet',
      description='Basic tool for sharing state among objects.',
      long_description=long_description,
      platforms=['any'],
      classifiers=["Development Status :: 4 - Beta",
                   "Intended Audience :: Developers",
                   "License :: OSI Approved :: BSD License",
                   "Natural Language :: English",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python :: 3.4"]
)

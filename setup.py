#!/usr/bin/env python
#from distutils.core import setup
from setuptools import setup, find_packages

requirements = list(open('dist_requirements.txt').readlines())

setup(name="lark",
      version='0.0.1',
      description="Lark is a RESTy interface for python",
      long_description=open('README.rst').read(),
      license="MIT",
      author="Alex Kessinger",
      author_email="voidfiles@gmail.com",
      url="http://github.com/voidfiles/lark",
      packages=find_packages(exclude=['tests']),
      install_requires=requirements,
      keywords="rest lark json",
      zip_safe=True)

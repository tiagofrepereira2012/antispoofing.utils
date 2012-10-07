#!/usr/bin/env python
#Tiago de Freitas Pereira <tiagofrepereira@gmail.com>
#Sat Jul  9 20:21:55 CEST 2012

from setuptools import setup, find_packages

# The only thing we do in this file is to call the setup() function with all
# parameters that define our package.
setup(

    name='antispoofing.utils',
    version='1.1.0a0',
    description='Utilitary package for antispoofing countermeasures',
    url='http://pypi.python.org/pypi/antispoofing.utils',
    license='GPLv3',
    author='Tiago de Freitas Pereira',
    author_email='tiagofrepereira@gmail.com',
    long_description=open('README.rst').read(),

    # This line is required for any distutils based packaging.
    packages=find_packages(),
    include_package_data = True,

    install_requires=[
      "setuptools",
      "bob >= 1.1",
      "xbob.db.replay",
      "xbob.db.casia_fasd",
    ],

    namespace_packages = [
      'antispoofing',
      ],


    entry_points = {
      # Database declaration
      'antispoofing.utils.db': [
        'replay     = antispoofing.utils.db.replay:Database',
        'casia_fasd = antispoofing.utils.db.casia_fasd:Database',
        ],
      },

)

#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
    Magento API

    :license: BSD, see LICENSE for more details

'''
import os
from setuptools import setup

execfile(os.path.join('magento', 'version.py'))

setup(
    name = 'magento',
    version=VERSION,
    url='https://github.com/fulfilio/magento/',
    license='BSD 3-Clause',
    author='Sharoon Thomas, Openlabs Technologies',
    author_email='info@fulfil.io',
    description='Magento Core API Client',
    long_description=open('README.rst').read(),
    packages=['magento'],
    zip_safe=False,
    platforms='any',
    install_requires=[
        'suds>=0.3.9',
    ],
    classifiers=[
        'Development Status :: 6 - Mature',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)

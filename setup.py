#!/usr/bin/env python
from setuptools import find_packages, setup

version = '0.1.0'

setup(
    name="django-model-deprecater",
    version=version,
    packages=find_packages(),
    zip_safe=True,
    description="A django library to assist in deprecating models.",
    long_description=open('README.rst').read(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development',
    ],
    author='Jason Novinger, Evan Fagerberg',
    author_email='jnovinger@oreilly.com, efagerberg@oreilly.com',
    url='http://github.com/oreilly/django-model-deprecater',
    include_package_data=True,
)

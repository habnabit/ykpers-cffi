# Copyright (c) Aaron Gallagher <_@habnab.it>
# See COPYING for details.

from setuptools import setup
import os.path


with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as infile:
    long_description = infile.read()

setup(
    name='ykpers-cffi',

    description='libykpers bindings for python via cffi',
    long_description=long_description,
    author='Aaron Gallagher',
    author_email='_@habnab.it',
    url='https://github.com/habnabit/ykpers-cffi',
    license='ISC',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Topic :: Security',
        'Topic :: Utilities',
    ],

    py_modules=['ykpers'],
    install_requires=['cffi'],
    tests_require=['mock', 'pytest'],
    setup_requires=['vcversioner'],
    vcversioner={},
)

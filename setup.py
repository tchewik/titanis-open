#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import, print_function

import io
from os.path import dirname
from os.path import join

from setuptools import setup


def read(*names, **kwargs):
    return io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ).read()


setup(
    name='titanis',
    version='0.0.1-open',
    description='ISA library for text mining.',
    author='ISA RAS',
    author_email='',
    packages=['titanis', 'titanis.features', 'titanis.data'],
    package_dir={'': 'src'},
    data_files=[('titanis/data', ['src/titanis/data/psydicts.json'])],
    include_package_data=True,
    zip_safe=False,
    install_requires=['isanlp @ git+https://github.com/IINemo/isanlp.git', 'nltk', 'pymystem3']
)

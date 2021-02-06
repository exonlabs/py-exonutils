# -*- coding: utf-8 -*-
"""
    :copyright: 2021, ExonLabs. All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
import os
import re
from setuptools import setup, find_packages

pkgname = "exonutils"

os.chdir(os.path.abspath(os.path.dirname(__file__)))
with open(os.path.join(pkgname, '__init__.py'), 'rt') as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)
with open('README.md', 'rt') as f:
    long_description = f.read()


setup(
    name=pkgname,
    version=version,
    url='https://bitbucket.org/exonlabs/exonutils',
    author='ExonLabs',
    license='BSD',
    description='Common and base utilities for applications.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    python_requires='>=3.7',
    install_requires=[],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)

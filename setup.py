# -*- coding: utf-8 -*-
"""
    :copyright: 2020, ExonLabs. All rights reserved.
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
    python_requires='>=2.7,<3.0',
    install_requires=[
        'future>=0.18',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)

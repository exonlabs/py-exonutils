# -*- coding: utf-8 -*-
"""
    :copyright: 2020, ExonLabs. All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
import os
from setuptools import setup

os.chdir(os.path.abspath(os.path.dirname(__file__)))

__PKGNAME__ = 'exonutils'
__VERSION__ = '1.6.1.dev'

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name=__PKGNAME__,
    version=__VERSION__,
    license='BSD',
    url='https://bitbucket.org/exonlabs/exonutils',
    author='exonlabs',
    description='Common and base utilities for applications.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=[__PKGNAME__],
    include_package_data=True,
    zip_safe=False,
    platforms='linux',
    python_requires='>=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*,!=3.5.*',
    install_requires=[
        'future>=0.18',
        'setproctitle>=1.1',
        'flask>=1.1',
        'Jinja2>=2.11',
        'gunicorn>=20.0;python_version>="3.6"',
        'gunicorn>=19.10;python_version<"3.0"',  # py2 compatability
        'gevent>=20.5',
        'sqlalchemy>=1.3',
        'alembic>=1.4',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)

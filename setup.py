# -*- coding: utf-8 -*-
"""
    :copyright: 2020, ExonLabs. All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
import os
import sys
from setuptools import setup

os.chdir(os.path.abspath(os.path.dirname(__file__)))

__PKGNAME__ = 'exonutils'
__VERSION__ = '1.1.1.dev'

PY3 = sys.version_info >= (3, 0)


setup(
    name=__PKGNAME__,
    version=__VERSION__,
    license='BSD',
    url='https://bitbucket.org/exonlabs/exonutils',
    author='exonlabs',
    description='Common and base utilities for applications.',
    packages=[__PKGNAME__],
    include_package_data=True,
    zip_safe=False,
    platforms='linux',
    python_requires='>=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*',
    install_requires=[
        'setproctitle>=1.1.10',
        'simplejson>=3.17.0',
        'sqlalchemy>=1.3.15',
        'alembic>=1.4.0',
        'flask>=1.1.1',
        'Jinja2>=2.11.1',
        'gunicorn>=%s' % ('20.0.4' if PY3 else '19.10.0'),
        'gevent>=1.4.0',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)

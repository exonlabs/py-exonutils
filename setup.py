# -*- coding: utf-8 -*-
"""
    :copyright: 2020, ExonLabs. All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
import os
import re
from setuptools import setup, find_packages

pkg_name = 'exonutils'

os.chdir(os.path.abspath(os.path.dirname(__file__)))
with open(os.path.join(pkg_name, '__init__.py'), 'rt') as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)
with open('README.md', 'rt') as f:
    long_description = f.read()


setup(
    name=pkg_name,
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

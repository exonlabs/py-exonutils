# -*- coding: utf-8 -*-
"""
    :copyright: 2020, ExonLabs. All rights reserved.
    :license: BSD, see LICENSE for more details.
"""


# return True if you are running inside virtualenv
def is_virtualenv():
    import sys
    return (getattr(sys, 'base_prefix', sys.prefix) != sys.prefix or
            hasattr(sys, 'real_prefix'))


# returns list of python packages inside certain target location
def pypkgs(target, package):
    from importlib import import_module
    from pkgutil import iter_modules
    try:
        if target == '.':
            pkg_parts = package.split('.')
            target = '.%s' % pkg_parts[-1]
            package = '.'.join(pkg_parts[:-1])
        pkg_path = import_module(target, package=package).__path__
        return [name for imp, name, ispkg in iter_modules(pkg_path)
                if ispkg]
    except ImportError:
        return []


# returns list of python modules inside certain target location
def pymods(target, package):
    from importlib import import_module
    from pkgutil import iter_modules
    try:
        if target == '.':
            pkg_parts = package.split('.')
            target = '.%s' % pkg_parts[-1]
            package = '.'.join(pkg_parts[:-1])
        pkg_path = import_module(target, package=package).__path__
        return [name for imp, name, ispkg in iter_modules(pkg_path)
                if not ispkg]
    except ImportError:
        return []

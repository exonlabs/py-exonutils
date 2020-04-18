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


# create shared data buffer with access locking
def shared_buffer():
    import threading

    class SharedBuffer(object):

        def __init__(self):
            self._data = {}
            self._lock = {}

        def list(self):
            return self._data.keys()

        def get(self, key):
            if key in self._data:
                with self._lock[key]:
                    return self._data[key]
            return None

        def set(self, key, value):
            if key not in self._data:
                self._lock[key] = threading.Lock()
            with self._lock[key]:
                self._data[key] = value

        def delete(self, key):
            if key in self._data:
                del(self._data[key])
                del(self._lock[key])

        def reset(self):
            self._data = {}
            self._lock = {}

    return SharedBuffer()

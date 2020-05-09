# -*- coding: utf-8 -*-
"""
    :copyright: 2020, ExonLabs. All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
import sys

__all__ = []


# return True if you are running inside virtualenv
def is_virtualenv():
    return (getattr(sys, 'base_prefix', sys.prefix) != sys.prefix or
            hasattr(sys, 'real_prefix'))


# returns list of python packages inside certain target package
def pypkgs(target):
    from importlib import import_module
    from pkgutil import iter_modules
    try:
        pkg = import_module('.', package=target)
        return ['%s.%s' % (target, n)
                for i, n, ispkg in iter_modules(pkg.__path__) if ispkg]
    except:
        return []


# returns list of python modules inside certain target package
def pymods(target):
    from importlib import import_module
    from pkgutil import iter_modules
    try:
        pkg = import_module('.', package=target)
        res = [pkg]
        mods = ['%s.%s' % (target, n)
                for i, n, ispkg in iter_modules(pkg.__path__) if not ispkg]
        for m in mods:
            res.append(import_module(m, package=target))
        return res
    except:
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

# -*- coding: utf-8 -*-
"""
    :copyright: 2020, ExonLabs. All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
import sys
import os
import pickle
from shutil import rmtree
from tempfile import gettempdir

__all__ = []


# return True if you are running inside virtualenv
def is_virtualenv():
    return (getattr(sys, 'base_prefix', sys.prefix) != sys.prefix or
            hasattr(sys, 'real_prefix'))


# returns list of python packages inside certain target package
def pypkgs(target):
    from importlib import import_module
    from pkgutil import iter_modules

    pkg = import_module('.', package=target)
    return ['%s.%s' % (target, n)
            for i, n, ispkg in iter_modules(pkg.__path__) if ispkg]


# returns list of python modules inside certain target package
def pymods(target):
    from importlib import import_module
    from pkgutil import iter_modules

    pkg = import_module('.', package=target)
    res = [pkg]
    mods = ['%s.%s' % (target, n)
            for i, n, ispkg in iter_modules(pkg.__path__) if not ispkg]
    for m in mods:
        res.append(import_module(m, package=target))
    return res


# create shared data buffer
class SharedBuffer(object):

    def __init__(self, name, tmpdir=None):
        if not tmpdir:
            tmpdir = gettempdir()
        self._dir = os.path.join(tmpdir, 'shm', name)
        if not os.path.exists(self._dir):
            os.makedirs(self._dir)

    def __del__(self):
        self.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        if os.path.exists(self._dir):
            rmtree(self._dir, ignore_errors=True)

    def keys(self):
        return list(os.walk(self._dir))[0][-1]

    def items(self):
        return {k: self.get(k) for k in self.keys()}

    def get(self, key, default=None):
        fpath = os.path.join(self._dir, key)
        if os.path.exists(fpath):
            with open(fpath, 'rb') as f:
                return pickle.load(f)
        return default

    def set(self, key, value):
        fpath = os.path.join(self._dir, key)
        with open(fpath, 'wb') as f:
            pickle.dump(value, f)

    def delete(self, key):
        fpath = os.path.join(self._dir, key)
        if os.path.exists(fpath):
            os.unlink(fpath)

    def reset(self):
        for fname in self.keys():
            fpath = os.path.join(self._dir, fname)
            os.unlink(fpath)

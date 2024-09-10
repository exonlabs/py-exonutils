# -*- coding: utf-8 -*-
from importlib import import_module
from pkgutil import iter_modules

__all__ = []


# returns list of python packages inside certain target package
def get_pkgs(target):
    pkg = import_module('.', package=target)
    return ['%s.%s' % (target, n)
            for i, n, ispkg in iter_modules(pkg.__path__) if ispkg]


# returns list of python modules inside certain target package
def get_mods(target):
    pkg = import_module('.', package=target)
    res = [pkg]
    mods = ['%s.%s' % (target, n)
            for i, n, ispkg in iter_modules(pkg.__path__) if not ispkg]
    for m in mods:
        res.append(import_module(m, package=target))
    return res


# returns list of python classes inside certain target module
def get_classes(target, baseclass=None):
    res = []
    if hasattr(target, '__all__'):
        for name in target.__all__:
            cls = getattr(target, name)
            if not baseclass or issubclass(cls, baseclass):
                res.append(cls)
    return res

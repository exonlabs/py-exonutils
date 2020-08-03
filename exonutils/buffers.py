# -*- coding: utf-8 -*-
"""
    :copyright: 2020, ExonLabs. All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
import os
import pickle
import copy
import time
import logging

__all__ = ['SimpleBuffer', 'SharedFileBuffer']


class _FileLock(object):

    lock_poll_delay = 0.1  # delay in sec to check existing lock
    lock_poll_trials = 5   # number of retires to check existing lock

    def __init__(self, name, store_dir):
        _dir = os.path.abspath(store_dir)
        if not os.path.exists(_dir):
            raise RuntimeError("dir doesn't exist: %s" % _dir)
        self._lockfile = os.path.join(_dir, '%s.lock' % name)

    def __enter__(self):
        # bypass/ignore existing lock if timeout passes
        for i in range(self.lock_poll_trials):
            if not os.path.exists(self._lockfile):
                open(self._lockfile, 'w').close()
                break
            time.sleep(self.lock_poll_delay)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            os.unlink(self._lockfile)
        except:
            pass


class BaseBuffer(object):

    def __init__(self, defaults={}):
        self._defaults = copy.deepcopy(defaults) \
            if type(defaults) is dict else {}
        self._lock = None
        self.init()

    def __repr__(self):
        with self._lock:
            d = self.load()
        return d.__repr__()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def init(self):
        raise NotImplementedError()

    def load(self):
        raise NotImplementedError()

    def save(self, data):
        raise NotImplementedError()

    def keys(self):
        with self._lock:
            d = self.load()
        return d.keys()

    def items(self):
        with self._lock:
            d = self.load()
        return d.items()

    def get(self, key, default=None):
        with self._lock:
            d = self.load()
        return d.get(key, default)

    def set(self, key, value):
        with self._lock:
            d = self.load()
            d[key] = value
            self.save(d)

    def delete(self, key):
        with self._lock:
            d = self.load()
            del(d[key])
            self.save(d)

    def reset(self):
        with self._lock:
            self.save(self._defaults)

    def purge(self):
        pass


# pure in memory dict based buffer
class SimpleBuffer(BaseBuffer):

    def init(self):
        from multiprocessing import RLock
        self._lock = RLock()
        self._data = copy.deepcopy(self._defaults)

    def load(self):
        return self._data

    def save(self, data):
        self._data = copy.deepcopy(data)


# file based data buffer
class SharedFileBuffer(BaseBuffer):

    def __init__(self, name, defaults={}, store_dir='', create_dirs=False):
        self._defaults = copy.deepcopy(defaults) \
            if type(defaults) is dict else {}

        if store_dir:
            _dir = os.path.abspath(store_dir)
        else:
            from tempfile import gettempdir
            _dir = gettempdir()
        if not os.path.exists(_dir):
            if create_dirs:
                os.makedirs(_dir)
            else:
                raise RuntimeError("dir doesn't exist: %s" % _dir)
        self._fpath = os.path.join(_dir, '%s.dat' % name)
        self._lock = _FileLock(name, _dir)

        self.init()

    def init(self):
        if not os.path.exists(self._fpath):
            self.save(self._defaults)

    def load(self):
        if os.path.exists(self._fpath):
            try:
                with open(self._fpath, 'rb') as f:
                    return pickle.load(f)
            except Exception as e:
                logging.getLogger().debug(
                    "failed to load buffer %s - %s" % (self._fpath, e))
        return {}

    def save(self, data):
        with open(self._fpath, 'wb') as f:
            pickle.dump(data, f)

    def purge(self):
        try:
            if os.path.exists(self._fpath):
                os.unlink(self._fpath)
        except Exception as e:
            logging.getLogger().debug(
                "failed to purge buffer %s - %s" % (self._fpath, e))

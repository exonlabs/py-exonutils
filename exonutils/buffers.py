# -*- coding: utf-8 -*-
"""
    :copyright: 2020, ExonLabs. All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
import os
import pickle
import logging
import time
from shutil import rmtree

__all__ = ['BaseBuffer', 'FileBuffer']


class BaseBuffer(object):

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self.name)

    # low level list all buffer keys
    def _list(self, trials=0):
        raise NotImplementedError()

    # low level read key from buffer
    def _read(self, key, trials=0):
        raise NotImplementedError()

    # low level write key in buffer
    def _write(self, key, value, trials=0):
        raise NotImplementedError()

    # low level delete key from buffer
    def _delete(self, key, trials=0):
        raise NotImplementedError()

    # low level delete all buffer data
    def _purge(self, trials=0):
        raise NotImplementedError()

    def init(self, defaults, clean=True, trials=3):
        if clean:
            self._purge(trials=trials)
        for k, v in defaults:
            self._write(k, v, trials=trials)

    # list all keys in buffer
    def keys(self, trials=3):
        return self._list(trials=trials)

    # list all items in buffer
    def items(self, trials=3):
        return {k: self._read(k, trials=trials)
                for k in self._list(trials=trials)}

    # get certain key from buffer
    def get(self, key, default=None, trials=3):
        res = self._read(key, trials=trials)
        return res if res is not None else default

    # set certain key in buffer
    def set(self, key, value, trials=3):
        return self._write(key, value, trials=trials)

    # delete certain key from buffer
    def delete(self, key, trials=3):
        return self._delete(key, trials=trials)

    # purge buffer
    def purge(self, trials=3):
        return self._purge(trials=trials)


# file based data buffer
class FileBuffer(BaseBuffer):

    def __init__(self, name, root_dir='', logger=None):
        super(FileBuffer, self).__init__(name)

        # root dir to use for storage
        if root_dir:
            self.root_dir = os.path.abspath(root_dir)
        else:
            from tempfile import gettempdir
            self.root_dir = gettempdir()

        # buffer store path
        self.base_path = os.path.join(self.root_dir, self.name)

        # buffer logger
        self.log = logger if logger else logging.getLogger(__name__)

    # low level list all buffer keys
    def _list(self, trials=3):
        for i in range(trials):
            try:
                if not os.path.exists(self.base_path):
                    return []
                root, dirs, files = os.walk(self.base_path)
                return list(files)
            except Exception as e:
                self.log.warn("failed listing filebuffer %s - %s"
                              % (self.base_path, e))
            time.sleep(0.05)

        return []

    # low level read key from buffer
    def _read(self, key, trials=3):
        fpath = os.path.join(self.base_path, key)
        for i in range(trials):
            try:
                if not os.path.exists(fpath):
                    return None
                with open(fpath, 'rb') as f:
                    return pickle.load(f)
            except Exception as e:
                self.log.warn("failed reading filebuffer key %s - %s"
                              % (fpath, e))
                time.sleep(0.05)

        return None

    # low level write key in buffer
    def _write(self, key, value, trials=3):
        fpath = os.path.join(self.base_path, key)
        for i in range(trials):
            try:
                if not os.path.exists(self.base_path):
                    os.makedirs(self.base_path)
                with open(fpath, 'wb') as f:
                    pickle.dump(value, f)
                return True
            except Exception as e:
                self.log.warn("failed writing filebuffer key %s - %s"
                              % (fpath, e))
                time.sleep(0.05)

        return False

    # low level delete key from buffer
    def _delete(self, key, trials=3):
        fpath = os.path.join(self.base_path, key)
        for i in range(trials):
            try:
                if not os.path.exists(fpath):
                    return True
                os.unlink(fpath)
                return True
            except Exception as e:
                self.log.warn("failed deleting filebuffer key %s - %s"
                              % (fpath, e))
                time.sleep(0.05)

        return False

    # low level delete all buffer data
    def _purge(self, trials=3):
        for i in range(trials):
            try:
                if not os.path.exists(self.base_path):
                    return True
                rmtree(self.base_path, ignore_errors=True)
                return True
            except Exception as e:
                self.log.warn("failed purging filebuffer %s - %s"
                              % (self.base_path, e))
                time.sleep(0.05)

        return False

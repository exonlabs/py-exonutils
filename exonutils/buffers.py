# -*- coding: utf-8 -*-
"""
    :copyright: 2021, ExonLabs. All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
import os
import pickle
from shutil import rmtree

__all__ = ['BaseBuffer', 'FileBuffer']


class BaseBuffer(object):

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self.name)

    # low level list all buffer keys
    def _list(self):
        raise NotImplementedError()

    # low level read key from buffer
    def _read(self, key):
        raise NotImplementedError()

    # low level write key in buffer
    def _write(self, key, value):
        raise NotImplementedError()

    # low level delete key from buffer
    def _delete(self, key):
        raise NotImplementedError()

    # low level delete all buffer data
    def _purge(self):
        raise NotImplementedError()

    def init(self, defaults, clean=True):
        if clean:
            self._purge()
        for k, v in defaults:
            self._write(k, v)

    # list all keys in buffer
    def keys(self):
        return self._list()

    # list all items in buffer
    def items(self):
        return {k: self._read(k)
                for k in self._list()}

    # get certain key from buffer
    def get(self, key, default=None):
        res = self._read(key)
        return res if res is not None else default

    # set certain key in buffer
    def set(self, key, value):
        return self._write(key, value)

    # delete certain key from buffer
    def delete(self, key):
        return self._delete(key)

    # purge buffer
    def purge(self):
        return self._purge()


# file based data buffer
class FileBuffer(BaseBuffer):

    def __init__(self, name, root_dir=''):
        super(FileBuffer, self).__init__(name)

        # root dir to use for storage
        if root_dir:
            self.root_dir = os.path.abspath(root_dir)
        else:
            from tempfile import gettempdir
            self.root_dir = gettempdir()

        # buffer store path
        self.base_path = os.path.join(self.root_dir, self.name)

    # low level list all buffer keys
    def _list(self):
        if os.path.exists(self.base_path):
            root, dirs, files = os.walk(self.base_path)
            return list(files)
        return []

    # low level read key from buffer
    def _read(self, key):
        fpath = os.path.join(self.base_path, key)
        if os.path.exists(fpath):
            with open(fpath, 'rb') as f:
                return pickle.load(f)
        return None

    # low level write key in buffer
    def _write(self, key, value):
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)
        fpath = os.path.join(self.base_path, key)
        with open(fpath, 'wb') as f:
            pickle.dump(value, f)

    # low level delete key from buffer
    def _delete(self, key):
        fpath = os.path.join(self.base_path, key)
        if os.path.exists(fpath):
            os.unlink(fpath)

    # low level delete all buffer data
    def _purge(self):
        if os.path.exists(self.base_path):
            rmtree(self.base_path, ignore_errors=True)

# -*- coding: utf-8 -*-
import os
import json
from shutil import rmtree
from tempfile import gettempdir

from .common import BaseBuffer

__all__ = []


# file based data buffer
class SimpleFileBuffer(BaseBuffer):

    def __init__(self, name, base_path=''):
        # buffer path to use for storage
        if base_path:
            self.buffer_path = os.path.join(
                os.path.abspath(base_path), name)
        else:
            self.buffer_path = os.path.join(gettempdir(), name)

    def __repr__(self):
        return '<%s: %s>' % (
            self.__class__.__name__, self.buffer_path)

    # list all keys in buffer
    def keys(self):
        if os.path.exists(self.buffer_path):
            files = next(os.walk(self.buffer_path))[2]
            return list(files)

        return []

    # list all items in buffer
    def items(self):
        return [(k, self.get(k))
                for k in self.keys()]

    # read certain key from buffer
    def get(self, key, default=None):
        if not key or type(key) is not str:
            raise ValueError("invalid key value")

        fpath = os.path.join(self.buffer_path, key)
        if os.path.exists(fpath):
            with open(fpath, 'r') as fh:
                res = json.load(fh)
            return res

        return default

    # set certain key in buffer
    def set(self, key, value):
        if not key or type(key) is not str:
            raise ValueError("invalid key value")

        if not os.path.exists(self.buffer_path):
            os.makedirs(self.buffer_path)

        fpath = os.path.join(self.buffer_path, key)
        with open(fpath, 'w') as fh:
            json.dump(value, fh)

    # delete certain key from buffer
    def delete(self, key):
        if not key or type(key) is not str:
            raise ValueError("invalid key value")

        fpath = os.path.join(self.buffer_path, key)
        if os.path.exists(fpath):
            os.unlink(fpath)

    # purge buffer, delete all keys
    def purge(self):
        if os.path.exists(self.buffer_path):
            rmtree(self.buffer_path, ignore_errors=True)

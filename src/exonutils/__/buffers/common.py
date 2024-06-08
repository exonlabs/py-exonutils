# -*- coding: utf-8 -*-

__all__ = []


class BaseBuffer(object):

    # list all keys in buffer
    def keys(self):
        raise NotImplementedError()

    # list all items in buffer
    def items(self):
        raise NotImplementedError()

    # read certain key from buffer
    def get(self, key, default=None):
        raise NotImplementedError()

    # set certain key in buffer
    def set(self, key, value):
        raise NotImplementedError()

    # delete certain key from buffer
    def delete(self, key):
        raise NotImplementedError()

    # purge buffer, delete all keys
    def purge(self):
        raise NotImplementedError()

    # reset and initialize buffer with default values
    def reset(self, defaults=None, clean=True):
        if clean:
            self.purge()
        if defaults:
            for k, v in defaults:
                self.set(k, v)

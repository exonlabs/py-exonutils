# -*- coding: utf-8 -*-
import threading
from queue import SimpleQueue

from .common import BaseBuffer

__all__ = []


# thread safe shared variable data
class SharedData(object):

    def __init__(self, default=None):
        self._data = default
        self._lock = threading.Lock()

    def __repr__(self):
        with self._lock:
            return repr(self._data)

    # read data value
    def get(self):
        with self._lock:
            return self._data

    # write new data value
    def set(self, value):
        with self._lock:
            self._data = value


# thread safe shared variable buffer
class SharedBuffer(BaseBuffer):

    def __init__(self):
        self._data = {}
        self._lock = threading.Lock()

    def __repr__(self):
        with self._lock:
            return repr(self._data)

    # list all keys in buffer
    def keys(self):
        with self._lock:
            return list(self._data.keys())

    # list all items in buffer
    def items(self):
        with self._lock:
            return list(self._data.items())

    # read certain key from buffer
    def get(self, key, default=None):
        with self._lock:
            return self._data.get(key, default)

    # set certain key in buffer
    def set(self, key, value):
        with self._lock:
            self._data[key] = value

    # delete certain key from buffer
    def delete(self, key):
        with self._lock:
            if key in self._data:
                del(self._data[key])

    # purge buffer, delete all keys
    def purge(self):
        with self._lock:
            self._data = {}


# thread safe shared variable queues buffer
class SharedQueueBuffer(SharedBuffer):

    # create new key queue
    def create(self, key):
        with self._lock:
            self._data[key] = SimpleQueue()

    # pop value from key queue
    def get(self, key, default=None):
        with self._lock:
            if key in self._data:
                try:
                    return self._data[key].get_nowait()
                except:
                    pass
        return default

    # push value in key queue and create if not exist
    def set(self, key, value):
        with self._lock:
            if key not in self._data:
                self._data[key] = SimpleQueue()
            self._data[key].put_nowait(value)

    # push value in key queue if exist
    def put(self, key, value):
        with self._lock:
            if key in self._data:
                self._data[key].put_nowait(value)
                return True
        return False

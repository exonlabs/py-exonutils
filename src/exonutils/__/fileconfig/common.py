# -*- coding: utf-8 -*-
import os
import copy
import json
import base64

__all__ = []


# base configuration file handler
class BaseFileConfig(object):

    # char for buffer sub-keys
    subkey_char = '.'

    def __init__(self, file_path, defaults=None):
        # config file path on system
        self.file_path = file_path
        # buffer holding config data
        self.buffer = {}

        # load config
        self.load(defaults=defaults)

    def __repr__(self):
        return '<%s: %s>' % (
            self.__class__.__name__, self.file_path)

    # mangle bytes data to avoid easy detectable patterns, inverting
    # every 2 bytes order. Need to overide function in real applications
    def _mangle(self, blob):
        res = bytearray()
        blob = bytearray(blob)
        l = len(blob) - 1
        for i in range(0, l, 2):
            if (i + 1) < l:
                res.append(blob[i + 1])
            res.append(blob[i])
        res.append(blob[l])
        return res

    # de-mangle bytes data inverting every 2 bytes order.
    # Need to overide function in real applications
    def _demangle(self, blob):
        return self._mangle(blob)

    # low level basic data encoding
    # --> overide function in real applications
    def _encode(self, value):
        return self._mangle(
            base64.b64encode(json.dumps(value).encode()))

    # low level basic value decoding
    # --> overide function in real applications
    def _decode(self, blob):
        return json.loads(
            base64.b64decode(self._demangle(blob)))

    # merge 2 dicts recursively
    def _merge_dicts(self, src, updt):
        res = {k: copy.deepcopy(src[k])
               for k in src.keys() if k not in updt}
        for k in updt.keys():
            if type(src.get(k)) is dict and type(updt[k]) is dict:
                res[k] = self._merge_dicts(src[k], updt[k])
            else:
                res[k] = copy.deepcopy(updt[k])

        return res

    # load config buffer from file and merge with defaults
    def load(self, defaults=None):
        raise NotImplementedError()

    # save current config buffer to file
    def save(self):
        raise NotImplementedError()

    # dump config file contents
    def dump(self):
        raise NotImplementedError()

    # list all keys in buffer
    def keys(self):
        if type(self.buffer) is not dict:
            raise ValueError("invalid buffer data type")

        return self.buffer.keys()

    # get certain key from config
    def get(self, key, default=None, decode=False):
        if not key or type(key) is not str:
            raise ValueError("invalid key value")

        if type(self.buffer) is not dict:
            raise ValueError("invalid buffer data type")

        try:
            res = eval("self.buffer['%s']"
                       % key.replace(self.subkey_char, "']['"))
        except (SyntaxError, KeyError):
            return default

        if decode:
            try:
                return self._decode(bytes.fromhex(str(res)))
            except Exception:
                raise ValueError("failed decoding data for key: %s" % key)

        return res

    # set certain key in config
    def set(self, key, value, encode=False):
        if not key or type(key) is not str:
            raise ValueError("invalid key value")

        if type(self.buffer) is not dict:
            raise ValueError("invalid buffer data type")

        if encode:
            try:
                val = self._encode(value).hex()
            except Exception:
                raise ValueError("failed encoding data for key: %s" % key)
        else:
            val = copy.deepcopy(value)

        if self.subkey_char in key:
            kparts = key.split(self.subkey_char)
            kparts.reverse()
            sub_dict = {kparts[0]: val}
            for n in kparts[1:]:
                sub_dict = {n: sub_dict}
            self.buffer = self._merge_dicts(self.buffer, sub_dict)
        else:
            self.buffer[key] = val

    # delete certain key from config
    def delete(self, key):
        if not key or type(key) is not str:
            raise ValueError("invalid key value")

        try:
            exec("del(self.buffer['%s'])"
                 % key.replace(self.subkey_char, "']['"))
        except (SyntaxError, KeyError):
            pass

    # purge config file
    def purge(self):
        self.buffer = {}
        if os.path.exists(self.file_path):
            os.unlink(self.file_path)

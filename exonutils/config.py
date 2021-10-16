# -*- coding: utf-8 -*-
"""
    :copyright: 2021, ExonLabs. All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
import os
import copy
import pickle
import json
import base64

__all__ = ['BaseFileConfig', 'BlobFileConfig', 'JsonFileConfig']


# base configuration file handler
class BaseFileConfig(object):

    # prefix char for encode/decode buffer keys
    coding_char = '~'

    # char for buffer sub-keys
    subkey_char = '.'

    def __init__(self, filepath, defaults=None):
        # config file path on system
        self.filepath = filepath
        # buffer holding config data
        self.buffer = {}

        self.load(defaults=defaults)

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self.filepath)

    # mangle bytes data to avoid easy detectable patterns,
    # simple invert every 2 bytes order
    def _mangle(self, blob):
        res = bytearray()
        l = len(blob) - 1
        for i in range(0, l, 2):
            if (i + 1) < l:
                res.append(blob[i + 1])
            res.append(blob[i])
        res.append(blob[l])
        return res

    # de-mangle bytes data
    def _demangle(self, blob):
        return self._mangle(blob)

    # low level value encoding
    def _encode(self, value):
        data = base64.b64encode(pickle.dumps(value))
        return ''.join(['{:02x}'.format(k) for k in self._mangle(data)])

    # low level value decoding
    def _decode(self, value):
        data = self._demangle(bytearray.fromhex(value))
        return pickle.loads(base64.b64decode(data))

    # apply format function to dict values recursively
    def _format_dict(self, d1, fmt):
        for k in list(d1.keys()):
            if k[0] == self.coding_char:
                d1[k] = fmt(d1[k])
            elif type(d1[k]) is dict:
                d1[k] = self._format_dict(d1[k], fmt)
        return d1

    # merge 2 dicts recursively
    def _merge_dicts(self, src_dict, updt_dict):
        res = copy.deepcopy(src_dict)
        for k in list(updt_dict.keys()):
            if type(res.get(k)) is dict and type(updt_dict[k]) is dict:
                res[k] = self._merge_dicts(res[k], updt_dict[k])
            else:
                res[k] = copy.deepcopy(updt_dict[k])
        return res

    # load config buffer from file
    def load(self, defaults=None):
        raise NotImplementedError()

    # save current config buffer to file
    def save(self):
        raise NotImplementedError()

    # dump config file contents
    def dump(self):
        raise NotImplementedError()

    # purge config file
    def purge(self):
        if os.path.exists(self.filepath):
            os.unlink(self.filepath)

    # list all keys in buffer
    def keys(self):
        return self.buffer.keys()

    # get certain key from config
    def get(self, key, default=None):
        try:
            if not key:
                return self.buffer
            else:
                return eval("self.buffer['%s']" % (
                    key.replace(self.subkey_char, "']['")))
        except:
            pass
        return default

    # set certain key in config
    def set(self, key, value):
        try:
            if not key:
                self.buffer = copy.deepcopy(value)
            elif self.subkey_char in key:
                kparts = key.split(self.subkey_char)
                kparts.reverse()
                sub_dict = {kparts[0]: value}
                for n in kparts[1:]:
                    sub_dict = {n: sub_dict}
                self.buffer = self._merge_dicts(self.buffer, sub_dict)
            else:
                self.buffer[key] = copy.deepcopy(value)
            return True
        except:
            pass
        return False

    # delete certain key from config
    def delete(self, key):
        try:
            if not key:
                self.buffer = {}
            else:
                exec("del(self.buffer['%s'])" % (
                    key.replace(self.subkey_char, "']['")))
            return True
        except:
            pass
        return False


# binary config file handler
class BlobFileConfig(BaseFileConfig):

    # load config buffer from file and merge with defaults
    def load(self, defaults=None):
        data = None
        if os.path.exists(self.filepath):
            with open(self.filepath, 'r') as f:
                blob = f.read()
            data = self._decode(blob)
        self.buffer = self._merge_dicts(defaults or {}, data or {})

    # save current config buffer to file
    def save(self):
        blob = self._encode(self.buffer)
        with open(self.filepath, 'wb') as f:
            f.write(blob.encode())

    # dump config file contents
    def dump(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, 'rb') as f:
                return bytes(f.read())
        return bytes()


# json config file handler
class JsonFileConfig(BaseFileConfig):

    # load config buffer from file and merge with defaults
    def load(self, defaults=None):
        data = None
        if os.path.exists(self.filepath):
            with open(self.filepath, 'r') as f:
                data = self._format_dict(json.load(f), self._decode)
        self.buffer = self._merge_dicts(defaults or {}, data or {})

    # save current config buffer to file
    def save(self):
        data = self._format_dict(
            copy.deepcopy(self.buffer), self._encode)
        with open(self.filepath, 'w') as f:
            json.dump(data, f, indent=2)

    # dump config file contents
    def dump(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, 'r') as f:
                return f.read().decode()
        return ''

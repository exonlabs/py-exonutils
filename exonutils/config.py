# -*- coding: utf-8 -*-
"""
    :copyright: 2020, ExonLabs. All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
import os
import copy
import pickle
try:
    import simplejson as json
except ImportError:
    import json

__all__ = ['BaseFileConfig', 'PickleFileConfig', 'JsonFileConfig']


# python 2/3 compatible unicode to string conversion
def _str(value):
    try:
        if type(value) is unicode:
            return str(value)
    except:
        pass
    return value


# base configuration file handler
class BaseFileConfig(object):

    # prefix char for encode/decode dict keys
    encoding_char = '.'

    def __init__(self, filepath, defaults=None):
        self.filepath = filepath
        self.defaults = defaults if type(defaults) is dict else {}
        self.data = {}

        self.load()

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self.filepath)

    # low level read and parse config file into dict
    def _load(self):
        raise NotImplementedError()

    # low level write config dict into file
    def _save(self, cfg):
        raise NotImplementedError()

    # low level delete config file
    def _purge(self):
        raise NotImplementedError()

    # low level value encoding
    def _encode(self, value):
        blob = bytearray(pickle.dumps(value))
        return ''.join(['{:02X}'.format(k) for k in blob]).upper()

    # low level value decoding
    def _decode(self, value):
        return pickle.loads(bytearray.fromhex(value))

    # search and encode dict keys recursively
    def _encode_dict(self, d1):
        for k, v in d1.items():
            if type(_str(k)) is str and _str(k[0]) == self.encoding_char:
                d1[k] = self._encode(v)
            elif type(v) is dict:
                d1[k] = self._encode_dict(v)
        return d1

    # search and decode dict keys recursively
    def _decode_dict(self, d1):
        for k, v in d1.items():
            if type(_str(k)) is str and _str(k[0]) == self.encoding_char:
                d1[k] = self._decode(v)
            elif type(v) is dict:
                d1[k] = self._decode_dict(v)
        return d1

    # merge 2 dicts recursively
    def _merge_dicts(self, d1, d2):
        res = copy.deepcopy(d1)
        for k, v in d2.items():
            if k in d1 and type(d1[k]) is dict and type(v) is dict:
                res[k] = self._merge_dicts(d1[k], v)
            else:
                res[k] = copy.deepcopy(v)
        return res

    # load config object
    def load(self):
        data = self._decode_dict(self._load())
        self.data = self._merge_dicts(self.defaults, data)

    # save config object
    def save(self):
        data = copy.deepcopy(self.data)
        self._save(self._encode_dict(data))

    # purge config file
    def purge(self):
        self._purge()

    # list all keys in config
    def keys(self):
        return self.data.keys()

    # list all items in config
    def items(self):
        return self.data.items()

    # get certain key from config
    def get(self, key, default=None):
        return self.data.get(key, default)

    # set certain key in config
    def set(self, key, value):
        self.data[key] = value

    # delete certain key from config
    def delete(self, key):
        if key in self.data:
            del(self.date[key])


# pickled config file handler
class PickleFileConfig(BaseFileConfig):

    # low level read pickled file and parse config into dict
    def _load(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, 'rb') as f:
                return pickle.load(f)
        return {}

    # low level write config dict into pickled file
    def _save(self, cfg):
        with open(self.filepath, 'wb') as f:
            pickle.dump(cfg, f)

    # purge config file
    def _purge(self):
        if os.path.exists(self.filepath):
            os.unlink(self.filepath)


# json config file handler
class JsonFileConfig(BaseFileConfig):

    # low level read json file and parse config into dict
    def _load(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, 'r') as f:
                return json.load(f)
        return {}

    # low level write config dict into json file
    def _save(self, cfg):
        with open(self.filepath, 'w') as f:
            json.dump(cfg, f, indent=2)

    # purge config file
    def _purge(self):
        if os.path.exists(self.filepath):
            os.unlink(self.filepath)

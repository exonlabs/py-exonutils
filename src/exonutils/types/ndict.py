# -*- coding: utf-8 -*-
from typing import Any

__all__ = []

# nested keys seperator
sepNDict = "."


# Nested Dict type with nested keys support
class NDict(dict):

    # create new NDict from initial dict data
    def __init__(self, buff: dict = None):
        if not buff:
            return
        # delete empty keys
        if "" in buff:
            del buff[""]
        # recursive conversion
        from .dict import Dict
        for key, value in buff.items():
            if type(value) in [dict, Dict, NDict]:
                self[key] = NDict(value)
            elif type(value) in [list, tuple]:
                b = []
                for v in value:
                    if type(v) in [dict, Dict, NDict]:
                        b.append(NDict(v))
                    else:
                        b.append(v)
                self[key] = b
            else:
                self[key] = value

    # dict built-in keys function call
    def __keys(self) -> list[str]:
        return list(super(NDict, self).keys())

    # return list up to N level nested _keys
    def _keys(self, lvl: int) -> list[str]:
        keys = []
        for k in self.__keys():
            if lvl != 1:
                if type(self[k]) is NDict:
                    for sk in self[k]._keys(lvl - 1):
                        keys.append(k + sepNDict + sk)
                    continue
            keys.append(k)
        return keys

    # return sorted list of all nested level keys
    def keys(self) -> list[str]:
        keys = self._keys(-1)
        if len(keys) > 0:
            return sorted(keys)
        return keys

    # return sorted recursive list up to N level nested keys
    def keys_n(self, lvl: int) -> list[str]:
        keys = self._keys(lvl)
        if len(keys) > 0:
            return sorted(keys)
        return keys

    # check if key exist in dict
    def is_exist(self, key: str) -> bool:
        k = key.split(sepNDict, 1)
        if k[0] in self.__keys():
            # not nested key
            if len(k) == 1:
                return True
            # value is of type NDict
            if type(self[k[0]]) is NDict:
                return self[k[0]].is_exist(k[1])
        return False

    # get value from dict by key or return default value
    def get(self, key: str, defval: Any = None) -> Any:
        k = key.split(sepNDict, 1)
        if k[0] in self.__keys():
            # not nested key
            if len(k) == 1:
                return self[k[0]]
            # value is of type NDict
            if type(self[k[0]]) is NDict:
                return self[k[0]].get(k[1], defval)
        return defval

    # set value in dict by key
    def set(self, key: str, newval: Any):
        if len(key) != 0:
            k = key.split(sepNDict, 1)
            # not nested key
            if len(k) == 1:
                self[k[0]] = newval
            else:
                # 1st level key not exist or not of type Dict
                if not (k[0] in self and type(self[k[0]]) is NDict):
                    self[k[0]] = NDict({})
                self[k[0]].set(k[1], newval)

    # delete value from dict by key
    def delete(self, key: str):
        if len(key) != 0:
            k = key.split(sepNDict, 1)
            if k[0] in self:
                # not nested key
                if len(k) == 1:
                    del self[k[0]]
                    return
                # value is of type Dict
                if type(self[k[0]]) is NDict:
                    self[k[0]].delete(k[1])

    # update dict from updt dict
    def update(self, updt: dict):
        buff = NDict(updt)
        for key in buff.keys():
            if len(key) != 0:
                self.set(key, buff.get(key, None))

    # delete all values from dict
    def reset(self):
        for k in self.__keys():
            del self[k]


# recursive convert NDict into standard dict data
def StripNDict(buff: NDict) -> dict:
    if buff is None:
        return dict()
    # recursive conversion
    from .dict import Dict
    for key, value in buff.items():
        if type(value) in [dict, Dict, NDict]:
            buff[key] = StripNDict(value)
        elif type(value) in [list, tuple]:
            b = []
            for v in value:
                if type(v) in [dict, Dict, NDict]:
                    b.append(StripNDict(v))
                else:
                    b.append(v)
            buff[key] = b
    return dict(buff)


# create deep clone of NDict
def CloneNDict(src: NDict) -> NDict:
    from copy import deepcopy
    return deepcopy(src)

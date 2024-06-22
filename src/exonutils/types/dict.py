# -*- coding: utf-8 -*-
from typing import Any

__all__ = []


# Nested Dict type with nested keys support
class Dict(dict):

    # create new Dict from initial dict data
    def __init__(self, buff: dict = None):
        if not buff:
            return
        # delete empty keys
        if "" in buff:
            del buff[""]
        # recursive conversion
        from .ndict import NDict
        for key, value in buff.items():
            if type(value) in [dict, Dict, NDict]:
                self[key] = Dict(value)
            elif type(value) in [list, tuple]:
                b = []
                for v in value:
                    if type(v) in [dict, Dict, NDict]:
                        b.append(Dict(v))
                    else:
                        b.append(v)
                self[key] = b
            else:
                self[key] = value

    # dict built-in keys function call
    def __keys(self) -> list[str]:
        return list(super(Dict, self).keys())

    # return sorted list of all nested level keys
    def keys(self) -> list[str]:
        keys = list(self.__keys())
        if len(keys) > 0:
            return sorted(keys)
        return keys

    # check if key exist in dict
    def is_exist(self, key: str) -> bool:
        return key in self

    # get value from dict by key or return default value
    def get(self, key: str, defval: Any = None) -> Any:
        if key in self:
            return self[key]
        return defval

    # set value in dict by key
    def set(self, key: str, newval: Any):
        if len(key) != 0:
            self[key] = newval

    # delete value from dict by key
    def delete(self, key: str):
        if len(key) != 0 and key in self:
            del self[key]

    # update dict from updt dict
    def update(self, updt: dict):
        for key, val in updt.items():
            if len(key) != 0:
                self[key] = val

    # delete all values from dict
    def reset(self):
        for k in self.__keys():
            del self[k]


# recursive convert Dict into standard dict data
def StripDict(buff: Dict) -> dict:
    if buff is None:
        return dict()
    # recursive conversion
    from .ndict import NDict
    for key, value in buff.items():
        if type(value) in [dict, Dict, NDict]:
            buff[key] = StripDict(value)
        elif type(value) in [list, tuple]:
            b = []
            for v in value:
                if type(v) in [dict, Dict, NDict]:
                    b.append(StripDict(v))
                else:
                    b.append(v)
            buff[key] = b
    return dict(buff)


# create deep clone of Dict
def CloneDict(src: Dict) -> Dict:
    from copy import deepcopy
    return deepcopy(src)

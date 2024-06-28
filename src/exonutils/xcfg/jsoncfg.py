# -*- coding: utf-8 -*-
import json

from .filecfg import FileConfig

__all__ = []


# json file config
class JsonConfig(FileConfig):

    # load serialized bytes data into internal dict buffer
    def _loader(self, buff: bytes):
        if buff:
            data = json.loads(buff)
            self.update(data)

    # dump internal dict buffer to serialized bytes data
    def _dumper(self) -> bytes:
        s = json.dumps(self, indent=2, ensure_ascii=False)
        return (s + "\n").encode("utf8")

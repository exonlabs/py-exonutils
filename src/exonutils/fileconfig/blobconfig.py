# -*- coding: utf-8 -*-
import os

from .common import BaseFileConfig

__all__ = []


# binary config file handler
class BlobFileConfig(BaseFileConfig):

    # load config buffer from file and merge with defaults
    def load(self, defaults=None):
        if defaults is not None and type(defaults) is not dict:
            raise ValueError("invalid defaults data type")

        data = None
        if os.path.exists(self.file_path):
            with open(self.file_path, 'rb') as fh:
                data = self._decode(fh.read())
            if data is not None and type(data) is not dict:
                raise ValueError(
                    "invalid data contents of file: %s" % self.file_path)

        self.buffer = self._merge_dicts(defaults or {}, data or {})

    # save current config buffer to file
    def save(self):
        if type(self.buffer) is not dict:
            raise ValueError("invalid buffer data type")

        with open(self.file_path, 'wb') as fh:
            fh.write(self._encode(self.buffer))

    # dump config file contents
    def dump(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'rb') as fh:
                return bytes(fh.read())

        return bytes()

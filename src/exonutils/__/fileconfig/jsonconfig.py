# -*- coding: utf-8 -*-
import os
import json

from .common import BaseFileConfig

__all__ = []


# json config file handler
class JsonFileConfig(BaseFileConfig):

    # load config buffer from file and merge with defaults
    def load(self, defaults=None):
        if defaults is not None and type(defaults) is not dict:
            raise ValueError("invalid defaults data type")

        data = None
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as fh:
                data = json.load(fh)
            if data is not None and type(data) is not dict:
                raise ValueError(
                    "invalid data contents of file: %s" % self.file_path)

        self.buffer = self._merge_dicts(defaults or {}, data or {})

    # save current config buffer to file
    def save(self):
        if type(self.buffer) is not dict:
            raise ValueError("invalid buffer data type")

        with open(self.file_path, 'w') as fh:
            json.dump(self.buffer, fh, indent=2)

    # dump config file contents
    def dump(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as fh:
                return fh.read()

        return ''

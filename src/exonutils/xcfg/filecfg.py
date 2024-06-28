# -*- coding: utf-8 -*-
import os
import json
from typing import Any
from abc import ABCMeta
from base64 import b64encode, b64decode

from exonutils.types import NDict
from exonutils.crypto import xcipher

__all__ = []


# configuration file handler
class FileConfig(NDict, metaclass=ABCMeta):

    # config filepath on disk
    _filepath: str = ""
    _bakpath:  str = ""

    # cipher object
    _cipher = None

    def __init__(self, path: str, defaults: dict = None):
        super(FileConfig, self).__init__(buff=defaults)
        self._filepath = path

    # enable config file backup support
    def enable_backup(self, bakpath: str = ""):
        if bakpath:
            bakpath = os.path.realpath(bakpath)
            dirpath = os.path.dirname(bakpath)
            if bakpath == os.path.sep or bakpath == dirpath:
                raise ValueError("invalid config backup path")
            self._bakpath = bakpath
        else:
            self._bakpath = self._filepath + ".backup"

    # check config file exist on disk
    def is_file_exist(self) -> bool:
        return os.path.exists(self._filepath)

    # check backup config file exist on disk, if backup support enabled
    def is_bakfile_exist(self) -> bool:
        if self._bakpath:
            return os.path.exists(self._bakpath)
        return False

    # load serialized bytes data into internal dict buffer
    def _loader(self, buff: bytes):
        raise NotImplementedError()

    # dump internal dict buffer to serialized bytes data
    def _dumper(self) -> bytes:
        raise NotImplementedError()

    # read raw bytes content of config file, if error: then check and
    # read the backup file if backup support enabled.
    def load(self):
        if self._filepath in [os.path.sep, os.path.dirname(self._filepath)]:
            raise ValueError("invalid config file path")

        if self.is_file_exist():
            try:
                with open(self._filepath, 'rb') as f:
                    b = f.read()
                self._loader(b)
                self._save_backup(b)
                return
            except Exception:
                pass

        if self.is_bakfile_exist():
            try:
                with open(self._bakpath, 'rb') as f:
                    b = f.read()
                self._loader(b)
                self.save()
                return
            except Exception:
                pass

    # write raw bytes content to config file, if not error: then check and
    # write backup config if backup support enabled.
    def save(self):
        if self._filepath in [os.path.sep, os.path.dirname(self._filepath)]:
            raise ValueError("invalid config file path")

        buff = self._dumper()
        with open(self._filepath, "wb+") as f:
            f.write(buff)
        os.chmod(self._filepath, 0o666)
        self._save_backup(buff)

    def _save_backup(self, buff: bytes):
        if self._bakpath:
            with open(self._bakpath, "wb+") as f:
                f.write(buff)
            os.chmod(self._bakpath, 0o666)

    # delete config and backup files from disk and reset local buffer
    def purge(self):
        if self._filepath in [os.path.sep, os.path.dirname(self._filepath)]:
            raise ValueError("invalid config file path")
        self.reset()
        if self.is_bakfile_exist():
            os.unlink(self._bakpath)
        if self.is_file_exist():
            os.unlink(self._filepath)

    # ##########################################

    def init_aes128(self, secret: str):
        self._cipher = xcipher.AES128(secret)

    def init_aes256(self, secret: str):
        self._cipher = xcipher.AES256(secret)

    # get secure value from config by key
    def get_secure(self, key: str, defval: Any = None) -> Any:
        if not self._cipher:
            raise RuntimeError("security is not configured")

        data = self.get(key)
        if data is None:
            # key not exist
            return defval

        if type(data) is not str:
            raise ValueError("invalid value format")
        if len(data) == 0:
            # empty key
            return defval

        b = b64decode(data.encode("ascii"))
        b = self._cipher.decrypt(b)
        return json.loads(b.decode("utf8"))

    # set secure value in config by key, creates key if not exist
    def set_secure(self, key: str, val: Any):
        if not self._cipher:
            raise RuntimeError("security is not configured")

        b = json.dumps(val).encode("utf8")
        b = self._cipher.encrypt(b)
        self.set(key, b64encode(b).decode("ascii"))

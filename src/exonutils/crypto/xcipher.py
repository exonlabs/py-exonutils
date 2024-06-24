# -*- coding: utf-8 -*-
import os
from abc import ABCMeta
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes


class Cipher(metaclass=ABCMeta):

    _aead: AESGCM = None
    _aad: bytes = None
    _nounce_size: int = 12

    def __init__(self, key: bytes):
        key = bytearray(key)
        n = int(len(key) / 2)
        # mangle key first half bytes
        for i in range(0, n, 2):
            key[i], key[i+1] = key[i+1], key[i]
        self._aead = AESGCM(key[n:])
        self._aad = key[:n]

    def encrypt(self, in_buff: bytes) -> bytes:
        if not in_buff:
            raise ValueError("malformed data for encryption")
        nonce = os.urandom(self._nounce_size)
        out_buff = self._aead.encrypt(nonce, in_buff, self._aad)
        return nonce + out_buff

    def decrypt(self, in_buff: bytes) -> bytes:
        if not in_buff or len(in_buff) <= self._nounce_size:
            raise ValueError("malformed data for decryption")
        nonce = in_buff[:self._nounce_size]
        return self._aead.decrypt(
            nonce, in_buff[self._nounce_size:], self._aad)


class AES128(Cipher):

    def __init__(self, secret: str):
        digest = hashes.Hash(hashes.SHA256())
        digest.update(secret.encode("utf8"))
        super(AES128, self).__init__(digest.finalize())


class AES256(Cipher):

    def __init__(self, secret: str):
        digest = hashes.Hash(hashes.SHA512())
        digest.update(secret.encode("utf8"))
        super(AES256, self).__init__(digest.finalize())

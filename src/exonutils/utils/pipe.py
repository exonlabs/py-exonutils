# -*- coding: utf-8 -*-
import os
import time
from select import select


# Named Pipes
class Pipe(object):

    @classmethod
    def open(cls, path, perm=0o666):
        if os.path.exists(path):
            os.unlink(path)
        os.umask(0o000)
        os.mkfifo(path, perm)

    @classmethod
    def close(cls, path):
        if os.path.exists(path):
            os.unlink(path)

    # send data on named pipe
    # return: True on send success, False if no peer
    @classmethod
    def send(cls, path, data, wait_peer=True):
        if wait_peer:
            fd = os.open(path, os.O_WRONLY)
        else:
            try:
                fd = os.open(path, os.O_WRONLY | os.O_NONBLOCK)
            except Exception:
                # no peer connected
                return False
        try:
            os.write(fd, data)
        finally:
            os.close(fd)

        return True

    # wait data from named pipe
    # return string: received data
    @classmethod
    def recv(cls, path, size=1024, timeout=5, break_event=None):
        ts = time.time() + timeout
        while time.time() < ts and \
                not (break_event and break_event.is_set()):
            fd = None
            try:
                fd = os.open(path, os.O_RDONLY | os.O_NONBLOCK)
                if select((fd, ), (), (), 0.2)[0]:
                    res = os.read(fd, size)
                    if res:
                        return res
            finally:
                if fd:
                    os.close(fd)

        return bytes()

    # send command on named pipe and wait reply
    # return:
    #   - None: if wait_reply is False
    #   - string: reply string
    @classmethod
    def send_wait(cls, path, data, wait_peer=True, size=1024, timeout=5):
        if not cls.send(path, data, wait_peer=wait_peer):
            raise RuntimeError("no peer connected")

        res = cls.recv(path, size=size, timeout=timeout)
        if res:
            return res

        raise RuntimeError('timeout')

# -*- coding: utf-8 -*-
import os
import time
import threading
from select import select


# Named Pipes
class NamedPipe(object):

    def __init__(self, path):
        self.path = path

        # polling delay for operations
        self.polling_delay = 0.2
        # delay for send operations
        self.send_delay = 0.1
        # delay for recv operations
        self.recv_delay = 0.1
        # chunck size of bytes to read at a time
        self.recv_size = 1024

        # cancel operations event
        self.cancel_event = threading.Event()

    def open(self, perm=0o666):
        self.close()

        os.umask(0o000)
        os.mkfifo(self.path, perm)

    def close(self):
        if os.path.exists(self.path):
            os.unlink(self.path)

    def cancel(self):
        self.cancel_event.set()

    # send data on named pipe
    # return: True on send success, False if no peer
    def send(self, data, timeout=0):
        fd = None
        try:
            break_ts = time.time() + timeout
            while True:
                try:
                    fd = os.open(self.path, os.O_WRONLY | os.O_NONBLOCK)
                    break
                except Exception:
                    pass

                # operation canceled
                if self.cancel_event.wait(timeout=self.polling_delay):
                    return False

                # no peer connected until timeout
                if timeout and time.time() >= break_ts:
                    return False

            # send data on pipe
            os.write(fd, data)

            os.close(fd)
            fd = None

            # small delay to allow finishing read from pipe
            time.sleep(self.send_delay)

            return True

        except Exception:
            raise
        finally:
            if fd:
                os.close(fd)

        return False

    # wait data from named pipe
    # return bytes: received data
    def recv(self, timeout=0):
        fd = None
        try:
            fd = os.open(self.path, os.O_RDONLY | os.O_NONBLOCK)

            break_ts = time.time() + timeout
            while True:
                if select((fd, ), (), (), self.polling_delay)[0]:
                    break

                # operation canceled
                if self.cancel_event.is_set():
                    return bytes()

                # no peer connected until timeout
                if timeout and time.time() >= break_ts:
                    return bytes()

            # recv data from pipe
            data = bytes()
            while True:
                if select((fd, ), (), (), self.recv_delay)[0]:
                    d = os.read(fd, self.recv_size)
                    if not d:
                        break
                    data += d

            os.close(fd)
            fd = None

            return data

        except Exception:
            raise
        finally:
            if fd:
                os.close(fd)

        return bytes()

    # send command on named pipe and wait reply
    # return:
    #   - None: if wait_reply is False
    #   - string: reply string
    def send_wait(self, data, timeout=0):
        if not self.send(data, timeout=timeout):
            raise RuntimeError("no peer connected")

        res = self.recv(timeout=timeout)
        if res:
            return res

        raise RuntimeError('timeout')

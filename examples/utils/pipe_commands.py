# -*- coding: utf-8 -*-
import os
import time
from tempfile import gettempdir

from exonutils.utils.pipe import Pipe


def main():
    fpath = os.path.join(gettempdir(), 'foobar.pipe')

    try:
        print("\nOpen Pipe: %s" % fpath)
        Pipe.open(fpath)

        time.sleep(3)

        print("\nChecking Peer")
        if Pipe.send(fpath, b"HELLO\n", wait_peer=False):
            print("-- Peer Connected")
        else:
            print("-- No Peer")

        msg = "MY_MESSAGE\n"
        print("\nSending Message: %s" % msg.strip())
        Pipe.send(fpath, msg.encode())

        print("\nReceiving:")
        try:
            res = Pipe.recv(fpath, timeout=5)
            if res:
                print("-- received: %s" % res.decode().strip())
            else:
                print("-- timeout")
        except Exception as e:
            print("-- error: %s" % e)

        msg = "COMMAND\n"
        print("\nSend Wait: %s" % msg.strip())
        try:
            res = Pipe.send_wait(fpath, msg.encode(), timeout=5)
            print("-- received: %s" % res.decode().strip())
        except Exception as e:
            print("-- error: %s" % e)

    finally:
        print("\nClose pipe")
        Pipe.close(fpath)

    print()


if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        print("\n-- terminated --")

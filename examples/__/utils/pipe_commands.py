# -*- coding: utf-8 -*-
import os
from tempfile import gettempdir

from exonutils.utils.pipe import NamedPipe


def main():
    fpath = os.path.join(gettempdir(), 'foobar.pipe')

    try:
        pipe = NamedPipe(fpath)

        print("\nOpen Pipe: %s" % fpath)
        pipe.open()

        print("\nChecking Peer")
        if pipe.send(b"HELLO\n", timeout=5):
            print("-- Peer Connected")
        else:
            print("-- No Peer yet")

        msg = "MY_MESSAGE\n"
        print("\nSending Message (waiting peer): %s" % msg.strip())
        pipe.send(msg.encode())

        print("\nReceiving:")
        try:
            res = pipe.recv(timeout=5)
            if res:
                print("-- received: %s" % res.decode().strip())
            else:
                print("-- timeout")
        except Exception as e:
            print("-- error: %s" % e)

        msg = "COMMAND\n"
        print("\nSend Wait: %s" % msg.strip())
        try:
            res = pipe.send_wait(msg.encode(), timeout=5)
            print("-- received: %s" % res.decode().strip())
        except Exception as e:
            print("-- error: %s" % e)

    finally:
        print("\nClose pipe")
        pipe.close()

    print()


if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        print("\n-- terminated --")

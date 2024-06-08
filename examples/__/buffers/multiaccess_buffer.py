# -*- coding: utf-8 -*-
import time
import threading

from exonutils.buffers.filebuffer import SimpleFileBuffer

buff = None
lock = threading.Lock()


def reader_task():
    global buff, lock

    while True:
        try:
            print("\n-- buffer data --")
            with lock:
                data = buff.items()
            for k, v in data:
                print("  %s = %s" % (k, v))
        except Exception as e:
            print(e)

        time.sleep(1)


def writer_task():
    global buff, lock

    while True:
        try:
            with lock:
                counter = buff.get('counter')
                if counter is None:
                    buff.set('counter', 0)
                else:
                    buff.set('counter_old', counter)
                    buff.set('counter', counter + 1)
        except Exception as e:
            print(e)

        time.sleep(3)


def main():
    global buff

    try:
        buff = SimpleFileBuffer('SampleBuffer')
        buff.set('counter_old', 0)

        t1 = threading.Thread(target=reader_task, daemon=True)
        t1.start()

        t2 = threading.Thread(target=writer_task, daemon=True)
        t2.start()

        t1.join()
        t2.join()

    except Exception:
        raise
    except (KeyboardInterrupt, SystemExit):
        print("\n")
    finally:
        if buff:
            buff.purge()


if __name__ == '__main__':
    main()

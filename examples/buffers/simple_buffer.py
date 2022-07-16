# -*- coding: utf-8 -*-
from pprint import pprint

from exonutils.buffers.filebuffer import SimpleFileBuffer


def main():
    try:
        buff = None

        # create new buffer
        buff = SimpleFileBuffer('SampleBuffer')

        # fill keys
        buff.set('key1', None)
        buff.set('key2', 123)
        buff.set('key3', 123.456)
        buff.set('key4', 'string_value')
        buff.set('key5', b'bytes_value')
        buff.set('key6', u'utf8_value')
        buff.set('key7', 'عربي')
        buff.set('key8', u'عربي')

        buff.set('دليل1', None)
        buff.set('دليل2', 123)
        buff.set('دليل3', 123.456)
        buff.set('دليل4', 'string_value')
        buff.set('دليل5', b'bytes_value')
        buff.set('دليل6', u'utf8_value')
        buff.set('دليل7', 'عربي')
        buff.set('دليل8', u'عربي')

        # list buffer items
        print("\n-- Buffer Items --")
        for k in sorted(buff.keys()):
            print(k, buff.get(k))

        # list buffer as dict
        print("\n-- Buffer as Dict --")
        pprint(dict(buff.items()))

        print()

    except Exception:
        raise
    finally:
        if buff:
            buff.purge()


if __name__ == '__main__':
    main()

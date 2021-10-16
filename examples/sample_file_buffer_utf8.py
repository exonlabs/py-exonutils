# -*- coding: utf-8 -*-
import sys
import logging
from argparse import ArgumentParser
from traceback import format_exc

from exonutils.buffers import FileBuffer

logging.basicConfig(
    level=logging.INFO, stream=sys.stdout,
    format='%(asctime)s [%(name)s] %(levelname)s %(message)s')


if __name__ == '__main__':
    logger = logging.getLogger()
    logger.name = 'FileBuffer'
    try:
        pr = ArgumentParser(prog=None)
        pr.add_argument('-x', dest='debug', action='store_true',
                        help='enable debug mode')
        args = pr.parse_args()

        if args.debug:
            logger.setLevel(logging.DEBUG)

        buff = FileBuffer('SampleBuffer')

        buff.set('key1', None)
        buff.set('key2', 123)
        buff.set('key3', 123.456)
        buff.set('key4', 'string_value')
        buff.set('key5', b'bytes_value')
        buff.set('key6', u'utf_value')
        buff.set('key7', 'عربي')
        buff.set('key8', u'عربي')

        buff.set('دليل1', None)
        buff.set('دليل2', 123)
        buff.set('دليل3', 123.456)
        buff.set('دليل4', 'string_value')
        buff.set('دليل5', b'bytes_value')
        buff.set('دليل6', u'utf_value')
        buff.set('دليل7', 'عربي')
        buff.set('دليل8', u'عربي')

        print("buffer data")
        for k in sorted(buff.keys()):
            print(k, buff.get(k))

        buff.purge()

    except Exception:
        logger.fatal(format_exc())
        sys.exit(1)

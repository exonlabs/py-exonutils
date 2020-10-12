# -*- coding: utf-8 -*-
import os
import sys
import logging
import tempfile
# import pickle
from pprint import pprint
from argparse import ArgumentParser
from traceback import format_exc

from exonutils.config import JsonFileConfig

logging.basicConfig(
    level=logging.INFO, stream=sys.stdout,
    format='%(asctime)s [%(name)s] %(levelname)s %(message)s')

CFG_FILE = os.path.join(tempfile.gettempdir(), 'sample_config.json')


if __name__ == '__main__':
    log = logging.getLogger()
    log.name = 'FileConfig'
    try:
        pr = ArgumentParser(prog=None)
        pr.add_argument('-x', dest='debug', action='store_true',
                        help='enable debug mode')
        pr.add_argument('--init', dest='init', action='store_true',
                        help='initialize config file')
        args = pr.parse_args()

        if args.debug:
            log.setLevel(logging.DEBUG)

        print("\n* using cfg file: %s" % CFG_FILE)

        defaults = {
            '.key1': 'some value',
            '.key2': 123,
            'key3': [1, 2, 3],
            'key4': {
                'a': [1, 2, 3],
                'b': {
                    '1': 111,
                    '2': 222,
                    '3': {
                        'x': 'xxx',
                        '.y': 'yyy',
                        'z': 'zzz',
                    },
                },
            },
        }
        print("\n- default config:")
        pprint(defaults)

        if args.init:
            cfg = JsonFileConfig(CFG_FILE, defaults=defaults)
            cfg.purge()
            cfg.save()
            print("\n- config saved")

        cfg = JsonFileConfig(CFG_FILE)
        cfg.set('new_key', 999)

        print("\n- active config:")
        pprint(cfg)
        pprint(list(cfg.keys()))
        pprint(list(cfg.items()))
        print("")

        cfg.purge()

    except Exception:
        log.fatal(format_exc())
        sys.exit(1)

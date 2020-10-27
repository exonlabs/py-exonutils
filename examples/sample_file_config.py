# -*- coding: utf-8 -*-
import os
import sys
import logging
import tempfile
from pprint import pprint
from argparse import ArgumentParser
from traceback import format_exc

from exonutils.config import JsonFileConfig, PickleFileConfig

logging.basicConfig(
    level=logging.INFO, stream=sys.stdout,
    format='%(asctime)s [%(name)s] %(levelname)s %(message)s')

CFG_FILE = os.path.join(tempfile.gettempdir(), 'sample_config')


if __name__ == '__main__':
    log = logging.getLogger()
    log.name = 'FileConfig'
    try:
        pr = ArgumentParser(prog=None)
        pr.add_argument('-x', dest='debug', action='store_true',
                        help='enable debug mode')
        pr.add_argument('--init', dest='init', action='store_true',
                        help='initialize config file')
        pr.add_argument('--pickle', dest='pickle', action='store_true',
                        help='use pickle for saving config files')
        args = pr.parse_args()

        if args.debug:
            log.setLevel(logging.DEBUG)

        if args.pickle:
            FileConfigClass = PickleFileConfig
        else:
            FileConfigClass = JsonFileConfig

        print("\n* using cfg file: %s" % CFG_FILE)

        defaults = {
            '*key1': 'some value',
            '*key2': 123,
            'key3': [1, 2, 3],
            'key4': {
                'a': [1, 2, 3],
                'b': {
                    '1': 111,
                    '2': 222,
                    '3': {
                        'x': 'xxx',
                        '*y': 'yyy',
                        'z': 'zzz',
                    },
                },
            },
        }
        print("\n- default config:")
        pprint(defaults)

        if args.init:
            cfg = FileConfigClass(CFG_FILE, defaults=defaults)
            cfg.set('key4.b.*4', 444)
            cfg.purge()
            cfg.save()
            print("\n- config saved")
            print("-" * 50)
            try:
                print(cfg.dump().decode())
            except:
                print(cfg.dump())
            print("-" * 50)

        cfg = FileConfigClass(CFG_FILE)
        cfg.set('new_key', 999)
        cfg.set('key4.b.3.t', 'ttt')

        print("\n- active config:")
        pprint(cfg)
        pprint(cfg.data.keys())
        pprint(cfg.data)
        print("")

        cfg.purge()

    except Exception:
        log.fatal(format_exc())
        sys.exit(1)

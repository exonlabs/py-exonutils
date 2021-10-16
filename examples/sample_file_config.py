# -*- coding: utf-8 -*-
import os
import sys
import tempfile
from argparse import ArgumentParser
from traceback import format_exc

from exonutils.config import BlobFileConfig, JsonFileConfig

CFG_FILE = os.path.join(
    tempfile.gettempdir(), 'sample_config')


if __name__ == '__main__':
    try:
        pr = ArgumentParser(prog=None)
        pr.add_argument(
            '--init', dest='init', action='store_true',
            help='initialize config file')
        pr.add_argument(
            '--bincfg', dest='bincfg', action='store_true',
            help='use binary config files mode')
        args = pr.parse_args()

        if args.bincfg:
            FileConfig = BlobFileConfig
        else:
            FileConfig = JsonFileConfig

        print("\n* using cfg file: %s" % CFG_FILE)

        defaults = {
            '~key1': 'some value',
            '~key2': {
                'x': 'xxx',
                '~y': 'yyy',
                'z': 'zzz',
            },
            'key3': [1, 2, 3],
            'key4': {
                'a': [1, 2, 3],
                'b': {
                    '1': 111,
                    '2': 222,
                    '3': {
                        'x': 'xxx',
                        '~y': 'yyy',
                        'z': 'zzz',
                    },
                },
            },
            'key7': 'عربي',
            'key8': u'عربي',
            'دليل1': 'عربي',
            '~دليل2': u'عربي',
        }
        print("\n- default config:")
        for k in sorted(defaults.keys()):
            print(k, defaults[k])

        if args.init:
            cfg = FileConfig(CFG_FILE, defaults=defaults)
            cfg.set('key4.b.~4', 444)
            cfg.purge()
            cfg.save()
            print("\n- config saved")
            print("-" * 50)
            print(cfg.dump())
            print("-" * 50)

        cfg = FileConfig(CFG_FILE)
        cfg.set('new_key', 999)
        cfg.set('key4.b.3.t', 'ttt')
        cfg.set('key4.b.دليل', 'vvv')

        print("\n- active config:")
        print(cfg)
        for k in sorted(cfg.keys()):
            print(k, cfg.get(k))
        print("")

        cfg.purge()

    except Exception:
        print(format_exc())
        sys.exit(1)

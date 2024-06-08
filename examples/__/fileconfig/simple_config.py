# -*- coding: utf-8 -*-
import os
import tempfile
from pprint import pprint
from argparse import ArgumentParser

from exonutils.fileconfig.jsonconfig import JsonFileConfig
from exonutils.fileconfig.blobconfig import BlobFileConfig

CFG_FILE = os.path.join(
    tempfile.gettempdir(), 'sample_config')

DEFAULTS = {
    'key1': 'some value',
    'key2': {
        'x': 'xxx',
        'y': 'yyy',
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
                'y': 'yyy',
                'z': 'zzz',
            },
        },
    },
    'key7': 'عربي',
    'key8': u'عربي',
    'دليل1': 'عربي',
    'دليل2': u'عربي',
}


def main():
    try:
        cfg = None

        pr = ArgumentParser(prog=None)
        pr.add_argument(
            '--init', dest='init', action='store_true',
            help='initialize config file')
        pr.add_argument(
            '--blobcfg', dest='blobcfg', action='store_true',
            help='use binary config files mode')
        args = pr.parse_args()

        if args.blobcfg:
            config_cls = BlobFileConfig
        else:
            config_cls = JsonFileConfig

        print("\n* using cfg file: %s" % CFG_FILE)

        if args.init:
            print("\n-- default config:")
            for k in sorted(DEFAULTS.keys()):
                print(k, DEFAULTS[k])

            cfg = config_cls(CFG_FILE, defaults=DEFAULTS)
            cfg.set('key4.b.4', [4, 44, 444], encode=True)
            for n in ['key2.y', 'key3']:
                cfg.set(n, cfg.get(n), encode=True)
            cfg.save()

            print("\n-- config saved")
            print("-" * 50)
            print(cfg.dump())
            print("-" * 50)

        cfg = config_cls(CFG_FILE)
        cfg.set('new_key', 999)
        cfg.set('key4.b.3.t', 'ttt', encode=True)
        cfg.set('key4.b.دليل', 'vvv')

        print("\n-- active config:")
        print(cfg)
        for k in sorted(cfg.keys()):
            print(k, cfg.get(k))

        # list buffer as dict
        print("\n-- Buffer as Dict --")
        pprint(cfg.buffer)

        # read values
        print("\n-- read encoded keys")
        for n in ['key2.y', 'key3', 'key4.b.4', 'key4.b.3.t']:
            print('%s =' % n, cfg.get(n, decode=True))

        print("")

    except Exception:
        raise
    finally:
        if cfg:
            cfg.purge()


if __name__ == '__main__':
    main()

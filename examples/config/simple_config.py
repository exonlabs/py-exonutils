# -*- coding: utf-8 -*-
import os
import tempfile
from pprint import pprint
from argparse import ArgumentParser

from exonutils.xcfg import JsonConfig

CFG_FILE = os.path.join(tempfile.gettempdir(), "sample_config.json")
SECRET = "12345678"

DEFAULTS = {
    "key1": "some value",
    "key2": {
        "1": "xxx",
        "2": "yyy",
        "3": "zzz",
    },
    "key3": [1, 2, 3],
    "key4": {
        "a": [1, 2, 3],
        "b": {
            "1": 111,
            "2": 222,
            "3": {
                "x": "xxx",
                "y": "yyy",
                "z": "zzz",
            },
            "4": None,
        },
    },
    "key7": "7 عربي",
    "key8": u"8 عربي",
    "دليل1": "1 عربي",
    "دليل2": u"2 عربي",
}


def NewConfig():
    cfg = JsonConfig(CFG_FILE, defaults=DEFAULTS)
    cfg.init_aes128(SECRET)
    return cfg


def main():
    pr = ArgumentParser(prog=None)
    pr.add_argument(
        '--init', dest='init', action='store_true',
        help='initialize config file')
    args = pr.parse_args()

    if args.init:
        cfg = NewConfig()
        print("\n* using cfg file: %s" % CFG_FILE)

        # add/set default secure data
        data = {
            "key2.y":   cfg.get("key2.y"),
            "key3":     cfg.get("key3"),
            "key4.b.5": [1, "2", True, 1.2345],
            "key5":     None,
        }
        for k, v in data.items():
            cfg.set_secure(k, v)

        print("\n-- initial config:")
        pprint(cfg)

        print("\n-- saving config")
        cfg.save()

        print("-" * 50)
        print("file contents")
        print("-" * 50)
        with open(CFG_FILE, "rb") as f:
            print(f.read().decode("utf8"))
        print("-" * 50)
        return

    cfg = NewConfig()
    print("\n* using cfg file: %s" % CFG_FILE)
    if cfg.is_file_exist():
        cfg.load()
    print("\n-- loaded config:")
    pprint(cfg)

    cfg.set("new_key", 999)
    cfg.set("key4.b.دليل", "vvv")
    cfg.set("key4.b.3.t", "ttt")
    cfg.delete("key1")
    print("\n-- modified config:")
    pprint(cfg)

    print("\n-- config keys/values:")
    for k in cfg.keys():
        print("%s = %s" % (k, cfg.get(k)))

    print("\n-- read secured keys")
    keys = [
        "key2.y", "key3", "key4.b.5", "key5",
    ]
    for k in keys:
        try:
            val = cfg.get_secure(k)
            print("%s = %s" % (k, val))
        except Exception as e:
            err = str(e)
            if not err:
                err = "ciphering failed"
            print("%s = err: %s" % (k, err))

    cfg.purge()
    print("\n-- config purged")

    print("")


main()

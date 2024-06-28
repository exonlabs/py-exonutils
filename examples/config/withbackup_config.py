# -*- coding: utf-8 -*-
import os
import tempfile
from pprint import pprint

from exonutils.xcfg import JsonConfig

CFG_FILE = os.path.join(tempfile.gettempdir(), "sample_config.json")
BAK_FILE = CFG_FILE + ".backup"

DEFAULTS = {
    "key1": "some value",
    "key2": {
        "1": "xxx",
        "2": "yyy",
        "3": "zzz",
    },
}


def main():
    print("\n* using cfg file: %s" % CFG_FILE)

    cfg = JsonConfig(CFG_FILE, defaults=DEFAULTS)
    cfg.enable_backup(BAK_FILE)
    print("\n-- initial config:")
    pprint(cfg)

    print("\n-- saving config")
    cfg.save()

    print("check master config exist: %s" % cfg.is_file_exist())
    print("check backup config exist: %s" % cfg.is_bakfile_exist())

    print("\n")

    print("-- removing master config")
    os.unlink(CFG_FILE)
    print("check master config exist: %s" % cfg.is_file_exist())

    print("")

    print("-- reloading config")
    cfg1 = JsonConfig(CFG_FILE)
    cfg1.enable_backup("")
    cfg1.load()
    pprint(cfg1)

    cfg.purge()
    print("\n-- config purged")

    print("")


main()

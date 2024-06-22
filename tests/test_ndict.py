# -*- coding: utf-8 -*-
import time
from argparse import ArgumentParser
from traceback import format_exc
from utils import valid_msg, fail_msg, red_text, print_data

from exonutils import types


class NDictAlt(dict):
    pass


def TestNDict_Keys() -> bool:
    chk = True

    d = types.NDict(NDictAlt({
        "k1": "some value",
        "k2": {"1": "xxx", "2": "yyy"},
        "k3": NDictAlt({"1": "xxx", "2": "yyy"}),
        "k4": {
            "1": "xxx",
            "2": NDictAlt({"1": "xxx", "2": "yyy"}),
            "3": {
                "1": "xxx",
                "2": {
                    "1": "xxx",
                    "2": {"1": "xxx", "2": "yyy"},
                    "3": [
                        {"1": "xxx",
                            "2": NDictAlt({"1": "xxx", "2": "yyy"}),
                            "3": {
                                "1": "xxx",
                                "2": NDictAlt({"1": "xxx", "2": "yyy"}),
                            }},
                        {"1": "xxx",
                            "2": NDictAlt({"1": "xxx", "2": "yyy"}),
                            "3": {
                                "1": "xxx",
                                "2": NDictAlt({"1": "xxx", "2": "yyy"}),
                            }},
                    ],
                },
                "3": {"1": "xxx", "2": "yyy"},
            },
        },
    }))
    print(">> input: %s" % print_data(d))

    validations = [
        [1, ["k1", "k2", "k3", "k4"]],
        [2, ["k1", "k2.1", "k2.2", "k3", "k4.1", "k4.2", "k4.3"]],
        [3, ["k1", "k2.1", "k2.2", "k3", "k4.1", "k4.2",
             "k4.3.1", "k4.3.2", "k4.3.3"]],
        [4, ["k1", "k2.1", "k2.2", "k3", "k4.1", "k4.2",
             "k4.3.1", "k4.3.2.1", "k4.3.2.2", "k4.3.2.3",
             "k4.3.3.1", "k4.3.3.2"]],
        [5, ["k1", "k2.1", "k2.2", "k3", "k4.1", "k4.2",
             "k4.3.1", "k4.3.2.1", "k4.3.2.2.1", "k4.3.2.2.2",
             "k4.3.2.3", "k4.3.3.1", "k4.3.3.2"]],
        [6, ["k1", "k2.1", "k2.2", "k3", "k4.1", "k4.2",
             "k4.3.1", "k4.3.2.1", "k4.3.2.2.1", "k4.3.2.2.2",
             "k4.3.2.3", "k4.3.3.1", "k4.3.3.2"]],
        [0, ["k1", "k2.1", "k2.2", "k3", "k4.1", "k4.2",
             "k4.3.1", "k4.3.2.1", "k4.3.2.2.1", "k4.3.2.2.2",
             "k4.3.2.3", "k4.3.3.1", "k4.3.3.2"]],
        [-1, ["k1", "k2.1", "k2.2", "k3", "k4.1", "k4.2",
              "k4.3.1", "k4.3.2.1", "k4.3.2.2.1", "k4.3.2.2.2",
              "k4.3.2.3", "k4.3.3.1", "k4.3.3.2"]],
    ]
    for din, dout in validations:
        res = d.keys_n(din)
        print("--- lvl %s = %s" % (din, res))
        if res == dout:
            print(valid_msg())
        else:
            chk = False
            print(red_text("FAILED check for lvl: %s" % din))

    return chk


def TestNDict_KeyExist() -> bool:
    chk = True

    d = types.NDict({
        "k1": "some value",
        "k2": {"1": "xxx", "2": "yyy"},
        "k3": NDictAlt({"1": "xxx", "2": "yyy"}),
        "k4": {
            "1": "xxx",
            "2": NDictAlt({"1": "xxx", "2": "yyy"}),
            "3": {
                "1": "xxx",
                "2": {
                    "1": "xxx",
                    "2": {"1": "xxx", "2": "yyy"},
                },
                "3": {"1": "xxx", "2": "yyy"},
            },
        },
    })
    print(">> input: %s" % print_data(d))

    validations = [
        ["k1", True], ["k1.xx", False],
        ["k2.1", True], ["k2.1.xx", False],
        ["k2.2", True], ["k2.2.xx", False],
        ["k3", True], ["k3.xx", False],
        ["k4.1", True], ["k4.1.xx", False],
        ["k4.2", True], ["k4.2.xx", False],
        ["k4.3.1", True], ["k4.3.1.xx", False],
        ["k4.3.2.1", True], ["k4.3.2.1.xx", False],
        ["k4.3.2.2.1", True], ["k4.3.2.2.1.xx", False],
        ["k4.3.2.2.2", True], ["k4.3.2.2.2.xx", False],
        ["k4.3.3.1", True], ["k4.3.3.1.xx", False],
        ["k4.3.3.2", True], ["k4.3.3.2.xx", False],
    ]
    for din, dout in validations:
        res = d.is_exist(din)
        print("--- %s exist %s" % (din, res))
        if res == dout:
            print(valid_msg())
        else:
            chk = False
            print(red_text("FAILED check for key: %s" % din))

    return chk


def TestNDict_Get():
    chk = True

    d = types.NDict({
        "k1": "some value",
        "k2": {"1": "xxx", "2": "yyy"},
        "k3": NDictAlt({"1": "xxx", "2": "yyy"}),
        "k4": {"1": "xxx", "2": "yyy"},
        "k5": None,
        "k6": [1, 2, 3],
        "k7": {
            "t": [
                {
                    "1": "xxx",
                    "2": NDictAlt({"1": "xxx", "2": "yyy"}),
                    "3": {
                        "1": "xxx",
                        "2": {"1": "xxx", "2": "yyy"},
                    }
                },
                {
                    "1": "xxx",
                    "2": NDictAlt({"1": "xxx", "2": "yyy"}),
                    "3": {
                        "1": "xxx",
                        "2": {"1": "xxx", "2": "yyy"},
                    }
                },
            ],
        },
    })
    print(">> input: %s" % print_data(d))

    validations = [
        ["k1", "some value"], ["k1.xx", None],
        ["k2", types.NDict({"1": "xxx", "2": "yyy"})],
        ["k2.1", "xxx"], ["k2.2", "yyy"], ["k2.xx.yy", None],
        ["k3", NDictAlt({"1": "xxx", "2": "yyy"})],
        ["k3.xx", None], ["k3.yy.zz", None], ["k3.2.3", None],
        ["k4", types.NDict({"1": "xxx", "2": "yyy"})],
        ["k4.1", "xxx"], ["k4.2", "yyy"], ["k4.xx.yy", None],
        ["k5", None], ["k5.xx", None], ["k5.yy.zz", None],
        ["k6", [1, 2, 3]], ["k6.xx", None],
    ]
    for k, v in validations:
        res = d.get(k, None)
        print("--- %s = %s" % (k, res))
        if res == v:
            print(valid_msg())
        else:
            chk = False
            print(red_text("FAILED check for key: %s" % k))

    # sub dicts checks
    for i, v in enumerate(d.get("k7.t", [])):
        k = "k7.t[%s].3.2.1" % i
        res = v.get("3.2.1", None)
        print("--- %s = %s" % (k, res))
        if res == "xxx":
            print(valid_msg())
        else:
            chk = False
            print(red_text("FAILED check for key: %s" % k))

    return chk


def TestNDict_Set() -> bool:
    chk = True

    d = types.NDict(None)
    print(">> input: %s" % print_data(d))

    validations = [
        ["k1", "some value"],
        ["k2", {"1": "xxx", "2": "yyy"}],
        ["k2.3", "333"],
        ["k3", types.NDict({"1": "xxx", "2": "yyy"})],
        ["k3.3", "333"],
        ["k3.3.1.2.1", "111"],
        ["k3.3.1.2.2", "222"],
    ]
    for k, v in validations:
        d.set(k, v)
        print(">> set %s = %s\n--- %s" % (k, v, d))
        res = d.get(k, None)
        if res == v:
            print(valid_msg())
        else:
            chk = False
            print(red_text("FAILED 'Set' check for key: %s" % k))

    return chk


def TestNDict_Delete() -> bool:
    chk = True

    d = types.NDict(NDictAlt({
        "k1": "some value",
        "k2": {"1": "111", "2": True, "3": 333},
        "k3": [1, 2, 3],
        "k4": {
            "a": ["1", 2, False, None],
            "b": {
                "1": 111, "2": "222", "3": None,
                "4": NDictAlt({"x": "xxx", "y": None, "z": "zzz"}),
                "5": {"x": "xxx", "y": None, "z": "zzz"},
            },
        },
    }))
    print(">> input: %s" % print_data(d))

    validations = [
        "k3.2.xxx", "k4.b.3", "k4.b.4",
    ]
    for k in validations:
        d.delete(k)
        print(">> Del %s\n--- %s" % (k, d))
        res = d.get(k, None)
        if res is None:
            print(valid_msg())
        else:
            chk = False
            print(red_text("FAILED 'Del' check for key: %s" % k))

    return chk


def TestNDict_Update() -> bool:
    chk = True

    d = types.NDict(NDictAlt({
        "k1": "some value",
        "k2": {"1": "111", "2": True, "3": 333},
        "k3": [1, 2, 3],
        "k4": {
            "a": ["1", 2, False, None],
            "b": {
                "1": 111, "2": "222", "3": None,
                "4": NDictAlt({"x": "xxx", "y": None, "z": "zzz"}),
                "5": {"x": "xxx", "y": None, "z": "zzz"},
            },
        },
    }))
    print(">> input: %s" % print_data(d))

    updt = {
        "k3": {"1": "111", "2": 222},
        "k4": {
            "b": {"5": 555, "6": 666},
            "c": "ccc",
        },
        "3": 333,
    }
    print(">> update: %s" % print_data(updt))

    validation = types.NDict({
        "k1": "some value",
        "k2": types.NDict({"1": "111", "2": True, "3": 333}),
        "k3": types.NDict({"1": "111", "2": 222}),
        "k4": types.NDict({
            "a": ["1", 2, False, None],
            "b": types.NDict({
                "1": 111, "2": "222", "3": None,
                "4": NDictAlt({"x": "xxx", "y": None, "z": "zzz"}),
                "5": 555, "6": 666}),
            "c": "ccc",
        }),
        "3": 333,
    })

    d.update(updt)
    if d == validation:
        print(" --- result: %s\n" % print_data(d) + valid_msg())
    else:
        chk = False
        print(red_text("FAILED 'Updt' check") +
              (" --- got: %s" % print_data(d)))

    return chk


def TestNDict_Reset() -> bool:
    chk = True

    d = types.NDict(NDictAlt({
        "k1": "some value",
        "k2": {"1": "111", "2": True, "3": 333},
        "k3": [1, 2, 3],
        "k4": {
            "a": ["1", 2, False, None],
            "b": {
                "1": 111, "2": "222", "3": None,
                "4": NDictAlt({"x": "xxx", "y": None, "z": "zzz"}),
                "5": {"x": "xxx", "y": None, "z": "zzz"},
            },
        },
    }))
    print(">> input: %s" % print_data(d))

    validation = types.NDict({})

    d.reset()
    if d == validation:
        print(" --- result: %s\n" % print_data(d) + valid_msg())
    else:
        chk = False
        print(red_text("FAILED 'Updt' check") +
              (" --- got: %s" % print_data(d)))

    return chk


def main():
    tests = [
        TestNDict_Keys,
        TestNDict_KeyExist,
        TestNDict_Get,
        TestNDict_Set,
        TestNDict_Delete,
        TestNDict_Update,
        TestNDict_Reset,
    ]

    pr = ArgumentParser(prog=None)
    pr.add_argument(
        "--run", dest="test_case", metavar="TEST_CASE_NAME",
        help="select test case to run")
    args = pr.parse_args()

    if args.test_case:
        for t in tests:
            if t.__name__ == args.test_case:
                tests = [t]
                break
        else:
            print("\nwarning: no tests to run\nPASS\n")
            return

    for t in tests:
        print("\n=== RUN   %s" % t.__name__)
        chk = "FAIL"
        ts = time.time()
        try:
            if t():
                chk = "PASS"
        except Exception:
            print(format_exc().strip() + "\n" + fail_msg())
        ts = (time.time() - ts) * 1000
        print("--- %s: %s (%.3f ms)" % (chk, t.__name__, ts))
        print(chk)

    print()


main()

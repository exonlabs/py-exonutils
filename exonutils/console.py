# -*- coding: utf-8 -*-
"""
    :copyright: 2020, ExonLabs. All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
import re
from builtins import input
from getpass import getpass


class ConsoleInput(object):

    input_caret = '>>'

    @classmethod
    def _msg(cls, msg):
        # print BOLD text message
        return "\033[1m%s %s \033[0m" % (cls.input_caret, msg)

    @classmethod
    def _err(cls, msg):
        # print RED color error message
        return "\033[31m -- %s\033[0m" % msg

    @classmethod
    def _input(cls, msg, hidden=False):
        fin = getpass if hidden else input
        return fin(cls._msg(msg)).strip()

    @classmethod
    def get(cls, msg, default=None, trials=3, hidden=False, regex=None,
            validator_callback=None):
        if default is None:
            msg = "%s:" % msg
        else:
            default = str(default)
            msg = "%s: [%s]" % (msg, default)

        for i in range(max(1, trials)):
            res = cls._input(msg, hidden=hidden)
            if res:
                if validator_callback and not validator_callback(res):
                    continue
                if regex and not re.search(regex, res):
                    print(cls._err("invalid input format"))
                    continue
                return res
            else:
                if default is not None:
                    return default
                print(cls._err("empty input, please enter value"))

        raise ValueError("failed to get valid input")

    @classmethod
    def confirm(cls, msg, value, trials=3, hidden=False):
        for i in range(max(1, trials)):
            res = cls._input("%s:" % msg, hidden=hidden)
            try:
                if (type(value) is int and int(res) == value) or \
                   (type(value) is float and float(res) == value) or \
                   (type(value) is bool and bool(res) == value) or \
                   res == value:
                    return True
            except Exception:
                pass
            print(cls._err("not matching value, please try again"))

        raise ValueError("failed to confirm input value")

    @classmethod
    def number(cls, msg, default=None, trials=3, vmin=None, vmax=None):
        def validator(res):
            if not re.search('^[0-9-]+$', res):
                print(cls._err("invalid number format"))
                return False

            num = int(res)
            if (vmin is not None and num < int(vmin)) or \
               (vmax is not None and num > int(vmax)):
                print(cls._err("value out of range, %s <= n <= %s"
                      % (vmin, vmax)))
                return False

            return True

        res = cls.get(msg, default=default, trials=trials,
                      validator_callback=validator)
        return int(res) if res else default

    @classmethod
    def decimal(cls, msg, default=None, trials=3, vmin=None, vmax=None):
        def validator(res):
            if not re.search('^[0-9-]+(.[0-9]+)?$', res):
                print(cls._err("invalid decimal format"))
                return False

            num = float(res)
            if (vmin is not None and num < float(vmin)) or \
               (vmax is not None and num > float(vmax)):
                print(cls._err("value out of range, %s <= n <= %s"
                      % (vmin, vmax)))
                return False

            return True

        res = cls.get(msg, default=default, trials=trials,
                      validator_callback=validator)
        return float(res) if res else default

    @classmethod
    def select(cls, msg, values, default=None, trials=3, case_sensitive=False):
        if case_sensitive:
            values = [str(s) for s in values]
            if default is not None:
                default = str(default)
        else:
            values = [str(s).lower() for s in values]
            if default is not None:
                default = str(default).lower()

        if default in values:
            msg = "%s [%s]: [%s]" % (msg, '|'.join(values), default)
        else:
            msg = "%s [%s]:" % (msg, '|'.join(values))

        for i in range(max(1, trials)):
            res = cls._input(msg)
            if res:
                if not case_sensitive:
                    res = res.lower()
                if res in values:
                    return res
                print(cls._err("invalid value"))
            else:
                if default is not None:
                    return default
                print(cls._err("empty input, please select value"))

        raise ValueError("failed to get valid input")

    @classmethod
    def yesno(cls, msg, default=None, trials=3):
        res = cls.select(
            msg, values=['y', 'n'], default=default, trials=trials)
        return bool(res == 'y')

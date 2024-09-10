# -*- coding: utf-8 -*-
import re
from getpass import getpass
try:
    import readline
    readline.set_completer_delims(' \t\n;')
    readline.parse_and_bind("tab: complete")
except Exception:
    pass
try:
    import colorama
    colorama.init()
except ImportError:
    colorama = None

__all__ = []


class Console(object):

    prompt_caret = '>>'

    @classmethod
    def _get_input(cls, msg, default='', hidden=False):
        if colorama:
            # print BOLD/BRIGHT text message
            prompt = "%s%s %s %s" % (
                colorama.Style.BRIGHT,
                cls.prompt_caret,
                msg,
                colorama.Style.RESET_ALL)
        else:
            prompt = "%s %s " % (cls.prompt_caret, msg)

        result = (getpass(prompt) if hidden else input(prompt)).strip()
        return result if result else default

    @classmethod
    def _print_err(cls, msg):
        if colorama:
            # print RED color error message
            print("%s -- %s%s" % (
                colorama.Fore.RED + colorama.Style.BRIGHT,
                msg,
                colorama.Style.RESET_ALL))
        else:
            print(" -- %s" % msg)

    @classmethod
    def _validator(cls, input_str, regex=None):
        if regex and not re.search(regex, input_str):
            return "invalid input format"
        return True

    def get_value(self, msg, default=None, required=False, trials=3,
                  hidden=False, regex=None, validator=None):
        str_default = '' if default is None else str(default).strip()

        msg = "%s:" % msg
        if not required or str_default:
            msg += " [%s]" % str_default

        if not validator:
            validator = self._validator

        for i in range(max(1, trials)):
            input_str = self._get_input(
                msg, default=str_default, hidden=hidden)
            if input_str:
                chk = validator(input_str, regex=regex)
                if chk is True:
                    return input_str
                self._print_err(chk)
            elif not required:
                return None if default is None else str_default
            else:
                self._print_err("required input, please enter value")

        raise ValueError("failed to get valid input")

    def get_password(self, *args, **kwargs):
        kwargs.update({'hidden': True})
        return self.get_value(*args, **kwargs)

    def confirm_password(self, msg, value, trials=3):
        for i in range(max(1, trials)):
            res = self._get_input("%s:" % msg, hidden=True)
            if res:
                if res == str(value):
                    return True
                self._print_err("value not matching, please try again")
            else:
                self._print_err("empty input, please confirm value")

        raise ValueError("failed to confirm value")

    def get_number(self, msg, default=None, required=False, trials=3,
                   vmin=None, vmax=None):
        def validator(input_str, regex=None):
            if not re.search('^[0-9-]+$', input_str):
                return "invalid number format"
            num = int(input_str)
            if (vmin is not None and (int(vmin) - num) > 0) or \
               (vmax is not None and (int(vmax) - num) < 0):
                return "value out of range"
            return True

        res = self.get_value(
            msg, default=default, required=required, trials=trials,
            validator=validator)
        return int(res) if res is not None else None

    def get_decimal(self, msg, default=None, required=False, trials=3,
                    vmin=None, vmax=None):
        def validator(input_str, regex=None):
            if not re.search('^[0-9-]+(.[0-9]+)?$', input_str):
                return "invalid decimal format"
            num = float(input_str)
            if (vmin is not None and (float(vmin) - num) > 0) or \
               (vmax is not None and (float(vmax) - num) < 0):
                return "value out of range"
            return True

        res = self.get_value(
            msg, default=default, required=required, trials=trials,
            validator=validator)
        return float(res) if res is not None else None

    def select_value(self, msg, values, default=None, required=False,
                     trials=3, case_sensitive=False):
        if case_sensitive:
            values = [str(s) for s in values]
            if default is not None:
                default = str(default)
        else:
            values = [str(s).lower() for s in values]
            if default is not None:
                default = str(default).lower()

        msg = "%s {%s}" % (msg, '|'.join(values))
        if default not in values:
            default = None

        def validator(input_str, regex=None):
            if not case_sensitive:
                input_str = input_str.lower()
            if input_str not in values:
                return "invalid value, please select from list"
            return True

        return self.get_value(
            msg, default=default, required=required, trials=trials,
            validator=validator)

    def select_yesno(self, msg, default=None, required=False, trials=3):
        res = self.select_value(
            msg, ['y', 'n'], default=default, required=required,
            trials=trials, case_sensitive=False)
        return bool(res == 'y')

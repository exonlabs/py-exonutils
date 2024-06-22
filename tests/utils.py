# -*- coding: utf-8 -*-


def green_text(msg: str) -> str:
    return "\033[0;32m%s\033[0m" % msg


def red_text(msg: str) -> str:
    return "\033[0;31m%s\033[0m" % msg


def valid_msg() -> str:
    return green_text("VALID")


def fail_msg() -> str:
    return red_text("FAILED")


# Reverse the elements of the list and return a copy
def rev_copy(src: list) -> list:
    from copy import deepcopy
    dst = deepcopy(src)
    return dst.reverse()


def print_data(d) -> str:
    return "\n%s\n-----------------------------------------------" % str(d)

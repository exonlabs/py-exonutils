# -*- coding: utf-8 -*-
from datetime import datetime

from .common import Level

__all__ = []


class Formatter(object):

    record_format: str = ""
    time_format: str = ""
    escape_msg: bool = False

    def __init__(self, recfmt: str, tsfmt: str, escmsg: bool = False):
        self.record_format = recfmt
        self.time_format = tsfmt
        self.escape_msg = escmsg

    # generate new formatted log record
    def emit(self, lvl: Level, src: str, msg: str, *args) -> str:
        now = datetime.now()

        if self.time_format:
            t = now.strftime("%Y-%m-%d %H:%M:%S.%f")
        else:
            t = now.strftime(self.time_format)

        m = str(msg) % args
        if self.escape_msg:
            m = m.replace('\\', '\\\\').replace('"', '\\"')

        return (
            self.record_format
            .replace("{time}", t)
            .replace("{level}", str(lvl))
            .replace("{source}", str(src))
            .replace("{message}", m)
        )


# standard text formatted log record
def StdFormatter() -> Formatter:
    return Formatter(
        "{time} {level} [{source}] {message}",
        "%Y-%m-%d %H:%M:%S.%f",
    )


# simple text formatted log record, without source
def SimpleFormatter() -> Formatter:
    return Formatter(
        "{time} {level} {message}",
        "%Y-%m-%d %H:%M:%S.%f",
    )


# basic text formatted log record, just timestamp and message
def BasicFormatter() -> Formatter:
    return Formatter(
        "{time} {message}",
        "%Y-%m-%d %H:%M:%S.%f",
    )


# raw text formatted log record, just the message
def RawFormatter() -> Formatter:
    return Formatter(
        "{message}",
        "",
    )


# customized message text formatter
def CustomMsgFormatter(recfmt: str) -> Formatter:
    return Formatter(
        recfmt,
        "%Y-%m-%d %H:%M:%S.%f",
    )


# customized timestamp text formatter
def CustomTimeFormatter(tsfmt: str) -> Formatter:
    return Formatter(
        "{time} {level} {message}",
        tsfmt,
    )


# standard json formatted log record
def JsonFormatter() -> Formatter:
    return Formatter(
        "{%s}" % ",".join(
            [
                '"ts":"{time}"',
                '"lvl":"{level}"',
                '"src":"{source}"',
                '"msg":"{message}"',
            ]
        ),
        "%Y-%m-%d %H:%M:%S.%f",
        escmsg=True,
    )

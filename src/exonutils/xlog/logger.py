# -*- coding: utf-8 -*-
from typing import TypeVar

from .common import (
    Level,
    TRACE4,
    TRACE3,
    TRACE2,
    TRACE1,
    DEBUG,
    INFO,
    WARN,
    ERROR,
    FATAL,
    PANIC,
)
from .formatter import Formatter, StdFormatter
from .handlers import Handler

__all__ = []

Logger = TypeVar("Logger")


class Logger(object):

    name: str = ""
    level: Level = INFO
    _parent: Logger = None
    _formatter: Formatter = None
    _handlers: list[Handler] = None

    def __init__(self, name: str):
        self.name = name
        self.level = INFO
        self._formatter = StdFormatter()

    def child_logger(self, name: str) -> Logger:
        log = Logger(name)
        log._parent = self
        log.level = self.level
        log._formatter = self._formatter
        return log

    def sub_logger(self, prefix: str) -> Logger:
        log = Logger(self.name)
        log._parent = self
        log.level = self.level
        log._formatter = Formatter(
            self._formatter.record_format,
            self._formatter.time_format,
            self._formatter.escape_msg)
        log._formatter.msg_prefix = prefix
        return log

    def set_formatter(self, frmt: Formatter):
        if frmt and isinstance(frmt, Formatter):
            self._formatter = frmt

    def add_handler(self, hnd: Handler):
        if hnd and isinstance(hnd, Handler):
            if not self._handlers:
                self._handlers = [hnd]
            else:
                self._handlers.append(hnd)

    def clear_handlers(self):
        self._handlers = None

    def _log(self, r: str):
        # handle record with loaded handlers
        if self._handlers:
            for h in self._handlers:
                h.handle_record(r)
        # propagate to parent logger
        if self._parent:
            self._parent._log(r)

    def panic(self, msg: str, *args):
        if self.level <= PANIC:
            self._log(self._formatter.emit(PANIC, self.name, msg, *args))

    def fatal(self, msg: str, *args):
        if self.level <= FATAL:
            self._log(self._formatter.emit(FATAL, self.name, msg, *args))

    def error(self, msg: str, *args):
        if self.level <= ERROR:
            self._log(self._formatter.emit(ERROR, self.name, msg, *args))

    def warn(self, msg: str, *args):
        if self.level <= WARN:
            self._log(self._formatter.emit(WARN, self.name, msg, *args))

    def info(self, msg: str, *args):
        if self.level <= INFO:
            self._log(self._formatter.emit(INFO, self.name, msg, *args))

    def debug(self, msg: str, *args):
        if self.level <= DEBUG:
            self._log(self._formatter.emit(DEBUG, self.name, msg, *args))

    def trace1(self, msg: str, *args):
        if self.level <= TRACE1:
            self._log(self._formatter.emit(TRACE1, self.name, msg, *args))

    def trace2(self, msg: str, *args):
        if self.level <= TRACE2:
            self._log(self._formatter.emit(TRACE2, self.name, msg, *args))

    def trace3(self, msg: str, *args):
        if self.level <= TRACE3:
            self._log(self._formatter.emit(TRACE3, self.name, msg, *args))

    def trace4(self, msg: str, *args):
        if self.level <= TRACE4:
            self._log(self._formatter.emit(TRACE4, self.name, msg, *args))


# ///////////////////// creator functions

def StdoutLogger(name: str) -> Logger:
    from .handlers import StdoutHandler
    log = Logger(name)
    log._handlers = [StdoutHandler()]
    return log


def FileLogger(name: str, path: str) -> Logger:
    from .handlers import FileHandler
    log = Logger(name)
    log._handlers = [FileHandler(path)]
    return log

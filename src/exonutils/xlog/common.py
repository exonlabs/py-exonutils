# -*- coding: utf-8 -*-

__all__ = []


class Level(int):

    # returns string of log level
    def __str__(self) -> str:
        if self >= PANIC:
            return "PANIC"
        if self >= FATAL:
            return "FATAL"
        if self >= ERROR:
            return "ERROR"
        if self >= WARN:
            return "WARN "
        if self >= INFO:
            return "INFO "
        if self >= DEBUG:
            return "DEBUG"
        if self >= TRACE1:
            return "TRACE1"
        if self >= TRACE2:
            return "TRACE2"
        if self >= TRACE3:
            return "TRACE3"
        if self >= TRACE4:
            return "TRACE4"
        return "TRACE"


# logging levels
TRACE4 = Level(-50)
TRACE3 = Level(-40)
TRACE2 = Level(-30)
TRACE1 = Level(-20)
DEBUG = Level(-10)
INFO = Level(0)
WARN = Level(10)
ERROR = Level(20)
FATAL = Level(30)
PANIC = Level(40)

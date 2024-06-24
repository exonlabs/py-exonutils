# -*- coding: utf-8 -*-
import os
from tempfile import gettempdir

from exonutils import xlog

log_file = os.path.join(gettempdir(), "foobar.log")


def log_messages(logger: xlog.Logger):
    logger.panic("logging message type: %s", "panic")
    logger.fatal("logging message type: %s", "fatal")
    logger.error("logging message type: %s", "error")
    logger.warn("logging message type: %s", "warn")
    logger.info("logging message type: %s", "info")
    logger.debug("logging message type: %s", "debug")
    logger.trace1("logging message type: %s", "trace1")
    logger.trace2("logging message type: %s", "trace2")
    logger.trace3("logging message type: %s", "trace3")
    logger.trace4("logging message type: %s", "trace4")


def main():
    logger = xlog.Logger("main")
    logger.level = xlog.DEBUG

    hnd1 = xlog.StdoutHandler()
    logger.add_handler(hnd1)

    hnd2 = xlog.FileHandler(log_file)
    logger.add_handler(hnd2)

    print("\n* logging stdout and file:", hnd2.filepath)
    log_messages(logger)

    print("\n-- output log file: %s\n" % log_file)
    print()


main()

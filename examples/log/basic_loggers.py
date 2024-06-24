# -*- coding: utf-8 -*-
from exonutils import xlog


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
    logger = xlog.StdoutLogger("main")

    print("\n* logging level: TRACE2")
    logger.level = xlog.TRACE2
    log_messages(logger)

    print("\n* logging level: DEBUG")
    logger.level = xlog.DEBUG
    log_messages(logger)

    # adjust formatters
    print("\n-- logging without source formatter --")
    logger.set_formatter(xlog.SimpleFormatter())

    print("\n* logging level: ERROR")
    logger.level = xlog.ERROR
    log_messages(logger)

    print("\n* logging level: FATAL")
    logger.level = xlog.FATAL
    log_messages(logger)

    print("\n* logging level: PANIC")
    logger.level = xlog.PANIC
    log_messages(logger)

    # adjust formatters
    print("\n-- logging json formatter --")
    logger.set_formatter(xlog.JsonFormatter())
    logger.level = xlog.TRACE4
    log_messages(logger)

    print()


main()

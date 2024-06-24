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


formatter1 = xlog.Formatter(
    "{time} {level} -- {message}",
    "%Y-%m-%d %H:%M:%S",
)
formatter2 = xlog.Formatter(
    "{time} -- [{level}] -- {message}",
    "%Y-%m-%d %H:%M:%S",
)
formatter3 = xlog.Formatter(
    '{"time":"{time}", "level":"{level}", "message":"{message}"}',
    "%Y-%m-%d %H:%M:%S",
    escmsg=True,
)


def main():
    logger = xlog.StdoutLogger("main")
    logger.level = xlog.DEBUG

    print("\n* with default formatter:")
    log_messages(logger)

    print("\n* with custom formatter1:")
    logger.set_formatter(formatter1)
    log_messages(logger)

    print("\n* with custom formatter2:")
    logger.set_formatter(formatter2)
    log_messages(logger)

    print("\n* with custom json formatter:")
    logger.set_formatter(formatter3)
    log_messages(logger)

    print()


main()

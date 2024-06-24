# -*- coding: utf-8 -*-
from exonutils import xlog


def main():
    logger = xlog.StdoutLogger("main")
    logger.level = xlog.DEBUG
    logger.set_formatter(xlog.CustomMsgFormatter(
        "{time} {level} [{source}] -- root handler, {message}"))

    print("\n* logging parent logger:", logger.name)
    logger.warn("logging root message type: %s", "warn")
    logger.info("logging root message type: %s", "info")

    log1 = logger.child_logger("child1")
    print("\n* logging child  logger:", log1.name)
    logger.warn("logging root message type: %s", "warn")
    log1.warn("logging child 1 message type: %s", "warn")
    logger.info("logging root message type: %s", "info")
    log1.info("logging child 1 message type: %s", "info")

    log2 = logger.child_logger("child2")
    log2.level = xlog.WARN
    log2.set_formatter(xlog.CustomMsgFormatter(
        "{time} {level} ----- child2 handler, {message}"))
    print("\n* logging child 2 logger (+handlers):", log2.name)
    logger.warn("logging root message type: %s", "warn")
    log1.warn("logging child 1 message type: %s", "warn")
    log2.warn("logging child 2 message type: %s", "warn")
    logger.info("logging root message type: %s", "info")
    log1.info("logging child 1 message type: %s", "info")
    log2.info("logging child 2 message type: %s", "info")

    print()


main()

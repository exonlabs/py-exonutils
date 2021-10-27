# -*- coding: utf-8 -*-
import sys
import logging
from argparse import ArgumentParser
from traceback import format_exc

from exonutils.daemon import BaseDaemon

logging.basicConfig(
    level=logging.INFO, stream=sys.stdout,
    format='%(asctime)s %(levelname)-5.5s [%(name)s] %(message)s')
logging.addLevelName(logging.WARNING, "WARN")
logging.addLevelName(logging.CRITICAL, "FATAL")


class SampleDaemon(BaseDaemon):

    def initialize(self):
        self.log.info("Initializing")
        self.counter = 0

    def execute(self):
        self.counter += 1
        self.log.debug("Running: %s ..." % self.counter)
        if self.counter >= 50:
            self.log.info("exit process after count = %s" % self.counter)
            self.stop()
        self.sleep(2)

    def terminate(self):
        self.log.info("Shutting down")

        self.term_event.clear()
        self.log.info("exit after 5 counts")
        for i in range(5):
            self.log.info('count %s' % (i + 1))
            self.sleep(1)

    def handle_sigusr1(self):
        if self.log.level != logging.DEBUG:
            self.log.setLevel(logging.DEBUG)
            self.log.info("debugging ON")
        else:
            self.log.setLevel(logging.INFO)
            self.log.info("debugging OFF")

    def handle_sigusr2(self):
        self.counter = 0
        self.log.info("Counter reset")


if __name__ == '__main__':
    logger = logging.getLogger()
    logger.name = 'main'
    try:
        pr = ArgumentParser(prog=None)
        pr.add_argument(
            '-x', dest='debug', action='count', default=0,
            help='set debug modes')
        args = pr.parse_args()

        if args.debug > 0:
            logger.setLevel(logging.DEBUG)

        p = SampleDaemon(logger=logger, debug=args.debug)
        p.start()

    except Exception:
        logger.fatal(format_exc().strip())
        sys.exit(1)

# -*- coding: utf-8 -*-
import sys
import logging
from argparse import ArgumentParser

from exonutils.process.daemon import BaseDaemon

logging.basicConfig(
    level=logging.INFO, stream=sys.stdout,
    format='%(asctime)s %(levelname)-5.5s [%(name)s] %(message)s')
logging.addLevelName(logging.WARNING, "WARN")
logging.addLevelName(logging.CRITICAL, "FATAL")


class SampleDaemon(BaseDaemon):

    def initialize(self):
        self.counter = 0
        self.sleep(1)

    def execute(self):
        self.counter += 1

        self.log.debug("running: %s ..." % self.counter)
        if self.counter >= 60:
            self.log.info("exit process count = %s" % self.counter)
            self.stop()

        self.sleep(1)

    def terminate(self):
        exit_counts = 2
        self.log.info("exit after %s counts" % exit_counts)
        for i in range(exit_counts):
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
        self.log.info("counter reset")


def main():
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

        logger.info("**** starting ****")

        srv = SampleDaemon('SampleDaemon', logger=logger)
        srv.start()

    except Exception as e:
        logger.fatal(str(e), exc_info=args.debug)
        sys.exit(1)


if __name__ == '__main__':
    main()

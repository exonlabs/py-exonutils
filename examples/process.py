# -*- coding: utf-8 -*-
import sys
import logging
from time import sleep
from argparse import ArgumentParser
from traceback import format_exc

from exonutils.process import BaseProcess

logging.basicConfig(
    level=logging.INFO, stream=sys.stdout,
    format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger()


class SampleProcess(BaseProcess):

    def initialize(self):
        log.info("Initializing")
        self.counter = 0

    def execute(self):
        log.debug("Running: %s ..." % self.counter)
        self.counter += 1
        sleep(2)

    def terminate(self):
        log.info("Shutting down")

    def handle_sigusr1(self):
        rootlogger = logging.getLogger()
        if rootlogger.level != logging.DEBUG:
            rootlogger.setLevel(logging.DEBUG)
            log.info("debugging ON")
        else:
            rootlogger.setLevel(logging.INFO)
            log.info("debugging OFF")

    def handle_sigusr2(self):
        self.counter = 0
        log.info("Counter reset")


if __name__ == '__main__':
    try:
        pr = ArgumentParser(prog=None)
        pr.add_argument('-x', dest='debug', action='store_true',
                        help='enable debug mode')
        args = pr.parse_args()

        if args.debug:
            logging.getLogger().setLevel(logging.DEBUG)

        p = SampleProcess('SampleProcess')
        p.start()

    except Exception:
        log.fatal(format_exc())
        sys.exit(1)

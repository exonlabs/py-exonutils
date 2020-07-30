# -*- coding: utf-8 -*-
import sys
import logging
from argparse import ArgumentParser
from traceback import format_exc

from exonutils.service import BaseService, BaseServiceTask

logging.basicConfig(
    level=logging.INFO, stream=sys.stdout,
    format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger()

counter = 0


class Task1(BaseServiceTask):

    def initialize(self):
        log.info("initializing task")

    def execute(self):
        global counter
        log.debug("running ...")
        counter += 1
        self.sleep(5)

    def terminate(self):
        log.info("terminating task")


class Task2(BaseServiceTask):

    def initialize(self):
        log.info("initializing task")

    def execute(self):
        global counter
        log.debug("running ...")
        log.info("count = %s" % counter)
        self.sleep(3)

    def terminate(self):
        log.info("terminating task")


if __name__ == '__main__':
    try:
        pr = ArgumentParser(prog=None)
        pr.add_argument('-x', dest='debug', action='store_true',
                        help='enable debug mode')
        args = pr.parse_args()

        if args.debug:
            logging.getLogger().setLevel(logging.DEBUG)

        s = BaseService('SampleService')
        s.tasks = [Task1, Task2]
        s.start()

    except Exception:
        log.fatal(format_exc())
        sys.exit(1)

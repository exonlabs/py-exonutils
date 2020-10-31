# -*- coding: utf-8 -*-
import sys
import logging
from argparse import ArgumentParser
from traceback import format_exc

from exonutils.service import BaseService, BaseServiceTask

logging.basicConfig(
    level=logging.INFO, stream=sys.stdout,
    format='%(asctime)s %(levelname)-5.5s [%(name)s] %(message)s')
logging.addLevelName(logging.WARNING, "WARN")
logging.addLevelName(logging.CRITICAL, "FATAL")

counter = 0


class Task1(BaseServiceTask):

    def initialize(self):
        self.log.info("initializing")
        self.term_count = None

    def execute(self):
        global counter
        self.log.debug("running ...")
        counter += 1
        self.log.info("new count = %s" % counter)
        self.sleep(2)

    def terminate(self):
        self.log.info("terminating")

    def term_signal(self):
        global counter
        if self.term_count is None:
            self.term_count = counter + 3
            self.log.info(
                "TERM_EVENT: waiting till count = %s" % self.term_count)
        elif counter >= self.term_count:
            self.term_event.set()


class Task2(BaseServiceTask):

    def initialize(self):
        self.log.info("initializing")

    def execute(self):
        global counter
        self.log.debug("running ...")
        self.log.info("count = %s" % counter)
        if counter == 5:
            raise RuntimeError("Killing myself for test at count=5 ;)")
        self.sleep(1)

    def terminate(self):
        self.log.info("terminating")


if __name__ == '__main__':
    log = logging.getLogger()
    log.name = 'main'
    try:
        pr = ArgumentParser(prog=None)
        pr.add_argument(
            '-x', dest='debug', action='count', default=0,
            help='set debug modes')
        args = pr.parse_args()

        if args.debug > 0:
            log.setLevel(logging.DEBUG)

        srv = BaseService('SampleService', logger=log, debug=args.debug)
        srv.tasks = [Task1, Task2]

        srv.start()

    except Exception:
        log.fatal(format_exc())
        sys.exit(1)

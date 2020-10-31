# -*- coding: utf-8 -*-
import sys
import logging
from argparse import ArgumentParser
from traceback import format_exc

from exonutils.service import BaseService, BaseServiceTask

logging.basicConfig(
    level=logging.INFO, stream=sys.stdout,
    format='%(asctime)s [%(name)s] %(levelname)s %(message)s')

counter = 0


class Task1(BaseServiceTask):

    def initialize(self):
        self.log.info("initializing <%s>" % self.__class__.__name__)
        self.term_count = None

    def execute(self):
        global counter
        self.log.debug("running ...")
        counter += 1
        self.log.info("new count = %s" % counter)
        self.sleep(2)

    def terminate(self):
        self.log.info("terminating <%s>" % self.__class__.__name__)

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
        self.log.info("initializing <%s>" % self.__class__.__name__)

    def execute(self):
        global counter
        self.log.debug("running ...")
        self.log.info("count = %s" % counter)
        if counter == 5:
            raise RuntimeError("Killing myself for test at count=5 ;)")
        self.sleep(1)

    def terminate(self):
        self.log.info("terminating <%s>" % self.__class__.__name__)


if __name__ == '__main__':
    log = logging.getLogger()
    log.name = 'SampleService'
    try:
        pr = ArgumentParser(prog=None)
        pr.add_argument('-x', dest='debug', action='store_true',
                        help='enable debug mode')
        args = pr.parse_args()

        if args.debug:
            log.setLevel(logging.DEBUG)

        s = BaseService('SampleService', logger=log)
        s.tasks = [Task1, Task2]
        s.start()

    except Exception:
        log.fatal(format_exc())
        sys.exit(1)

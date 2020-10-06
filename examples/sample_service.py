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

    def execute(self):
        global counter
        self.log.debug("running ...")
        counter += 1
        self.sleep(5)

    def terminate(self):
        self.log.info("terminating <%s>" % self.__class__.__name__)


class Task2(BaseServiceTask):

    def initialize(self):
        self.log.info("initializing <%s>" % self.__class__.__name__)

    def execute(self):
        global counter
        self.log.debug("running ...")
        self.log.info("count = %s" % counter)
        self.sleep(3)

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

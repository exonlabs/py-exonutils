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
        counter += 1
        self.log.info("new count = %s" % counter)

        if counter == 5:
            self.log.info(
                "suspend <%s> at count: %s" % (Task2.__name__, counter))
            self.service.stop_task(Task2.__name__, suspend=True)
        elif counter == 10:
            self.log.info(
                "resume <%s> at count: %s" % (Task2.__name__, counter))
            self.service.start_task(Task2.__name__)

        self.sleep(2)

    def terminate(self):
        global counter

        term_count = counter + 3
        self.log.info("TERM_EVENT: wait till count = %s" % term_count)
        while counter < term_count:
            self.execute()

        self.log.info("terminating")


class Task2(BaseServiceTask):

    def initialize(self):
        self.log.info("initializing")

    def execute(self):
        global counter
        self.log.info("monitoring count = %s" % counter)

        if counter == 15:
            self.log.info("stopping myself at count = %s" % counter)
            self.stop()

        if counter >= 20:
            self.log.info("stopping service at count = %s" % counter)
            self.service.stop()

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

        srv = BaseService(logger=log, debug=args.debug)
        srv.tasks = [Task1, Task2]
        srv.start()

    except Exception:
        log.fatal(format_exc())
        sys.exit(1)

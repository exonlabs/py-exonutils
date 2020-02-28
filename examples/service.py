# -*- coding: utf-8 -*-
import sys
import logging
from argparse import ArgumentParser
from traceback import format_exc

from exonutils.service import Service, ServiceTask

logging.basicConfig(
    level=logging.INFO, stream=sys.stdout,
    format='%(asctime)s [%(name)s] %(levelname)s %(message)s')


class Task1(ServiceTask):

    def initialize(self):
        self.log.info("initializing task")

    def execute(self):
        self.log.debug("running ...")
        self.sleep(5)

    def terminate(self):
        self.log.info("terminating task")


class Task2(ServiceTask):

    def initialize(self):
        self.log.info("initializing task")

    def execute(self):
        self.log.debug("running ...")
        self.sleep(3)

    def terminate(self):
        self.log.info("terminating task")


if __name__ == '__main__':
    try:
        pr = ArgumentParser(prog=None)
        pr.add_argument('-x', dest='debug', action='store_true',
                        help='enable debug mode')
        args = pr.parse_args()

        if args.debug:
            logging.getLogger().setLevel(logging.DEBUG)

        s = Service('SampleService')
        s.tasks = [Task1, Task2]
        s.start()

    except Exception:
        print(format_exc())
        sys.exit(1)

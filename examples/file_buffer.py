# -*- coding: utf-8 -*-
import sys
import logging
from argparse import ArgumentParser
from traceback import format_exc

from exonutils.service import BaseService, BaseServiceTask
from exonutils.buffers import SharedFileBuffer

logging.basicConfig(
    level=logging.INFO, stream=sys.stdout,
    format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger()


class Task1(BaseServiceTask):

    def initialize(self):
        log.info("initializing task")
        self.buff = SharedFileBuffer('SampleBuffer')

    def execute(self):
        global counter
        counter = self.buff.get('counter')
        try:
            if counter is None:
                self.buff.set('counter', 0)
            else:
                self.buff.set('counter', counter + 1)
        except:
            pass
        self.sleep(1)

    def terminate(self):
        log.info("terminating task")
        self.buff.purge()


class Task2(BaseServiceTask):

    def initialize(self):
        log.info("initializing task")
        self.buff = SharedFileBuffer('SampleBuffer')

    def execute(self):
        global counter
        log.info("counter = %s" % self.buff.get('counter'))
        self.sleep(1)

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

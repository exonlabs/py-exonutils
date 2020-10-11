# -*- coding: utf-8 -*-
import sys
import logging
from argparse import ArgumentParser
from traceback import format_exc

from exonutils.service import BaseService, BaseServiceTask
from exonutils.buffers import FileBuffer

logging.basicConfig(
    level=logging.INFO, stream=sys.stdout,
    format='%(asctime)s [%(name)s] %(levelname)s %(message)s')


class Task1(BaseServiceTask):

    def initialize(self):
        self.log.info("initializing writer task")
        self.buff = FileBuffer('SampleBuffer')

    def execute(self):
        global counter
        counter = self.buff.get('counter')
        try:
            if counter is None:
                self.buff.set('counter', 0)
            else:
                self.buff.set('counter', counter + 1)
        except Exception as e:
            self.log.error(e)
        self.sleep(5)

    def terminate(self):
        self.log.info("terminating task")
        self.buff.purge()


class Task2(BaseServiceTask):

    def initialize(self):
        self.log.info("initializing reader task")
        self.buff = FileBuffer('SampleBuffer')

    def execute(self):
        global counter
        self.log.info("counter = %s" % self.buff.get('counter'))
        self.sleep(1)

    def terminate(self):
        log.info("terminating task")


if __name__ == '__main__':
    log = logging.getLogger()
    log.name = 'FileBuffer'
    try:
        pr = ArgumentParser(prog=None)
        pr.add_argument('-x', dest='debug', action='store_true',
                        help='enable debug mode')
        args = pr.parse_args()

        if args.debug:
            log.setLevel(logging.DEBUG)

        s = BaseService('FileBuffer', logger=log)
        s.tasks = [Task1, Task2]
        s.start()

    except Exception:
        log.fatal(format_exc())
        sys.exit(1)

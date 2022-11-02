# -*- coding: utf-8 -*-
import sys
import logging
from random import randint
from argparse import ArgumentParser

from exonutils.process.service import SimpleService
from exonutils.process.routine import BaseRoutine

logging.basicConfig(
    level=logging.INFO, stream=sys.stdout,
    format='%(asctime)s %(levelname)-5.5s [%(name)s] %(message)s')
logging.addLevelName(logging.WARNING, "WARN")
logging.addLevelName(logging.CRITICAL, "FATAL")


class Worker(BaseRoutine):

    def initialize(self):
        self.log.info("initializing")
        self.close_myself = False

    def execute(self):
        if randint(0, 10) >= 8:
            self.log.info("closing myself")
            self.close_myself = True
            self.stop()
            return

        self.log.info("running %s" % self.name)
        self.sleep(2)

    def terminate(self):
        if not self.close_myself and randint(0, 10) >= 5:
            self.log.info("i will not exit")
            while True:
                self.sleep(10)


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

        srv = SimpleService(
            'WorkersService', logger=logger, debug=args.debug)
        srv.monitor_interval = 1

        for i in range(3):
            srv.add_routine(Worker("worker_%s" % (i + 1)))

        srv.start()

    except Exception as e:
        logger.fatal(str(e), exc_info=args.debug)
        sys.exit(1)
    finally:
        logger.info("exit")


if __name__ == '__main__':
    main()

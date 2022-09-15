# -*- coding: utf-8 -*-
import sys
import logging
from argparse import ArgumentParser

from exonutils.process.service import SimpleService
from exonutils.process.routine import BaseRoutine

logging.basicConfig(
    level=logging.INFO, stream=sys.stdout,
    format='%(asctime)s %(levelname)-5.5s [%(name)s] %(message)s')
logging.addLevelName(logging.WARNING, "WARN")
logging.addLevelName(logging.CRITICAL, "FATAL")

counter = 0


class Routine1(BaseRoutine):

    def initialize(self):
        self.exit_count = None

    def execute(self):
        global counter
        counter += 1
        self.log.info("new count = %s" % counter)

        if counter == 5:
            self.log.info(
                "suspend <%s> at count: %s" % ('rt2', counter))
            self.parent.stop_routine('rt2', suspend=True)
        elif counter == 10:
            self.log.info(
                "resume <%s> at count: %s" % ('rt2', counter))
            self.parent.start_routine('rt2')

        self.sleep(1)

    def terminate(self):
        global counter

        exit_count = counter + 2
        self.log.info("wait exit count = %s" % exit_count)
        while counter < exit_count:
            counter += 1
            self.log.info("new count = %s" % counter)
            self.sleep(1)


class Routine2(BaseRoutine):

    def initialize(self):
        pass

    def execute(self):
        global counter
        self.log.info("monitoring count = %s" % counter)

        if counter == 15:
            self.log.info("stopping myself at count = %s" % counter)
            self.sleep(1)
            self.stop()

        if counter >= 20:
            self.log.info("stopping service at count = %s" % counter)
            self.parent.stop()

        self.sleep(0.5)

    def terminate(self):
        pass


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

        srv = SimpleService('SampleService', logger=logger)
        srv.monitor_interval = 1
        srv.exit_delay = 10

        srv.add_routine(Routine1("rt1"))
        srv.add_routine(Routine2("rt2"))

        srv.start()

    except Exception as e:
        logger.fatal(str(e), exc_info=args.debug)
        sys.exit(1)


if __name__ == '__main__':
    main()

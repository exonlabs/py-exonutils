# -*- coding: utf-8 -*-
import os
import sys
import logging
from tempfile import gettempdir
from argparse import ArgumentParser

from exonutils.process.service import ManagedService
from exonutils.process.routine import BaseRoutine

logging.basicConfig(
    level=logging.INFO, stream=sys.stdout,
    format='%(asctime)s %(levelname)-5.5s [%(name)s] %(message)s')
logging.addLevelName(logging.WARNING, "WARN")
logging.addLevelName(logging.CRITICAL, "FATAL")

# global index counter for workers
WORKERS_INDEX = 1


class Worker(BaseRoutine):

    def initialize(self):
        self.log.info("initializing")

    def execute(self):
        self.log.info("running %s" % self.name)
        self.sleep(2)

    def terminate(self):
        pass


def command_handler(srv, command):
    global WORKERS_INDEX

    if command == 'EXIT':
        srv.stop()
        return

    if 'ADD_WORKER' in command:
        try:
            srv.add_routine(Worker("worker_%s" % WORKERS_INDEX))
            WORKERS_INDEX += 1
            return 'DONE'
        except Exception as e:
            print(e)
            return 'FAILED'

    if 'DEL_WORKER' in command:
        index = command.split(':', 2)[1]
        if srv.del_routine("worker_%s" % index):
            return 'DONE'
        else:
            return 'FAILED'

    if 'START_WORKER' in command:
        index = command.split(':', 2)[1]
        if srv.start_routine("worker_%s" % index):
            return 'DONE'
        else:
            return 'FAILED'

    if 'STOP_WORKER' in command:
        index = command.split(':', 2)[1]
        if srv.stop_routine("worker_%s" % index):
            return 'DONE'
        else:
            return 'FAILED'

    if 'SUSPEND_WORKER' in command:
        index = command.split(':', 2)[1]
        if srv.stop_routine("worker_%s" % index, suspend=True):
            return 'DONE'
        else:
            return 'FAILED'

    return 'INVALID_COMMAND'


def main():
    global WORKERS_INDEX

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

        srv = ManagedService(
            'ManagedService', logger=logger, debug=args.debug)
        srv.monitor_interval = 3
        srv.manage_pipe = os.path.join(
            gettempdir(), '%s.pipe' % srv.name.lower())
        srv.cmdhandler_callback = command_handler

        for i in range(3):
            srv.add_routine(Worker("worker_%s" % WORKERS_INDEX))
            WORKERS_INDEX += 1

        srv.start()

    except Exception as e:
        logger.fatal(str(e), exc_info=args.debug)
        sys.exit(1)
    finally:
        logger.info("exit")


if __name__ == '__main__':
    main()

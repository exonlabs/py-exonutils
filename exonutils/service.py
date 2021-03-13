# -*- coding: utf-8 -*-
"""
    :copyright: 2021, ExonLabs. All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
import threading
import logging
from traceback import format_exc

from .daemon import BaseDaemon

__all__ = ['BaseService', 'BaseServiceTask']


class BaseService(BaseDaemon):

    # interval in sec to check for tasks
    check_interval = 5

    def __init__(self, name=None, logger=None, debug=0):
        super(BaseService, self).__init__(
            name=name, logger=logger, debug=debug)

        # service tasks list
        self.tasks = []

        # runtime threads buffer
        self._threads = dict()

    def initialize(self):
        self.log.info("Initializing")

        # check service tasks list
        if not self.tasks:
            raise RuntimeError("No tasks loaded !!!")
        for T in self.tasks:
            if not issubclass(T, BaseServiceTask):
                raise RuntimeError("Invalid task: %s" % str(T))
        # debug tasks
        if self.debug >= 2:
            self.log.debug("Loaded tasks: (%s)"
                           % ','.join([T.__name__ for T in self.tasks]))

    def execute(self):
        for T in self.tasks:
            try:
                # check and clean dead tasks threads
                thrd = self._threads.get(T.__name__, None)
                if thrd and not thrd.is_alive():
                    del(self._threads[T.__name__])
                    self.log.debug("cleaned dead <TASK:%s>" % T.__name__)

                # start new task thread
                if T.__name__ not in self._threads:
                    self.log.debug("starting <TASK:%s>" % T.__name__)
                    t = T(self)
                    t.start()
                    self._threads[T.__name__] = t

            except Exception:
                self.log.error(format_exc().strip())

        # checking threads interval
        self.sleep(self.check_interval)

    def terminate(self):
        try:
            self.log.info("stopping all tasks")
            for t in self._threads.values():
                t.stop()

            self.log.debug("wait all tasks exit")
            for t in self._threads.values():
                if t.is_alive():
                    t.join()

        except Exception:
            self.log.error(format_exc().strip())

        self.log.info("exit")


class BaseServiceTask(threading.Thread):

    def __init__(self, service):
        super(BaseServiceTask, self).__init__(
            name=self.__class__.__name__)

        # service terminate event
        self.service_term_event = service.term_event
        # task terminate event
        self.term_event = threading.Event()

        # task logger
        self.log = logging.getLogger(self.name)
        self.log.parent = service.log
        # debug level
        self.debug = service.debug

    def initialize(self):
        pass

    def execute(self):
        raise NotImplementedError()

    def terminate(self):
        pass

    def run(self):
        # initialize task
        self.initialize()

        # run task forever
        while not self.term_event.is_set():
            self.execute()

        self.term_event.clear()

        # terminate task
        self.terminate()

    def start(self):
        super(BaseServiceTask, self).start()

    def stop(self):
        self.term_event.set()

    def stop_service(self):
        self.service_term_event.set()

    def sleep(self, timeout):
        self.term_event.wait(timeout=timeout)

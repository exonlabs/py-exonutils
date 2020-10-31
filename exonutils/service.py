# -*- coding: utf-8 -*-
"""
    :copyright: 2020, ExonLabs. All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
import threading
import time
import logging
from traceback import format_exc

from .process import BaseProcess

__all__ = ['BaseService', 'BaseServiceTask']


class BaseService(BaseProcess):

    # interval in sec to check for tasks
    tasks_check_interval = 10

    def __init__(self, name, logger=None, debug=0):
        _logger = logger if logger else logging.getLogger(__name__)
        super(BaseService, self).__init__(name, logger=_logger, debug=debug)

        # runtime threads buffer
        self._threads = dict()

        # service tasks list
        self.tasks = []

        # reload tasks event
        self.reload_event = threading.Event()
        # terminate service event
        self.term_event = threading.Event()

    def initialize(self):
        self.log.info("Initializing")

        # check service tasks list
        if not self.tasks:
            raise RuntimeError("No tasks loaded !!!")
        for T in self.tasks:
            if not issubclass(T, BaseServiceTask):
                raise RuntimeError("Invalid task: %s" % str(T))
        # debug tasks
        if self.debug >= 3:
            self.log.debug("Loaded tasks: (%s)"
                           % ','.join([T.__name__ for T in self.tasks]))

    def run(self):
        self.log.info("Starting all tasks")
        super(BaseService, self).run()

    def execute(self):
        if self.term_event.is_set():
            self.reload_event.clear()
            self.stop()
            return None

        if self.reload_event.is_set():
            self.terminate()

        for T in self.tasks:
            try:
                # checking task thread
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
        for k in range(self.tasks_check_interval):
            time.sleep(1)
            if self.term_event.is_set() or self.reload_event.is_set():
                break

    def terminate(self):
        if self.reload_event.is_set():
            self.log.info("Reload all tasks")
        else:
            self.log.info("Stopping all tasks")

        self.term_event.set()

        # wait all tasks threads to terminate
        for t in self._threads.values():
            if t.is_alive():
                t.join()

        # clean runtime tasks buffer
        self._threads = dict()

        if self.reload_event.is_set():
            self.reload_event.clear()
            self.term_event.clear()
        else:
            self.log.info("Shutting down")

    def handle_sigusr1(self):
        self.reload_event.set()


class BaseServiceTask(threading.Thread):

    def __init__(self, service):
        super(BaseServiceTask, self).__init__(name=self.__class__.__name__)

        # task logger
        self.log = logging.getLogger(self.name)
        self.log.parent = service.log

        # service terminate event
        self.service_term_event = service.term_event
        # task terminate event
        self.term_event = threading.Event()

        # debug level
        self.debug = service.debug

    def initialize(self):
        pass

    def execute(self):
        raise NotImplementedError()

    def terminate(self):
        pass

    def term_signal(self):
        self.term_event.set()

    def run(self):
        # initialize task
        self.initialize()

        try:
            # run task forever or till term_event
            while not self.term_event.is_set():
                self.execute()
                if self.service_term_event.is_set():
                    self.term_signal()
        except Exception:
            self.log.error(format_exc().strip())
        except SystemExit:
            pass

        # terminate task
        self.terminate()

    def start(self):
        super(BaseServiceTask, self).start()

    def stop(self):
        raise SystemExit()

    def sleep(self, timeout):
        if self.service_term_event.wait(timeout=timeout):
            raise SystemExit()

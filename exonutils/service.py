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
from .misc import SharedBuffer

__all__ = ['Service', 'ServiceTask']


class Service(BaseProcess):

    # interval in sec to check for tasks
    tasks_check_interval = 10

    def __init__(self, name, logger=None, tmpdir=None, debug=0):
        super(Service, self).__init__(name, logger=logger, debug=debug)

        # service tasks list
        self.tasks = []
        # shared global buffer
        self.shared_buffer = SharedBuffer(self.name, tmpdir=tmpdir)

        # runtime tasks threads buffer
        self._threads = dict()

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
            if not issubclass(T, ServiceTask):
                raise RuntimeError("Invalid task: %s" % str(T))
        # debug tasks
        self.log.debug("Loaded tasks: (%s)"
                       % ','.join([T.__name__ for T in self.tasks]))

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
                # start new task thread
                if T.__name__ not in self._threads:
                    self.log.debug("start <TASK:%s>" % T.__name__)
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

        # clean shared data
        self.shared_buffer.close()

        if self.reload_event.is_set():
            self.reload_event.clear()
            self.term_event.clear()
        else:
            self.log.info("Shutting down")

    def handle_sigusr1(self):
        self.reload_event.set()


class ServiceTask(threading.Thread):

    def __init__(self, service):
        super(ServiceTask, self).__init__(name=self.__class__.__name__)

        # shared global buffer
        self.shared_buffer = service.shared_buffer
        # task terminate event
        self.term_event = service.term_event

        # task logger
        self.log = logging.getLogger('%s.%s' % (service.log.name, self.name))
        self.log.name = '%s::%s' % (self.log.parent.name, self.name)

    def initialize(self):
        pass

    def execute(self):
        raise NotImplementedError()

    def terminate(self):
        pass

    def run(self):
        # initialize task
        self.initialize()

        try:
            # run task forever or till term_event
            while not self.term_event.is_set():
                self.execute()
        except Exception:
            self.log.error(format_exc().strip())
        except SystemExit:
            pass

        # terminate task
        self.terminate()

    def start(self):
        super(ServiceTask, self).start()

    def stop(self):
        raise SystemExit()

    def sleep(self, timeout):
        if self.term_event.wait(timeout=timeout):
            raise SystemExit()

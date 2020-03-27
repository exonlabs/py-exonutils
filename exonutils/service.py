# -*- coding: utf-8 -*-
"""
    :copyright: 2020, ExonLabs. All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
import threading
import time
import logging

from .process import BaseProcess


class Service(BaseProcess):

    # service tasks list
    tasks = []

    def __init__(self, name, logger=None):
        super(Service, self).__init__(name, logger=logger)

        # threads shared context
        self.context = {}

        # runtime tasks threads buffer
        self._threads = dict()
        # reload tasks flag
        self._tasks_reload = False

        # terminate event
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
            self.stop()
            return None

        if self._tasks_reload:
            self.terminate(shutdown=False)
            self._tasks_reload = False

        for T in self.tasks:
            try:
                # checking task thread
                thrd = self._threads.get(T.__name__, None)
                if thrd and not thrd.is_alive():
                    del(self._threads[T.__name__])
                # start new task thread
                if T.__name__ not in self._threads:
                    self.log.debug("start <TASK:%s>" % T.__name__)
                    t = T(self, context=self.context)
                    t.start()
                    self._threads[T.__name__] = t
            except Exception:
                from traceback import format_exc
                self.log.error(format_exc().strip())

        # checking threads interval
        time.sleep(1)

    def terminate(self, shutdown=True):
        if shutdown:
            self.log.info("Stopping all tasks")
        else:
            self.log.info("Reload all tasks")

        self.term_event.set()
        # wait all tasks threads to terminate
        for t in self._threads.values():
            if t.is_alive():
                t.join()

        # clean runtime tasks buffer
        self._threads = dict()

        if shutdown:
            self.log.info("Shutting down")
        else:
            self.term_event.clear()

    def handle_sighup(self):
        self._tasks_reload = True

    def handle_sigusr1(self):
        rootlogger = logging.getLogger()
        if rootlogger.level != logging.DEBUG:
            rootlogger.setLevel(logging.DEBUG)
            self.log.info("debugging ON")
        else:
            rootlogger.setLevel(logging.INFO)
            self.log.info("debugging OFF")


class ServiceTask(threading.Thread):

    def __init__(self, service, context={}):
        super(ServiceTask, self).__init__(name=self.__class__.__name__)

        # threads shared context
        self.context = context

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
            from traceback import format_exc
            self.log.error(format_exc().strip())
        except SystemExit:
            pass

        # terminate task
        self.terminate()

    def start(self):
        super(ServiceTask, self).start()

    def stop(self):
        raise SystemExit()

    def sleep(self, timeout=0):
        if self.term_event.wait(timeout=timeout):
            raise SystemExit()

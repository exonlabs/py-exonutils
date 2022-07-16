# -*- coding: utf-8 -*-
import time
import threading
import logging

from .daemon import BaseDaemon
from .routine import BaseRoutine

__all__ = []

# interval in sec to check for routines
ROUTINE_MONITOR_INTERVAL = 5
# delay in sec to wait for routines exit
ROUTINE_EXIT_DELAY = 3


class SimpleService(BaseDaemon):

    def __init__(self, name, logger=None):
        super(SimpleService, self).__init__(name, logger=logger)

        self.monitor_interval = ROUTINE_MONITOR_INTERVAL
        self.exit_delay = ROUTINE_EXIT_DELAY

        # buffer holding routines objects
        self._routines = dict()

        # buffer holding running routine threads
        self._threads = dict()
        self._threads_lock = threading.Lock()

    def initialize(self):
        # check service routines list
        if not self._routines:
            raise RuntimeError("INVALID_PARAMS - no routines loaded")

        # debug routines
        self.log.debug(
            "loaded routines: %s" % ', '.join(self._routines.keys()))

    def execute(self):
        self.monitor_routines()

        # wait monitoring interval
        self.sleep(self.monitor_interval)

    def terminate(self):
        self.log.info("stopping all routines")
        for name in self._routines.keys():
            self._routines[name].stop()

        # check running threads and wait their termination
        exit_ts = time.time() + self.exit_delay
        while time.time() <= exit_ts:
            if not self._threads:
                return
            self.sleep(0.1)

        for name in list(self._threads.keys()):
            self.log.error("failed stopping <Routine: %s>" % name)

    def routine_exit_callback(self, name):
        with self._threads_lock:
            if name in self._threads:
                del(self._threads[name])

    def add_routine(self, routine_hnd):
        if not isinstance(routine_hnd, BaseRoutine):
            raise RuntimeError("INVALID_ROUTINE - %s" % routine_hnd)

        routine_hnd.parent = self
        self._routines[routine_hnd.name] = routine_hnd

    def monitor_routines(self):
        for name in self._routines.keys():
            try:
                # check and clean dead routines threads
                th = self._threads.get(name, None)
                if th and not th.is_alive():
                    self.log.warning("found dead <Routine:%s>" % name)
                    with self._threads_lock:
                        del(self._threads[name])

                # start routine
                if name not in self._threads and \
                        not self._routines[name].is_suspended:
                    self.start_routine(name)

            except Exception as e:
                exc = bool(self.log.level == logging.DEBUG)
                self.log.error(str(e), exc_info=exc)

    def start_routine(self, name):
        if name not in self._routines:
            self.log.warning("invalid routine name: %s" % name)
            return False

        # clear suspended state
        self._routines[name].is_suspended = False

        # create and run thread for routine
        with self._threads_lock:
            if name not in self._threads:
                self.log.info("starting <Routine: %s>" % name)
                self._threads[name] = threading.Thread(
                    name=name, daemon=True,
                    target=self._routines[name].start,
                    kwargs={'term_callback': self.routine_exit_callback})
                self._threads[name].start()

        return True

    def stop_routine(self, name, suspend=False, wait_exit=True):
        if name not in self._routines:
            self.log.warning("invalid routine name: %s" % name)
            return False

        if self._routines[name].is_running:
            self.log.info("stopping <Routine: %s>" % name)
        self._routines[name].stop()

        # update suspended state
        self._routines[name].is_suspended = suspend

        if not wait_exit:
            return True

        exit_ts = time.time() + self.exit_delay
        while time.time() <= exit_ts:
            if name not in self._threads:
                return True
            self.sleep(0.1)

        self.log.error("failed stopping <Routine: %s>" % name)
        return False

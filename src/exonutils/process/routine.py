# -*- coding: utf-8 -*-
import threading
import logging

__all__ = []


class BaseRoutine(object):

    def __init__(self, name=None, logger=None):
        # routine name
        self.name = name if name else self.__class__.__name__
        # routine parent handler
        self.parent = None
        # routine logger
        self.log = logger

        # routine run status
        self.is_running = False
        # routine suspend status, will not auto-start by parent
        self.is_suspended = False

        # routine terminate event
        self.term_event = threading.Event()

    def initialize(self):
        pass

    # must override this method in subclass
    def execute(self):
        raise NotImplementedError()

    def terminate(self):
        pass

    def run(self):
        try:
            while not (self.term_event.is_set() or self.is_suspended):
                try:
                    self.is_running = True
                    self.execute()
                except Exception as e:
                    exc = bool(self.log.level == logging.DEBUG)
                    self.log.error(str(e), exc_info=exc)
                    self.sleep(1)
        except (KeyboardInterrupt, SystemExit):
            self.log.debug("routine exit event")

    def start(self, term_callback=None):
        if not self.parent:
            raise RuntimeError(
                "INVALID_PARAMS - no parent handler defined")

        if not self.log:
            self.log = logging.getLogger(self.name)
            self.log.parent = self.parent.log
            self.log.level = self.parent.log.level

        try:
            self.term_event.clear()

            self.log.info("initializing")
            self.initialize()

            # check termination event
            if self.term_event.is_set():
                raise SystemExit()

            # run forever till term event
            self.run()

            self.term_event.clear()

            # graceful terminate
            self.terminate()

        except Exception as e:
            exc = bool(self.log.level == logging.DEBUG)
            self.log.error(str(e), exc_info=exc)
        except (KeyboardInterrupt, SystemExit):
            pass

        try:
            if term_callback:
                term_callback(self.name)
        except Exception as e:
            exc = bool(self.log.level == logging.DEBUG)
            self.log.error(str(e), exc_info=exc)
        except (KeyboardInterrupt, SystemExit):
            pass

        self.is_running = False
        self.log.info("terminated")

    def stop(self):
        self.term_event.set()

    def sleep(self, timeout):
        if self.term_event.wait(timeout=timeout):
            raise SystemExit()

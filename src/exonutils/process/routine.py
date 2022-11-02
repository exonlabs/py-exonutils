# -*- coding: utf-8 -*-
import threading
import logging

__all__ = []


class BaseRoutine(object):

    def __init__(self, name, logger=None, debug=0, auto_start=True):
        # routine name
        self.name = name
        # routine parent handler
        self.parent = None
        # routine logger
        self.log = logger
        # debug mode
        self.debug = debug

        # initial routine status
        self.initial_run = False
        # routine suspend status, will not auto-start by parent
        self.is_suspended = not auto_start
        # routine is cancelled and will be deleted by parent
        self.is_cancelled = False

        # routine terminate event
        self.term_event = threading.Event()

        # thread handler
        self._thread = None

    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, self.name)

    def initialize(self):
        pass

    # must override this method in subclass
    def execute(self):
        raise NotImplementedError()

    def terminate(self):
        pass

    def run(self):
        self.initial_run = True
        self.term_event.clear()

        # initializing
        try:
            self.initialize()
        except Exception as e:
            self.log.error(str(e), exc_info=bool(self.debug >= 2))
            self.log.info("terminated")
            return
        except (KeyboardInterrupt, SystemExit):
            self.log.info("terminated")
            return

        # run forever till term event
        while not (self.term_event.is_set() or
                   self.is_suspended or self.is_cancelled):
            try:
                self.execute()
            except Exception as e:
                self.log.error(str(e), exc_info=bool(self.debug >= 2))
                self.sleep(1)
            except (KeyboardInterrupt, SystemExit):
                break

        self.log.info("-- terminate event --")
        self.term_event.clear()

        # graceful terminate
        try:
            self.terminate()
        except Exception as e:
            self.log.error(str(e), exc_info=bool(self.debug >= 2))
        except (KeyboardInterrupt, SystemExit):
            pass

        self._thread = None
        self.log.info("terminated")

    def start(self):
        if not self.parent:
            raise RuntimeError("no parent service handler")

        if not self.log:
            self.log = logging.getLogger(self.name)
            self.log.parent = self.parent.log
            self.log.level = self.parent.log.level

        self.debug = self.parent.debug
        if not self.debug and self.log.level == logging.DEBUG:
            self.debug = 1

        # clear status
        self.is_suspended = False
        self.is_cancelled = False

        # run routine
        self._thread = threading.Thread(
            name=self.name, daemon=True, target=self.run)
        self._thread.start()

    def stop(self, suspend=False, cancel=False):
        self.is_suspended = bool(suspend or cancel)
        self.is_cancelled = bool(cancel)
        self.term_event.set()

    def is_alive(self):
        if self._thread and self._thread.is_alive():
            return True

        self._thread = None
        return False

    def sleep(self, timeout):
        if self.term_event.wait(timeout=timeout):
            raise SystemExit()

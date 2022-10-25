# -*- coding: utf-8 -*-
import signal
import threading
import logging
from traceback import format_exc

__all__ = []


class BaseDaemon(object):

    # signals to be handled by process
    signals = ['SIGINT', 'SIGTERM', 'SIGQUIT',
               'SIGHUP', 'SIGUSR1', 'SIGUSR2']

    def __init__(self, name=None, logger=None, debug=0):
        # daemon name
        self.name = name if name else self.__class__.__name__.lower()
        # daemon process title to show in os process table
        self.proctitle = self.name

        # terminate event
        self.term_event = threading.Event()

        # process logger
        self.log = logger if logger else logging.getLogger()

        # debug level
        self.debug = debug

    def initialize(self):
        pass

    def execute(self):
        raise NotImplementedError()

    def terminate(self):
        pass

    def run(self):
        try:
            # initialize process
            self.initialize()
            # run process forever untill term event
            while not self.term_event.is_set():
                self.execute()
        except Exception:
            self.log.error(format_exc().strip())
        except (KeyboardInterrupt, SystemExit):
            pass

        try:
            # terminate process
            self.terminate()
        except Exception:
            self.log.error(format_exc().strip())
        except (KeyboardInterrupt, SystemExit):
            pass

        self.log.info('exit')

    def start(self):
        # set signal handlers
        for s in self.signals:
            if hasattr(signal, s):
                signal.signal(getattr(signal, s), self.signal)

        # set process title
        if self.proctitle:
            try:
                from setproctitle import setproctitle
                setproctitle(str(self.proctitle).strip().lower())
            except ImportError:
                self.log.debug(
                    "can't set proctitle - [setproctitle] not installed")

        # run process
        self.run()

    def stop(self):
        self.term_event.set()

    def sleep(self, timeout):
        if self.term_event.wait(timeout=timeout):
            raise SystemExit()

    # signal handler dispatcher
    def signal(self, sig, frame):
        try:
            signame = signal.Signals(sig).name
        except:
            res = [k for k, v in signal.__dict__.iteritems() if v == sig]
            signame = '' if not res else res[0]

        if hasattr(self, "handle_%s" % signame.lower()):
            self.log.info("-- received %s --" % signame)
            getattr(self, "handle_%s" % signame.lower())()
        else:
            self.log.debug("-- received %s -- (ignoring)" % signame)

    def handle_sigint(self):
        self.stop()

    def handle_sigterm(self):
        self.stop()

    def handle_sigquit(self):
        self.stop()

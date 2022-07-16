# -*- coding: utf-8 -*-
import copy
import signal
import threading
import logging
try:
    from setproctitle import setproctitle
except ImportError:
    setproctitle = None

__all__ = []

# signals handled by daemon process
DAEMON_SIGNALS = [
    'SIGINT', 'SIGTERM', 'SIGQUIT',
    'SIGHUP', 'SIGUSR1', 'SIGUSR2',
]


class BaseDaemon(object):

    def __init__(self, name, logger=None):
        # daemon name
        self.name = name
        # daemon process title to show in os process table
        self.proctitle = self.name
        # daemon logger
        self.log = logger

        self.signals = copy.deepcopy(DAEMON_SIGNALS)

        # terminate event
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
            while not self.term_event.is_set():
                try:
                    self.execute()
                except Exception as e:
                    exc = bool(self.log.level == logging.DEBUG)
                    self.log.error(str(e), exc_info=exc)
                    self.sleep(1)
        except (KeyboardInterrupt, SystemExit):
            self.log.debug("daemon exit event")

    def start(self):
        if not self.log:
            self.log = logging.getLogger(self.name)

        # set signal handlers
        for s in self.signals:
            if hasattr(signal, s):
                signal.signal(getattr(signal, s), self.handle_signals)

        # set daemon process title
        if self.proctitle:
            if setproctitle:
                setproctitle(str(self.proctitle).strip().lower())
            else:
                self.log.debug("ignoring setproctitle - not installed")

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

        self.log.info("exit")

    def stop(self):
        self.term_event.set()

    def sleep(self, timeout):
        if self.term_event.wait(timeout=timeout):
            raise SystemExit()

    # signal handler dispatcher
    def handle_signals(self, sig, frame):
        try:
            signame = signal.Signals(sig).name
        except:
            res = [k for k, v in signal.__dict__.iteritems() if v == sig]
            signame = '' if not res else res[0]

        if hasattr(self, "handle_%s" % signame.lower()):
            self.log.info("received %s" % signame)
            getattr(self, "handle_%s" % signame.lower())()
        else:
            self.log.debug("received %s - (ignoring)" % signame)

    def handle_sigint(self):
        self.stop()

    def handle_sigterm(self):
        self.stop()

    def handle_sigquit(self):
        self.stop()

# -*- coding: utf-8 -*-
import signal
import threading
import logging
try:
    from setproctitle import setproctitle
except ImportError:
    setproctitle = None

__all__ = []


class BaseDaemon(object):

    def __init__(self, name, proctitle='', logger=None, debug=0):
        # daemon name
        self.name = name
        # daemon process title to show in OS process table
        self.proctitle = proctitle or name
        # daemon logger
        self.log = logger
        # debug mode
        self.debug = debug

        # default signals handled by daemon process
        self.signals = [
            'SIGINT', 'SIGTERM', 'SIGQUIT',
            'SIGHUP', 'SIGUSR1', 'SIGUSR2',
        ]

        # daemon terminate event
        self.term_event = threading.Event()

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
        self.term_event.clear()

        # initializing
        try:
            self.initialize()
        except Exception as e:
            self.log.error(str(e), exc_info=bool(self.debug >= 2))
            return
        except (KeyboardInterrupt, SystemExit):
            return

        # run forever till term event
        while not self.term_event.is_set():
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

    def start(self):
        if not self.log:
            self.log = logging.getLogger(self.name)
        if not self.debug and self.log.level == logging.DEBUG:
            self.debug = 1

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

        # run daemon
        self.run()

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
            self.log.info("<received: %s>" % signame)
            getattr(self, "handle_%s" % signame.lower())()
        else:
            self.log.debug("<received: %s> - ignoring" % signame)

    def handle_sigint(self):
        self.stop()

    def handle_sigterm(self):
        self.stop()

    def handle_sigquit(self):
        self.stop()

# -*- coding: utf-8 -*-
"""
    :copyright: 2021, ExonLabs. All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
import sys
import signal
import threading
import logging
from traceback import format_exc

__all__ = ['BaseProcess']


class BaseProcess(object):

    # signals to be handled by process
    signals = ['SIGINT', 'SIGTERM', 'SIGQUIT',
               'SIGHUP', 'SIGUSR1', 'SIGUSR2']

    def __init__(self, name, logger=None, debug=0):
        # process name
        self.name = name
        # process title to show in process table
        self.proctitle = self.name

        # terminate event
        self.term_event = threading.Event()

        # process logger
        self.log = logger if logger else logging.getLogger(__name__)

        # debug level
        self.debug = debug

    def initialize(self):
        pass

    def execute(self):
        raise NotImplementedError()

    def terminate(self):
        pass

    def run(self):
        # initialize process
        self.initialize()

        # run process forever
        while not self.term_event.is_set():
            try:
                self.execute()
            except Exception:
                self.log.error(format_exc().strip())
            except (KeyboardInterrupt, SystemExit):
                break

        self.term_event.clear()

        # terminate process
        self.terminate()

    def start(self):
        try:
            # set process title
            if self.proctitle:
                try:
                    from setproctitle import setproctitle
                    setproctitle(str(self.proctitle).strip())
                except ImportError:
                    self.log.debug(
                        "ignoring setproctitle - package not installed")

            # set process signal handler
            for s in self.signals:
                if hasattr(signal, s):
                    signal.signal(getattr(signal, s), self.signal)

            # run process
            self.run()

        except Exception:
            self.log.error(format_exc().strip())
            sys.exit(1)

        sys.exit(0)

    def stop(self):
        self.term_event.set()

    def sleep(self, timeout):
        self.term_event.wait(timeout=timeout)

    # signal handler dispatcher
    def signal(self, sig, frame):
        try:
            signame = signal.Signals(sig).name
        except:
            res = [k for k, v in signal.__dict__.iteritems() if v == sig]
            signame = '' if not res else res[0]

        handler = getattr(self, "handle_%s" % signame.lower(), None)
        if handler:
            self.log.info("-- received %s --" % signame)
            handler()
        else:
            self.log.info(
                "-- received %s -- (no handler defined)" % signame)

    def handle_sigint(self):
        self.stop()

    def handle_sigterm(self):
        self.stop()

    def handle_sigquit(self):
        self.stop()

    def handle_sighup(self):
        self.stop()

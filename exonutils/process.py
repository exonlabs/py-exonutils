# -*- coding: utf-8 -*-
"""
    :copyright: 2020, ExonLabs. All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
import sys
import signal
import logging
from setproctitle import setproctitle
from traceback import format_exc

__all__ = ['BaseProcess']


class BaseProcess(object):

    # signals to be handled by process
    signals = [signal.SIGINT, signal.SIGQUIT, signal.SIGTERM,
               signal.SIGHUP, signal.SIGUSR1, signal.SIGUSR2]

    def __init__(self, name, logger=None):
        # process name
        self.name = name
        # process title to show in process table
        self.proctitle = self.name

        # process logger
        if logger and isinstance(logger, logging.Logger):
            self.log = logger
        else:
            self.log = logging.getLogger(self.name)

    def initialize(self):
        pass

    def execute(self):
        raise NotImplementedError()

    def terminate(self):
        pass

    def run(self):
        try:
            # run process forever
            while True:
                self.execute()
        except Exception:
            self.log.error(format_exc().strip())
            self.stop(exit_status=1)
        except KeyboardInterrupt:
            self.stop()

    def start(self):
        # initialize process
        self.initialize()

        # set process title
        if self.proctitle:
            setproctitle(str(self.proctitle).strip())

        # set process signal handler
        for s in self.signals:
            signal.signal(s, self.signal)

        # run process
        self.run()

    def stop(self, exit_status=0):
        try:
            self.terminate()
            sys.exit(exit_status)
        except Exception:
            self.log.error(format_exc().strip())
            sys.exit(1)

    # process signal handler dispatcher
    def signal(self, sig, frame):
        try:
            signame = signal.Signals(sig).name
        except:
            res = [k for k, v in signal.__dict__.iteritems() if v == sig]
            signame = '' if not res else res[0]

        self.log.debug("received signal: %s" % signame)
        handler = getattr(self, "handle_%s" % signame.lower(), None)
        if handler:
            handler()
        else:
            self.log.debug("no signal handler defined")

    def handle_sigint(self):
        self.stop()

    def handle_sigquit(self):
        self.stop()

    def handle_sigterm(self):
        self.stop()

    def handle_sighup(self):
        self.stop()

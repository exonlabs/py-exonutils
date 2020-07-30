# -*- coding: utf-8 -*-
"""
    :copyright: 2020, ExonLabs. All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
import sys
import signal
import logging
from traceback import format_exc

__all__ = ['BaseProcess']

_log = logging.getLogger('%s.core' % __package__)


class BaseProcess(object):

    # signals to be handled by process
    signals = ['SIGINT', 'SIGTERM', 'SIGQUIT',
               'SIGHUP', 'SIGUSR1', 'SIGUSR2']

    def __init__(self, name):
        # process name
        self.name = name
        # process title to show in process table
        self.proctitle = self.name

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
            _log.error(format_exc().strip())
            self.stop(exit_status=1)
        except KeyboardInterrupt:
            self.stop()

    def start(self):
        # initialize process
        self.initialize()

        # set process title
        if self.proctitle:
            try:
                from setproctitle import setproctitle
                setproctitle(str(self.proctitle).strip())
            except ImportError:
                _log.debug("ignoring setproctitle - package not installed")

        # set process signal handler
        for s in self.signals:
            if hasattr(signal, s):
                signal.signal(getattr(signal, s), self.signal)
            else:
                _log.debug("invalid or not supported signal %s" % s)

        # run process
        self.run()

    def stop(self, exit_status=0):
        try:
            self.terminate()
            sys.exit(exit_status)
        except Exception:
            _log.error(format_exc().strip())
            sys.exit(1)

    # process signal handler dispatcher
    def signal(self, sig, frame):
        try:
            signame = signal.Signals(sig).name
        except:
            res = [k for k, v in signal.__dict__.iteritems() if v == sig]
            signame = '' if not res else res[0]

        handler = getattr(self, "handle_%s" % signame.lower(), None)
        if handler:
            _log.debug("execute handler for signal: %s" % signame)
            handler()
        else:
            _log.debug("received signal: %s - (no handler)" % signame)

    def handle_sigint(self):
        self.stop()

    def handle_sigquit(self):
        self.stop()

    def handle_sigterm(self):
        self.stop()

    def handle_sighup(self):
        self.stop()

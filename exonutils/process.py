# -*- coding: utf-8 -*-
"""
    :copyright: 2020, ExonLabs. All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
import sys
import signal
import logging

# dict mapping all signal numbers to names
SIG_NAMES = dict(
    (getattr(signal, name), name.lower()) for name in dir(signal)
    if name[:3] == "SIG" and name[3] != "_")


class BaseProcess(object):

    # signals to be handled by process
    SIGNALS = [getattr(signal, 'SIG%s' % n)
               for n in "INT QUIT TERM HUP USR1 USR2".split()
               if ('SIG%s' % n).lower() in SIG_NAMES.values()]

    def __init__(self, name, logger=None):
        # process name
        self.name = name
        # process title to show in process table
        self.proctitle = self.name

        # process logger
        if logger and isinstance(logger, logging.Logger):
            self.log = logger
        else:
            self.log = logging.getLogger()
            self.log.name = self.name

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
            from traceback import format_exc
            self.log.error(format_exc().strip())
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
                self.log.warn("ignoring proctitle value, " +
                              "'setproctitle' package not installed")

        # set process signal handler
        for s in self.SIGNALS:
            signal.signal(s, self.signal)

        # run process
        self.run()

    def stop(self, exit_status=0):
        try:
            self.terminate()
            sys.exit(exit_status)
        except Exception:
            from traceback import format_exc
            self.log.error(format_exc().strip())
            sys.exit(1)

    # process signal handler dispatcher
    def signal(self, sig, frame):
        signame = SIG_NAMES[sig]
        self.log.debug("received signal: %s" % signame.upper())
        handler = getattr(self, "handle_%s" % signame, None)
        if handler:
            handler()
        else:
            self.log.debug("no handler defined, nothing to do")

    def handle_sigint(self):
        self.stop()

    def handle_sigquit(self):
        self.stop()

    def handle_sigterm(self):
        self.stop()

    def handle_sighup(self):
        self.stop()

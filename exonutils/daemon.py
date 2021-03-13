# -*- coding: utf-8 -*-
"""
    :copyright: 2021, ExonLabs. All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
import signal
import threading
import logging

__all__ = ['BaseDaemon']


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
        # initialize process
        self.initialize()

        # run process forever
        while not self.term_event.is_set():
            self.execute()

        self.term_event.clear()

        # terminate process
        self.terminate()

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
            self.log.debug("-- received %s -- (ignoring)" % signame)

    def handle_sigint(self):
        self.stop()

    def handle_sigterm(self):
        self.stop()

    def handle_sigquit(self):
        self.stop()

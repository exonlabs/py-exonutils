# -*- coding: utf-8 -*-
import sys
import logging
from argparse import ArgumentParser
from traceback import format_exc

from exonutils.webapp import BaseWebApp, BaseWebView

logging.basicConfig(
    level=logging.INFO, stream=sys.stdout,
    format='%(asctime)s %(levelname)-5.5s [%(name)s] %(message)s')
logging.addLevelName(logging.WARNING, "WARN")
logging.addLevelName(logging.CRITICAL, "FATAL")


class IndexView(BaseWebView):
    routes = [('/', 'index')]

    @classmethod
    def initialize(cls, webapp, app):
        log = logging.getLogger(cls.__name__)
        log.info("initializing")

    def get(self, **kwargs):
        self.log.debug(self.__class__.__name__)
        return self.__class__.__name__


class HomeView(BaseWebView):
    routes = [('/home', 'home')]

    @classmethod
    def initialize(cls, webapp, app):
        log = logging.getLogger(cls.__name__)
        log.info("initializing")

    def get(self, **kwargs):
        self.log.debug(self.__class__.__name__)
        return self.__class__.__name__


class ExitView(BaseWebView):
    routes = [('/exit', 'exit')]

    def get(self, **kwargs):
        self.webapp.stop()
        return ''


if __name__ == '__main__':
    log = logging.getLogger()
    log.name = 'main'
    try:
        pr = ArgumentParser(prog=None)
        pr.add_argument(
            '-x', dest='debug', action='count', default=0,
            help='set debug modes')
        args = pr.parse_args()

        if args.debug > 0:
            log.setLevel(logging.DEBUG)

        cfg = {
            'secret_key': "0123456789ABCDEF",
            'max_content_length': 10485760,
            'templates_auto_reload': bool(args.debug >= 3),
        }
        webapp = BaseWebApp(options=cfg, logger=log, debug=args.debug)
        webapp.views = [
            IndexView, HomeView,
            ExitView,
        ]
        webapp.initialize()
        webapp.start('0.0.0.0', 8000)

    except Exception:
        log.fatal(format_exc())
        sys.exit(1)

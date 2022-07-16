# -*- coding: utf-8 -*-
import sys
import logging
from argparse import ArgumentParser

from exonutils.webapp.server import SimpleWebServer
from exonutils.webapp.view import BaseWebView

logging.basicConfig(
    level=logging.INFO, stream=sys.stdout,
    format='%(asctime)s %(levelname)-5.5s [%(name)s] %(message)s')
logging.addLevelName(logging.WARNING, "WARN")
logging.addLevelName(logging.CRITICAL, "FATAL")


class IndexView(BaseWebView):
    routes = [('/', 'index')]

    def get(self, **kwargs):
        self.log.debug(self.__class__.__name__)
        return self.__class__.__name__


class HomeView(BaseWebView):
    routes = [('/home', 'home')]

    def get(self, **kwargs):
        self.log.debug(self.__class__.__name__)
        return self.__class__.__name__


class ExitView(BaseWebView):
    routes = [('/exit', 'exit')]

    def get(self, **kwargs):
        self.parent.stop()
        return ''


def main():
    logger = logging.getLogger()
    logger.name = 'main'

    reqlog = logging.getLogger('%s.requests' % logger.name)
    reqlog.handlers = [logging.StreamHandler(sys.stdout)]

    try:
        pr = ArgumentParser(prog=None)
        pr.add_argument(
            '-x', dest='debug', action='count', default=0,
            help='set debug modes')
        args = pr.parse_args()

        if args.debug > 0:
            logger.setLevel(logging.DEBUG)

        options = {
            'secret_key': "0123456789ABCDEF",
            'max_content_length': 10485760,
            'templates_auto_reload': bool(args.debug >= 3),
        }

        websrv = SimpleWebServer(
            options=options, logger=logger, reqlogger=reqlog)
        websrv.initialize()

        for view_cls in BaseWebView.__subclasses__():
            websrv.add_view(view_cls())

        websrv.start(
            '0.0.0.0', 8000,
            debug=bool(args.debug >= 1),
            use_reloader=bool(args.debug >= 3)
        )

    except Exception as e:
        logger.fatal(str(e), exc_info=args.debug)
        sys.exit(1)


if __name__ == '__main__':
    main()

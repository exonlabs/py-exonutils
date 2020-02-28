# -*- coding: utf-8 -*-
import sys
import logging
from argparse import ArgumentParser
from traceback import format_exc

from exonutils.webserver import WebServer, WebView

logging.basicConfig(
    level=logging.INFO, stream=sys.stdout,
    format='%(asctime)s [%(name)s] %(levelname)s %(message)s')

cfg = {
    'app': {
        'secret_key': "0123456789ABCDEF",
        'max_content_length': 10485760,
    },
    'engine': {
        'host': '0.0.0.0',
        'port': 8000,
        'workers': 2,
        'max_requests': 200,
        'max_requests_jitter': 50,
    },
}


class IndexView(WebView):
    routes = [('/', 'index')]

    def get(self, **kw):
        self.log.debug(self.__class__.__name__)
        return self.__class__.__name__


class HomeView(WebView):
    routes = [('/home', 'home')]

    def get(self, **kw):
        self.log.debug(self.__class__.__name__)
        return self.__class__.__name__


if __name__ == '__main__':
    try:
        pr = ArgumentParser(prog=None)
        pr.add_argument('-x', dest='debug', action='store_true',
                        help='enable debug mode')
        pr.add_argument('--simple', action='store_true',
                        help='use simple web engine')
        pr.add_argument('--workers', type=int, metavar='N',
                        help='number of workers handling requests')
        args = pr.parse_args()

        if args.debug:
            logging.getLogger().setLevel(logging.DEBUG)

        if args.simple:
            cfg['simple_engine'] = True
        elif args.workers:
            cfg['engine']['workers'] = args.workers

        p = WebServer('SamplePortal', options=cfg)
        p.views = [IndexView, HomeView]
        p.start()

    except Exception:
        print(format_exc())
        sys.exit(1)

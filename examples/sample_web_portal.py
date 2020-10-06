# -*- coding: utf-8 -*-
import sys
import logging
from argparse import ArgumentParser
from traceback import format_exc

from exonutils.webapp import BaseWebApp, BaseWebView

try:
    import colorama
    colorama.init()
except ImportError:
    pass

logging.basicConfig(
    level=logging.INFO, stream=sys.stdout,
    format='%(asctime)s [%(name)s] %(levelname)s %(message)s')

rlog = logging.getLogger('werkzeug')
rlog.setLevel(logging.INFO)
rlog.propagate = False


class IndexView(BaseWebView):
    routes = [('/', 'index')]

    def get(self, **kw):
        self.log.debug(self.__class__.__name__)
        return self.__class__.__name__


class HomeView(BaseWebView):
    routes = [('/home', 'home')]

    def get(self, **kw):
        self.log.debug(self.__class__.__name__)
        return self.__class__.__name__


if __name__ == '__main__':
    log = logging.getLogger()
    log.name = 'SamplePortal'
    try:
        pr = ArgumentParser(prog=None)
        # debug modes:
        # -x      debug ON
        # -xxx    debug ON, dev mode ON
        pr.add_argument('-x', dest='debug', action='count', default=0,
                        help='set debug modes')
        args = pr.parse_args()

        if args.debug > 0:
            log.setLevel(logging.DEBUG)

        cfg = {
            'secret_key': "0123456789ABCDEF",
            'max_content_length': 10485760,
            'templates_auto_reload': bool(args.debug > 0),
        }
        webapp = BaseWebApp('SamplePortal', options=cfg, logger=log)
        webapp.views = [IndexView, HomeView]

        log.info("Initializing")
        webapp.create_app().run(
            host='0.0.0.0',
            port='8000',
            debug=bool(args.debug >= 1),
            use_reloader=bool(args.debug >= 3))

    except Exception:
        log.fatal(format_exc())
        sys.exit(1)

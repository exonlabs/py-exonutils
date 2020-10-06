# -*- coding: utf-8 -*-
import sys
import logging
from flask import request
from argparse import ArgumentParser
from traceback import format_exc

from exonutils.webapp import BaseRESTWebApp, BaseWebView

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


class XMLRESTWebServer(BaseRESTWebApp):

    def response_parser(self, data, status):
        res = '<?xml version="1.0" encoding="UTF-8"?>\n<data>\n'
        for k, v in data.items():
            res += '<param name="%s">%s</param>\n' % (k, v)
        res += '</data>'
        return res, status, {'Content-Type': 'text/xml'}


class Res1(BaseWebView):
    routes = [('/res1', 'res1'),
              ('/res1/<guid>', 'res1_1')]

    def get(self, **kw):
        self.log.debug(self.__class__.__name__)
        return kw


class Res2(BaseWebView):
    routes = [('/res2', 'res2'),
              ('/res2/<guid>', 'res2_1')]

    def get(self, **kw):
        self.log.debug(self.__class__.__name__)
        return {'result': self.__class__.__name__}

    def post(self, **kw):
        return {'kwargs': kw,
                'req_args': request.args,
                'req_data': request.data,
                'req_form': request.form,
                'req_json': request.json}


if __name__ == '__main__':
    log = logging.getLogger()
    log.name = 'SampleRESTSRV'
    try:
        pr = ArgumentParser(prog=None)
        # debug modes:
        # -x      debug ON
        # -xxx    debug ON, dev mode ON
        pr.add_argument('-x', dest='debug', action='count', default=0,
                        help='set debug modes')
        pr.add_argument('--xml', action='store_true',
                        help='use XML rest interface')
        args = pr.parse_args()

        if args.debug > 0:
            log.setLevel(logging.DEBUG)

        cfg = {
            'secret_key': "0123456789ABCDEF",
            'max_content_length': 10485760,
            'templates_auto_reload': bool(args.debug > 0),
        }
        cls = XMLRESTWebServer if args.xml else BaseRESTWebApp
        webapp = cls('SampleRESTSRV', options=cfg, logger=log)
        webapp.views = [Res1, Res2]

        log.info("Initializing")
        webapp.create_app().run(
            host='0.0.0.0',
            port='8000',
            debug=bool(args.debug >= 1),
            use_reloader=bool(args.debug >= 3))

    except Exception:
        log.fatal(format_exc())
        sys.exit(1)

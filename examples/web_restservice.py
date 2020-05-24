# -*- coding: utf-8 -*-
import sys
import logging
from flask import request
from argparse import ArgumentParser
from traceback import format_exc

from exonutils.webserver import RESTWebServer, WebView

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


class XMLRESTWebServer(RESTWebServer):

    def response_parser(self, data, status):
        res = '<?xml version="1.0" encoding="UTF-8"?>\n<data>\n'
        for k, v in data.items():
            res += '<param name="%s">%s</param>\n' % (k, v)
        res += '</data>'
        return res, status, {'Content-Type': 'text/xml'}


class Res1(WebView):
    routes = [('/res1', 'res1'),
              ('/res1/<guid>', 'res1_1')]

    def get(self, **kw):
        self.log.debug(self.__class__.__name__)
        return kw


class Res2(WebView):
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
    try:
        pr = ArgumentParser(prog=None)
        pr.add_argument('-x', dest='debug', action='count', default=0,
                        help='set debug modes')
        pr.add_argument('--simple', action='store_true',
                        help='use simple web engine')
        pr.add_argument('--workers', type=int, metavar='N',
                        help='number of workers handling requests')
        pr.add_argument('--xml', action='store_true',
                        help='use XML rest interface')
        args = pr.parse_args()

        if args.debug > 0:
            logging.getLogger().setLevel(logging.DEBUG)

        if args.simple:
            cfg['simple_engine'] = True
        elif args.workers:
            cfg['engine']['workers'] = args.workers

        cls = XMLRESTWebServer if args.xml else RESTWebServer
        h = cls('SampleRESTSRV', options=cfg, debug=args.debug)
        h.views = [Res1, Res2]
        h.start()

    except Exception:
        print(format_exc())
        sys.exit(1)

# -*- coding: utf-8 -*-
import sys
import logging
from flask import request
from argparse import ArgumentParser
from traceback import format_exc

from exonutils.webapp import BaseRESTWebApp, BaseWebView

logging.basicConfig(
    level=logging.INFO, stream=sys.stdout,
    format='%(asctime)s %(levelname)-5.5s [%(name)s] %(message)s')
logging.addLevelName(logging.WARNING, "WARN")
logging.addLevelName(logging.CRITICAL, "FATAL")


class XMLRESTWebServer(BaseRESTWebApp):

    def response_parser(self, data, status):
        headers = {
            'Content-Type': 'text/xml; charset=utf-8',
        }

        res = '<?xml version="1.0" encoding="UTF-8"?>\n<data>\n'
        for k, v in data.items():
            res += '<param name="%s">%s</param>\n' % (k, v)
        res += '</data>'

        return res, status, headers


class Res1(BaseWebView):
    routes = [('/res1', 'res1'),
              ('/res1/<guid>', 'res1_1')]

    def get(self, **kwargs):
        self.log.debug(self.__class__.__name__)
        return kwargs


class Res2(BaseWebView):
    routes = [('/res2', 'res2'),
              ('/res2/<guid>', 'res2_1')]

    def get(self, **kwargs):
        self.log.debug(self.__class__.__name__)
        return {
            'result': self.__class__.__name__,
        }

    def post(self, **kwargs):
        return {
            'kwargs': kwargs,
            'req_args': request.args,
            'req_data': request.data,
            'req_form': request.form,
            'req_json': request.json,
        }


if __name__ == '__main__':
    log = logging.getLogger()
    log.name = 'main'
    try:
        pr = ArgumentParser(prog=None)
        pr.add_argument(
            '-x', dest='debug', action='count', default=0,
            help='set debug modes')
        pr.add_argument(
            '--xml', action='store_true',
            help='use XML rest interface')
        args = pr.parse_args()

        if args.debug > 0:
            log.setLevel(logging.DEBUG)

        cfg = {
            'secret_key': "0123456789ABCDEF",
            'max_content_length': 10485760,
            'templates_auto_reload': bool(args.debug >= 3),
        }
        cls = XMLRESTWebServer if args.xml else BaseRESTWebApp
        webapp = cls(options=cfg, logger=log, debug=args.debug)
        webapp.views = [
            Res1, Res2,
        ]
        webapp.initialize()
        webapp.start('0.0.0.0', 8000)

    except Exception:
        log.fatal(format_exc())
        sys.exit(1)

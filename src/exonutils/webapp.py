# -*- coding: utf-8 -*-
"""
    :copyright: 2021, ExonLabs. All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
import os
import uuid
import signal
import logging
from flask import Flask, request, jsonify
from jinja2 import BaseLoader
from traceback import format_exc

try:
    import colorama
    colorama.init()
except ImportError:
    pass

__all__ = ['BaseWebSrv', 'BaseRESTWebSrv', 'BaseWebView']


class BaseWebSrv(object):

    def __init__(self, name=None, options={}, logger=None,
                 req_logger=None, debug=0):
        self.name = name if name else self.__class__.__name__.lower()
        self.options = options
        self.debug = debug
        self.base_path = ''
        self.tpl_loader = None
        self.app = None

        # websrv logger
        self.log = logger if logger else logging.getLogger()
        # websrv requests logger
        self.reqlog = req_logger if req_logger else \
            logging.getLogger('%s.requests' % self.log.name)
        self.reqlog.setLevel(logging.INFO)
        self.reqlog.propagate = False
        if not self.reqlog.handlers:
            self.reqlog.handlers = [logging.NullHandler()]

    def initialize(self):
        self.log.info("Initializing")
        self.app = self.create_app()

    def load_views(self, views):
        # initialize view
        for V in views:
            if not issubclass(V, BaseWebView):
                raise RuntimeError("invalid view: %s" % str(V))

            v = V(self)
            if hasattr(v, 'initialize'):
                v.initialize()
            for url, endpoint in v.routes:
                self.app.add_url_rule(
                    url, endpoint=endpoint,
                    view_func=v.dispatch_request,
                    methods=v.methods)

    def create_app(self):
        # check and adjust app options
        if not self.options.get('secret_key', None):
            self.options['secret_key'] = uuid.uuid5(
                uuid.uuid1(), uuid.uuid4().hex).hex
        if not self.options.get('max_content_length', None):
            self.options['max_content_length'] = 10485760  # 10 MiB
        self.options['trap_http_exceptions'] = True
        self.options['trap_bad_request_errors'] = True

        # create flask app
        app = Flask(
            self.name,
            template_folder=os.path.join(self.base_path, 'templates'),
            static_folder=os.path.join(self.base_path, 'static'))

        # update app config from options
        for k, v in self.options.items():
            app.config[k.upper()] = v

        # set jinja options
        app.jinja_env.autoescape = True
        app.jinja_env.auto_reload = app.config.get('TEMPLATES_AUTO_RELOAD')
        if self.tpl_loader and isinstance(self.tpl_loader, BaseLoader):
            app.jinja_loader = self.tpl_loader

        # register exception handler
        @app.errorhandler(Exception)
        def exception_handler(e):
            if hasattr(e, 'name') and hasattr(e, 'code'):
                return self.handle_response((e.name, e.code))
            else:
                self.log.error(format_exc().strip())
                return self.handle_response(("Internal Server Error", 500))

        return app

    # response handler
    def handle_response(self, result):
        return result

    def start(self, host, port):
        # adjust request logs
        logging.getLogger('werkzeug').parent = self.reqlog

        # process PID
        self.root_pid = os.getpid()

        self.app.run(
            host=host, port=port,
            debug=bool(self.debug >= 1),
            use_reloader=bool(self.debug >= 3))

    def stop(self):
        os.kill(self.root_pid, signal.SIGTERM)


class BaseRESTWebSrv(BaseWebSrv):

    def handle_response(self, response):
        if type(response) is tuple:
            data, code = response[0], response[1]
        else:
            data, code = response, 200

        if type(data) is not dict:
            key = 'error' if code >= 400 else 'result'
            data = {key: data}

        return self.format_response(data, code)

    # default response parser is to send JSON data results
    def format_response(self, data, status):
        return (jsonify(**data), status)


class BaseWebView(object):
    routes = []
    methods = ['GET', 'POST']

    def __init__(self, websrv):
        self.name = self.__class__.__name__
        self.websrv = websrv
        self.debug = websrv.debug

        # view logger
        self.log = logging.getLogger(self.name)
        self.log.parent = websrv.log

    # def initialize(self):
    #     pass

    def dispatch_request(self, *args, **kwargs):
        # exec before request handlers
        if hasattr(self, 'before_request'):
            result = self.before_request()
            if result is not None:
                return self.websrv.handle_response(result)

        result = self.run_request(
            request.method.lower(), *args, **kwargs)

        # exec after request handlers
        if hasattr(self, 'after_request'):
            result = self.after_request(result)

        return self.websrv.handle_response(result)

    def run_request(self, method, *args, **kwargs):
        if not hasattr(self, method):
            # use GET method instead of HEAD if no handler
            if method == 'head' and hasattr(self, 'get'):
                method = 'get'
            else:
                return self.websrv.handle_response(
                    ("Method Not Allowed", 405))

        return getattr(self, method)(*args, **kwargs)

    # @classmethod
    # def before_request(cls):
    #     return None

    # @classmethod
    # def after_request(cls, response):
    #     return response

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
from flask.views import MethodView
from jinja2 import BaseLoader
from traceback import format_exc

try:
    import colorama
    colorama.init()
except ImportError:
    pass

__all__ = ['BaseWebApp', 'BaseRESTWebApp', 'BaseWebView']


class BaseWebApp(object):

    def __init__(self, name=None, options={}, logger=None, debug=0):
        self.name = name if name else self.__class__.__name__.lower()
        self.options = options
        self.base_path = ''
        self.tpl_loader = None

        # webapp views list
        self.views = []

        # webapp logger
        self.log = logger if logger else logging.getLogger()
        # webapp requests logger
        self.reqlog = logging.getLogger('%s.requests' % self.log.name)
        self.reqlog.setLevel(logging.INFO)
        self.reqlog.propagate = False

        # debug level
        self.debug = debug

    def initialize(self):
        self.log.info("Initializing")

        # check websrv views list
        if not self.views:
            raise RuntimeError("No views loaded !!!")
        for V in self.views:
            if not issubclass(V, BaseWebView):
                raise RuntimeError("Invalid view: %s" % str(V))
        # debug views
        if self.debug >= 2:
            self.log.debug("Loaded views: (%s)"
                           % ','.join([V.__name__ for V in self.views]))

    # response handler
    def response_handler(self, result):
        return result

    def create_app(self):
        # create flask app
        app = Flask(
            self.name,
            template_folder=os.path.join(self.base_path, 'templates'),
            static_folder=os.path.join(self.base_path, 'static'))

        # check app options
        if not self.options.get('secret_key', None):
            self.options['secret_key'] = uuid.uuid5(
                uuid.uuid1(), uuid.uuid4().hex).hex
        if not self.options.get('max_content_length', None):
            self.options['max_content_length'] = 10485760  # 10 MiB

        # update app config from options
        for k, v in self.options.items():
            app.config[k.upper()] = v
        # force specific app config
        app.config['TRAP_HTTP_EXCEPTIONS'] = True
        app.config['TRAP_BAD_REQUEST_ERRORS'] = True

        # set jinja options
        app.jinja_env.autoescape = True
        app.jinja_env.auto_reload = app.config.get('TEMPLATES_AUTO_RELOAD')
        if self.tpl_loader and isinstance(self.tpl_loader, BaseLoader):
            app.jinja_loader = self.tpl_loader

        # register exception handler
        @app.errorhandler(Exception)
        def exception_handler(e):
            if hasattr(e, 'name') and hasattr(e, 'code'):
                return self.response_handler((e.name, e.code))
            else:
                self.log.error(format_exc().strip())
                return self.response_handler(("Internal Server Error", 500))

        # load webapp views
        if not self.views:
            raise RuntimeError("No views loaded !!!")
        for V in self.views:
            V._initialize(self, app)
            for url, endpoint in V.routes:
                app.add_url_rule(url, view_func=V.as_view(endpoint, self))

        return app

    def start(self, host, port):
        # adjust request logs
        logging.getLogger('werkzeug').parent = self.reqlog

        # process PID
        self.root_pid = os.getpid()

        self.create_app().run(
            host=host, port=port,
            debug=bool(self.debug >= 1),
            use_reloader=bool(self.debug >= 3))

    def stop(self):
        os.kill(self.root_pid, signal.SIGTERM)


class BaseRESTWebApp(BaseWebApp):

    # default response parser is to send JSON data results
    def response_parser(self, data, status):
        return (jsonify(**data), status)

    def response_handler(self, response):
        if type(response) is tuple:
            data, code = response[0], response[1]
        else:
            data, code = response, 200

        if type(data) is not dict:
            key = 'error' if code >= 400 else 'result'
            data = {key: data}

        return self.response_parser(data, code)


class BaseWebView(MethodView):
    routes = []

    def __init__(self, webapp):
        self.name = self.__class__.__name__
        self.webapp = webapp
        self.response_handler = webapp.response_handler

        # view logger
        self.log = logging.getLogger(self.name)
        self.log.parent = webapp.log

        # debug level
        self.debug = webapp.debug

    @classmethod
    def _initialize(cls, webapp, app):
        return cls.initialize(webapp, app)

    @classmethod
    def initialize(cls, webapp, app):
        pass

    def _before_request(self):
        return self.before_request()

    def before_request(self):
        return None

    def _after_request(self, response):
        return self.after_request(response)

    def after_request(self, response):
        return response

    def run_request(self, method, *args, **kwargs):
        return method(*args, **kwargs)

    def dispatch_request(self, *args, **kwargs):
        meth = getattr(self, request.method.lower(), None)

        # use GET method if request method is HEAD and no handler for it
        if meth is None and request.method == "HEAD":
            meth = getattr(self, "get", None)

        if meth is None:
            return self.response_handler(("Method Not Allowed", 405))

        # exec before request handlers
        result = self._before_request()
        if result is not None:
            return self.response_handler(result)

        result = self.run_request(meth, *args, **kwargs)

        # exec after request handlers
        result = self._after_request(result)
        return self.response_handler(result)

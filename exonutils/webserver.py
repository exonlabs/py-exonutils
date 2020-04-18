# -*- coding: utf-8 -*-
"""
    :copyright: 2020, ExonLabs. All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
import os
import sys
import uuid
import logging
try:
    import gevent.monkey; gevent.monkey.patch_all() # noqa
    from gunicorn.app.base import BaseApplication as GunicornBaseApplication
    from gunicorn.glogging import Logger as GunicornLogger
    from gunicorn import util as gunicorn_util
except ImportError:
    GunicornBaseApplication = None
from flask import Flask, request, jsonify
from flask.views import MethodView
from jinja2 import BaseLoader

from .process import BaseProcess
from .misc import shared_buffer

__all__ = ['WebServer', 'RESTWebServer', 'WebView']

DEFAULT_HOST = '0.0.0.0'
DEFAULT_PORT = 8000


class WebServer(BaseProcess):

    def __init__(self, name, options={}, logger=None):
        super(WebServer, self).__init__(name, logger=logger)

        # websrv views list
        self.views = []
        # shared global buffer
        self.shared_buffer = shared_buffer()

        # websrv attrs
        self.options = options
        self.base_path = ''
        self.tpl_loader = None

        # websrv access request logger
        self.rlog = logging.getLogger('%s.requests' % self.log.name)

    def initialize(self):
        self.log.info("Initializing")

        # check gunicorn
        if not self.options.get('simple_engine', False):
            if not GunicornBaseApplication:
                self.log.fatal("please install 'gunicorn','gevent' " +
                               "packages to use gunicorn engine")
                sys.exit(1)

        # check websrv views list
        if not self.views:
            raise RuntimeError("No views loaded !!!")
        for V in self.views:
            if not issubclass(V, WebView):
                raise RuntimeError("Invalid view: %s" % str(V))
        # debug views
        self.log.debug("Loaded views: (%s)"
                       % ','.join([V.__name__ for V in self.views]))

        # adjust request logger handlers
        if not self.rlog.handlers:
            self.rlog.addHandler(logging.StreamHandler(sys.stdout))
        for hnd in self.rlog.handlers:
            hnd.setFormatter(logging.Formatter('%(message)s'))
        self.rlog.setLevel(logging.INFO)
        self.rlog.propagate = False

    def terminate(self):
        if self.options.get('simple_engine', False):
            self.log.info("Shutting down")

    # response handler
    def response_handler(self, response):
        return response

    def create_app(self):
        # create flask app
        app = Flask(
            self.name,
            template_folder=os.path.join(self.base_path, 'templates'),
            static_folder=os.path.join(self.base_path, 'static'))

        # update app config from options
        options = self.options.get('app', {})
        for k, v in options.items():
            app.config[k.upper()] = v

        # check app options
        if not app.config.get('SECRET_KEY', None):
            app.config['SECRET_KEY'] = uuid.uuid5(
                uuid.uuid1(), uuid.uuid4().hex).hex
        if not app.config.get('MAX_CONTENT_LENGTH', None):
            app.config['MAX_CONTENT_LENGTH'] = 10485760  # 10 MiB

        # find referance debug mode
        if self.log.level >= logging.DEBUG:
            debug = bool(self.log.level <= logging.DEBUG)
        else:
            debug = bool(logging.getLogger().level <= logging.DEBUG)

        # force specific app options
        app.config['APP_DEBUG'] = debug
        app.config['TEMPLATES_AUTO_RELOAD'] = True
        app.config['TRAP_HTTP_EXCEPTIONS'] = True
        app.config['TRAP_BAD_REQUEST_ERRORS'] = True

        # set jinja options
        app.jinja_env.autoescape = True
        app.jinja_env.auto_reload = True
        if self.tpl_loader and isinstance(self.tpl_loader, BaseLoader):
            app.jinja_loader = self.tpl_loader

        # register exception handler
        @app.errorhandler(Exception)
        def exception_handler(e):
            if hasattr(e, 'code'):
                return self.response_handler((e.name, e.code))
            else:
                from traceback import format_exc
                self.log.error(format_exc().strip())
                return self.response_handler(("Internal Server Error", 500))

        # load websrv views
        for view in self.views:
            view.initialize(self, app)
            for url, endpoint in view.routes:
                app.add_url_rule(url, view_func=view.as_view(endpoint, self))

        return app

    def run(self):
        if self.options.get('simple_engine', False):
            os.environ['FLASK_ENV'] = 'development'

            # setup werkzeug request logger
            wlogger = logging.getLogger('werkzeug')
            wlogger.parent = self.rlog

            # create werkzeug app
            options = self.options.get('engine', {})
            app = self.create_app()
            app.run(
                host=options.get('host', '') or DEFAULT_HOST,
                port=options.get('port', 0) or DEFAULT_PORT,
                debug=app.config['APP_DEBUG'],
                use_reloader=app.config['APP_DEBUG'])

            return None

        # use gunicorn engine
        error_logger = self.log
        access_logger = self.rlog

        class _Logger(GunicornLogger):
            def __init__(self, *args, **kw):
                super(_Logger, self).__init__(*args, **kw)
                self.error_log = error_logger
                self.access_log = access_logger

        class _App(GunicornBaseApplication):
            def __init__(self, websrv):
                self.websrv = websrv
                super(_App, self).__init__()

            def load_config(self):
                # load engine options
                options = self.websrv.options.get('engine', {})
                options.update({
                    'bind': '%s:%s' % (
                        options.get('host', '') or DEFAULT_HOST,
                        options.get('port', 0) or DEFAULT_PORT),
                    'workers': options.get('workers', 0) or os.cpu_count(),
                    'worker_class': 'gevent',
                    'logger_class': _Logger,
                    'accesslog': '-',
                    'access_log_format':
                        '%(h)s - %(u)s %(t)s "%(r)s" %(s)s ' +
                        '%(b)s "%(f)s" "%(a)s" %(D)s',
                    'max_requests': options.get('max_requests', 0) or 200,
                    'max_requests_jitter':
                        options.get('max_requests_jitter', 0) or 50,
                })
                if self.websrv.proctitle:
                    options['proc_name'] = self.websrv.proctitle.strip()
                    try:
                        from setproctitle import setproctitle
                        gunicorn_util._setproctitle = lambda t: setproctitle(
                            t[8:-1] if 'master' in t else ('%s+' % t[8:-1]))
                    except ImportError:
                        pass

                # set engine options
                for key, value in options.items():
                    if key in self.cfg.settings and value is not None:
                        self.cfg.set(key, value)

            def load(self):
                return self.websrv.create_app()

        # create gunicorn app
        app = _App(self)
        app.run()


class RESTWebServer(WebServer):

    # default response parser is to send JSON data results
    def response_parser(self, data, status):
        return (jsonify(**data), status)

    def response_handler(self, response):
        if type(response) is tuple:
            data, code = response[0], response[1]
        else:
            data, code = response, 200

        if type(data) is dict:
            return self.response_parser(data, code)

        if code >= 400:
            return self.response_parser({'error': data}, code)
        else:
            return self.response_parser({'result': data}, code)


class WebView(MethodView):
    routes = []

    def __init__(self, webserver):
        self.name = self.__class__.__name__
        self.response_handler = webserver.response_handler

        # shared global buffer
        self.shared_buffer = webserver.shared_buffer

        # view logger
        self.log = logging.getLogger(
            '%s.%s' % (webserver.log.name, self.name))
        self.log.name = '%s::%s' % (self.log.parent.name, self.name)

    @classmethod
    def initialize(cls, websrv, app):
        pass

    def _before_request(self):
        return self.before_request()

    def before_request(self):
        return None

    def _after_request(self, response):
        return self.after_request(response)

    def after_request(self, response):
        return response

    def dispatch_request(self, *args, **kw):
        meth = getattr(self, request.method.lower(), None)

        # use GET method if request method is HEAD and no handler for it
        if meth is None and request.method == "HEAD":
            meth = getattr(self, "get", None)

        if meth is None:
            return self.response_handler(("Method Not Allowed", 405))

        # exec before request handlers
        response = self._before_request()
        if response is not None:
            return self.response_handler(response)

        response = meth(*args, **kw)

        # exec after request handlers
        response = self._after_request(response)
        return self.response_handler(response)

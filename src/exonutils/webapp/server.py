# -*- coding: utf-8 -*-
import os
import uuid
import copy
import logging
from flask import Flask
from jinja2 import BaseLoader

from .view import BaseWebView

__all__ = []


class SimpleWebServer(object):

    def __init__(self, name, proctitle='', options={}, logger=None,
                 reqlogger=None, debug=0):
        # web server name
        self.name = name
        # process title to show in os process table
        self.proctitle = proctitle or name
        # debug mode
        self.debug = debug

        # web server config options
        self.options = copy.deepcopy(options)

        # web server logger
        self.log = logger
        # websrv requests logger
        self.reqlog = reqlogger

        self.app = None
        self.base_path = ''
        self.tpl_loader = None

    def initialize(self):
        if not self.log:
            self.log = logging.getLogger(self.name)
        if not self.debug and self.log.level == logging.DEBUG:
            self.debug = 1

        self.log.info("initializing")

        if not self.reqlog:
            self.reqlog = logging.getLogger('%s.requests' % self.name)
        self.reqlog.setLevel(logging.INFO)
        self.reqlog.propagate = False
        if not self.reqlog.handlers:
            self.reqlog.handlers = [logging.NullHandler()]

        if not self.app:
            self.app = self.create_app()

    def add_view(self, view_hnd):
        if not isinstance(view_hnd, BaseWebView):
            raise RuntimeError("INVALID_VIEW - %s" % view_hnd)

        view_hnd.parent = self
        view_hnd.initialize()
        for url, endpoint in view_hnd.routes:
            self.app.add_url_rule(
                url, endpoint=endpoint,
                view_func=view_hnd.dispatch_request,
                methods=view_hnd.methods)

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
                return e.name, e.code
            else:
                self.log.error(str(e), exc_info=bool(self.debug))
                return "Internal Server Error", 500

        return app

    def start(self, host, port, **kwargs):
        # adjust request logs
        if self.reqlog:
            logging.getLogger('werkzeug').parent = self.reqlog

        # store root process PID
        self.app.config['ROOT_PID'] = os.getpid()

        # set daemon process title
        if self.proctitle:
            try:
                from setproctitle import setproctitle
                setproctitle(str(self.proctitle).strip().lower())
            except ImportError:
                self.log.debug("ignoring setting proctitle")

        self.app.run(host=host, port=port, **kwargs)

    def stop(self):
        import signal

        pid = self.app.config.get('ROOT_PID')
        if pid:
            self.log.info("stop request")
            os.kill(pid, signal.SIGTERM)

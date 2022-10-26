# -*- coding: utf-8 -*-
import logging
from flask import request

__all__ = []


class BaseWebView(object):
    # list of tuples: [(url, endpoint), ...]
    routes = []
    # allowed methods for view
    methods = ['GET', 'POST']

    def __init__(self, name=None, logger=None):
        # view name
        self.name = name if name else self.__class__.__name__
        # view parent handler
        self.parent = None
        # view logger
        self.log = logger
        # debug mode
        self.debug = 0

    def initialize(self):
        if not self.parent:
            raise RuntimeError(
                "INVALID_PARAMS - no parent handler defined")

        if not self.log:
            self.log = logging.getLogger(self.name)
            self.log.parent = self.parent.log
            self.log.level = self.parent.log.level
        if not self.debug and self.log.level == logging.DEBUG:
            self.debug = 1

        self.log.debug("initializing")

    def dispatch_request(self, *args, **kwargs):
        # exec before request handlers
        if hasattr(self, 'before_request'):
            response = self.before_request(*args, **kwargs)
            if response is not None:
                return response

        # dispatch request
        response = self.handle_request(
            request.method.lower(), *args, **kwargs)

        # exec after request handlers
        if hasattr(self, 'after_request'):
            return self.after_request(response, *args, **kwargs)

        return response

    def handle_request(self, method, *args, **kwargs):
        if not hasattr(self, method):
            # use GET method instead of HEAD if not implemented
            if method == 'head' and hasattr(self, 'get'):
                method = 'get'
            else:
                return "Method Not Allowed", 405

        return getattr(self, method)(*args, **kwargs)

    # def before_request(self, *args, **kwargs):
    #     return None

    # def after_request(self, response, *args, **kwargs):
    #     return response

    # def head(self, *args, **kwargs):
    #     raise NotImplementedError()

    # def get(self, *args, **kwargs):
    #     raise NotImplementedError()

    # def post(self, *args, **kwargs):
    #     raise NotImplementedError()

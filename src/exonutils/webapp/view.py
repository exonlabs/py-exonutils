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

    def before_request(self, *args, **kwargs):
        return None

    def after_request(self, response, *args, **kwargs):
        return response

    def handle_request(self, *args, **kwargs):
        # exec before request handlers
        response = self.before_request(*args, **kwargs)
        if response is not None:
            return response

        # handle request method
        try:
            method = request.method.lower()
            response = getattr(self, method)(*args, **kwargs)
        except (AttributeError, NotImplementedError):
            return "Method Not Allowed", 405

        # exec after request handlers
        return self.after_request(response, *args, **kwargs)

    # default redirect for GET method if not implemented
    def head(self, *args, **kwargs):
        return self.get(*args, **kwargs)

    def get(self, *args, **kwargs):
        raise NotImplementedError()

    def post(self, *args, **kwargs):
        raise NotImplementedError()

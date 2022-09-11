# -*- coding: utf-8 -*-

__all__ = []


class BaseEngine(object):

    def backend_name(self):
        raise NotImplementedError()

    def session_factory(self):
        raise NotImplementedError()

    def table_schema(self, model, **kwargs):
        raise NotImplementedError()

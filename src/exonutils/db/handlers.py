# -*- coding: utf-8 -*-
import copy

__all__ = []


class BaseDBHandler(object):

    def __init__(self, options={}):
        self.options = copy.deepcopy(options)
        self.logger = None
        self.backend = ''

        # set default session params
        if not self.options.get("connect_timeout"):
            self.options["connect_timeout"] = 30
        if not self.options.get("retries"):
            self.options["retries"] = 10
        if not self.options.get("retry_delay"):
            self.options["retry_delay"] = 0.5

        # set sql statement placeholder
        if not self.options.get("sql_placeholder"):
            self.options["sql_placeholder"] = "$?"

    # get new session handler
    def session(self):
        raise NotImplementedError()

    # create database tables and initialize table data
    def init_database(self, models, **kwargs):
        with self.session() as dbs:
            # build database schema
            for model in models:
                model.create_schema(dbs, **kwargs)

            # initialize models data
            for model in models:
                model.initialize_data(dbs, **kwargs)

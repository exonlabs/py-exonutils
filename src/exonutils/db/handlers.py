# -*- coding: utf-8 -*-
import copy

from .session import Session

__all__ = []


class DBHandler(object):

    def __init__(self, engine, options={}):
        self.options = copy.deepcopy(options)
        self.logger = None

        # database backend engine
        self.engine = engine

        # set default options
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
        return Session(self)

    # create database tables and initialize table data
    def init_database(self, models, **kwargs):
        with self.session() as dbs:
            # build database schema
            dbs.begin()
            for model in models:
                for sql in self.engine.table_schema(model, **kwargs):
                    dbs.execute(sql)
                model.upgrade_schema(dbs, **kwargs)
            dbs.commit()

            # initialize models data
            for model in models:
                model.initialize_data(dbs, **kwargs)

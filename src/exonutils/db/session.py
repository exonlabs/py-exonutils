# -*- coding: utf-8 -*-
import re
import logging

__all__ = []


class BaseSession(object):

    def __init__(self, dbh):
        self.dbh = dbh

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def query(self, model, **kwargs):
        raise NotImplementedError()

    def is_connected(self):
        raise NotImplementedError()

    def in_transaction(self):
        raise NotImplementedError()

    def connect(self):
        raise NotImplementedError()

    def close(self):
        raise NotImplementedError()

    def execute(self, sql, params=None):
        raise NotImplementedError()

    def fetchall(self, sql, params=None):
        raise NotImplementedError()

    def rowsaffected(self):
        raise NotImplementedError()

    def lastinsertid(self):
        raise NotImplementedError()

    def begin(self):
        raise NotImplementedError()

    def commit(self):
        raise NotImplementedError()

    def rollback(self):
        raise NotImplementedError()

    # format and log sql query
    def log_sql(self, sql, params=None):
        if self.dbh.logger and self.dbh.logger.level == logging.DEBUG:
            # clean extra newlines with spaces
            sql = re.sub('\n\\s+', '\n', sql).strip()
            if params:
                self.dbh.logger.debug(
                    "SQL:\n---\n%s\nPARAMS: %s\n---" % (sql, params))
            else:
                self.dbh.logger.debug(
                    "SQL:\n---\n%s\n---" % (sql))

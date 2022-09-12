# -*- coding: utf-8 -*-
import re
import time
import logging

from .query import Query

__all__ = []


class Session(object):

    def __init__(self, dbh):
        self.dbh = dbh

        # db connection handler
        self._conn = None
        self._cur = None
        self._in_transaction = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    # shorthand to create query instance
    def __call__(self, model, **kwargs):
        return Query(self, model, **kwargs)

    def query(self, model, **kwargs):
        return Query(self, model, **kwargs)

    def is_connected(self):
        return bool(self._conn)

    def in_transaction(self):
        return bool(self._in_transaction)

    def connect(self):
        if not self._conn:
            if self.dbh.logger:
                self.dbh.logger.debug(
                    "(%s) - connect" % self.dbh.options.get('database'))

            self._conn = self.dbh.engine.connection(self.dbh.options)
            self._cur = self._conn.cursor()
            self._in_transaction = False

    def close(self):
        if self._conn:
            if self.dbh.logger:
                self.dbh.logger.debug(
                    "(%s) - close" % self.dbh.options.get('database'))

            self._conn.close()

        self._conn = None
        self._cur = None
        self._in_transaction = False

    def execute(self, sql, params=None):
        self.connect()

        sql = sql.replace(
            self.dbh.options['sql_placeholder'],
            self.dbh.engine.sql_placeholder)
        self.log_sql(sql, params=params)

        err = ""
        for i in range(self.dbh.options['retries']):
            try:
                if params:
                    self._cur.execute(sql, params)
                else:
                    self._cur.execute(sql)
                return
            except self.dbh.engine.DatabaseError as e:
                err = str(e)
                break
            except (RuntimeError, ValueError):
                raise
            except Exception as e:
                err = str(e)

            time.sleep(self.dbh.options['retry_delay'])

        raise RuntimeError(err)

    def fetchall(self, sql, params=None):
        self.execute(sql, params=params)
        return self._cur.fetchall()

    def rowsaffected(self):
        if self._cur:
            return self._cur.rowcount
        return 0

    def begin(self):
        if not self._in_transaction:
            self.execute("BEGIN;")
            self._in_transaction = True

    def commit(self):
        if self.dbh.logger:
            self.dbh.logger.debug(
                "(%s) - commit" % self.dbh.options.get('database'))

        self._conn.commit()
        self._in_transaction = False

    def rollback(self):
        if self.dbh.logger:
            self.dbh.logger.debug(
                "(%s) - rollback" % self.dbh.options.get('database'))

        self._conn.rollback()
        self._in_transaction = False

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

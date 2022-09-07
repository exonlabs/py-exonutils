# -*- coding: utf-8 -*-
import time
import sqlite3

from exonutils.db.session import BaseSession

from .query import Query

__all__ = []


class Session(BaseSession):

    def __init__(self, *args, **kwargs):
        super(Session, self).__init__(*args, **kwargs)

        if not self.dbh.options.get('database'):
            raise ValueError("invalid database configuration")

        self._conn = None
        self._cur = None

    def query(self, model, **kwargs):
        return Query(self, model, **kwargs)

    def is_connected(self):
        return bool(self._conn and self._cur)

    def in_transaction(self):
        if self._conn:
            return bool(self._conn.in_transaction)
        return False

    def connect(self):
        if not self._conn:
            if self.dbh.logger:
                self.dbh.logger.debug(
                    "(%s) - connect" % self.dbh.options['database'])

            self._cur = None

            self._conn = sqlite3.connect(
                self.dbh.options['database'],
                timeout=self.dbh.options['connect_timeout'],
                detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)

            self._conn.isolation_level = \
                self.dbh.options.get('isolation_level', None)
            self._conn.row_factory = lambda cur, row: {
                col[0]: row[idx] for idx, col in enumerate(cur.description)}

        if not self._cur:
            self._cur = self._conn.cursor()
            if self.dbh.options.get('foreign_keys_constraints', True):
                self._cur.execute('PRAGMA foreign_keys=ON')

    def close(self):
        if self._conn:
            if self.dbh.logger:
                self.dbh.logger.debug(
                    "(%s) - close" % self.dbh.options['database'])
            self._conn.close()

        self._conn = None
        self._cur = None

    def execute(self, sql, params=None):
        self.connect()

        sql = sql.replace(self.dbh.options['sql_placeholder'], "?")
        self.log_sql(sql, params=params)

        err = ""
        for i in range(self.dbh.options['retries']):
            try:
                if params:
                    self._cur.execute(sql, params)
                else:
                    self._cur.execute(sql)
                return
            except (RuntimeError, ValueError):
                raise
            except (sqlite3.NotSupportedError, sqlite3.IntegrityError,
                    sqlite3.ProgrammingError, sqlite3.OperationalError) as e:
                err = str(e)
                break
            except Exception as e:
                err = str(e)

            time.sleep(self.dbh.options['retry_delay'])

        raise RuntimeError(err)

    def executescript(self, sql_script):
        self.connect()

        self.sql_log(sql_script)

        err = ""
        for i in range(self.dbh.options['retries']):
            try:
                self._cur.executescript(sql_script)
                return
            except (RuntimeError, ValueError):
                raise
            except (sqlite3.NotSupportedError, sqlite3.IntegrityError,
                    sqlite3.ProgrammingError, sqlite3.OperationalError) as e:
                err = str(e)
                break
            except Exception as e:
                err = str(e)

            time.sleep(self.dbh.options['retry_delay'])

        raise RuntimeError(err)

    def fetchall(self, sql, params=None):
        self.execute(sql, params=params)
        return self._cur.fetchall()

    def fetchone(self, sql, params=None):
        self.execute(sql, params=params)
        return self._cur.fetchone()

    def fetchmany(self, sql, params=None, size=10):
        self.execute(sql, params=params)
        return self._cur.fetchmany(size=size)

    def rowsaffected(self):
        return self._cur.rowcount

    def lastinsertid(self):
        return self._cur.lastrowid

    def begin(self):
        if not self.in_transaction():
            self.execute("BEGIN;")

    def commit(self):
        if self.dbh.logger:
            self.dbh.logger.debug(
                "(%s) - commit" % self.dbh.options['database'])

        self._conn.commit()

    def rollback(self):
        if self.dbh.logger:
            self.dbh.logger.debug(
                "(%s) - rollback" % self.dbh.options['database'])

        self._conn.rollback()

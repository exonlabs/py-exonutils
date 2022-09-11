# -*- coding: utf-8 -*-
import time
import sqlite3 as sqlite

from exonutils.db.session import BaseSession

__all__ = []


class Session(BaseSession):

    def _connect(self):
        if not self.dbh.options.get('database'):
            raise ValueError("invalid database configuration")

        self._conn = sqlite.connect(
            self.dbh.options['database'],
            timeout=self.dbh.options['connect_timeout'],
            detect_types=sqlite.PARSE_DECLTYPES | sqlite.PARSE_COLNAMES)

        self._conn.isolation_level = \
            self.dbh.options.get('isolation_level', None)
        self._conn.row_factory = lambda cur, row: {
            col[0]: row[idx] for idx, col in enumerate(cur.description)}

        self._cur = self._conn.cursor()

        # post connect init
        if self.dbh.options.get('foreign_keys_constraints', True):
            self._cur.execute('PRAGMA foreign_keys=ON')

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
            except (sqlite.NotSupportedError, sqlite.IntegrityError,
                    sqlite.ProgrammingError, sqlite.OperationalError) as e:
                err = str(e)
                break
            except Exception as e:
                err = str(e)

            time.sleep(self.dbh.options['retry_delay'])

        raise RuntimeError(err)

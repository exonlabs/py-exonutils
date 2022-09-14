# -*- coding: utf-8 -*-
try:
    import MySQLdb as pysql
except ImportError:
    raise RuntimeError("backend package `mysqlclient` not installed")
from MySQLdb.cursors import DictCursor

from exonutils.db.engine import BaseEngine
from exonutils.db.common import sql_identifier

__all__ = []


class Engine(BaseEngine):

    backend = "mysql"

    sql_placeholder = '%s'

    Error = pysql.Error
    InterfaceError = pysql.InterfaceError
    DatabaseError = pysql.DatabaseError
    DataError = pysql.DataError
    OperationalError = pysql.OperationalError
    IntegrityError = pysql.IntegrityError
    InternalError = pysql.InternalError
    ProgrammingError = pysql.ProgrammingError
    NotSupportedError = pysql.NotSupportedError

    def connection(self, options):
        for k in ['database', 'host', 'port', 'username', 'password']:
            if not options.get(k):
                raise ValueError("invalid database configuration")

        conn = pysql.connect(
            database=options['database'],
            host=options['host'],
            port=options['port'],
            user=options['username'],
            password=options['password'],
            charset='utf8mb4',
            use_unicode=True,
            cursorclass=DictCursor,
            connect_timeout=options.get('connect_timeout') or 30)

        return conn

    def post_connect(self, conn, options):
        if options.get('foreign_keys_constraints', True):
            conn.cursor().execute('SET foreign_key_checks=1')

    def table_schema(self, model, **kwargs):
        # tblargs = model.table_args()

        tblname = sql_identifier(
            kwargs.get("table_name") or model.table_name())

        tblcolumns = model.table_columns()
        if tblcolumns[0][0] != "guid":
            tblcolumns.insert(
                0, ("guid", "VARCHAR(32) NOT NULL", "PRIMARY"))

        expr, constraints, indexes = [], [], []
        for c in tblcolumns:
            expr.append('%s %s' % (sql_identifier(c[0]), c[1]))

            if 'BOOLEAN' in c[1]:
                constraints.append('CHECK (%s IN (0,1))' % c[0])

            if len(c) <= 2:
                continue

            if 'PRIMARY' in c[2]:
                constraints.append('PRIMARY KEY (%s)' % c[0])
            elif 'UNIQUE' in c[2] and 'INDEX' not in c[2]:
                constraints.append('UNIQUE (%s)' % c[0])

            if 'PRIMARY' in c[2] or 'INDEX' in c[2]:
                u = 'UNIQUE ' if 'PRIMARY' in c[2] or 'UNIQUE' in c[2] else ''
                indexes.append(
                    'CREATE %sINDEX IF NOT EXISTS ' % u +
                    'ix_%s_%s ' % (tblname, c[0]) +
                    'ON %s (%s);' % (tblname, c[0]))

        expr.extend(constraints)
        expr.extend(model.table_constraints())

        stmt = 'CREATE TABLE IF NOT EXISTS %s (\n' % tblname
        stmt += ',\n'.join(expr)
        stmt += '\n);\n'

        result = [stmt]
        result.extend(indexes)
        return result

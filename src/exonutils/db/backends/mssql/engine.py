# -*- coding: utf-8 -*-
try:
    import pymssql as pysql
except ImportError:
    raise RuntimeError("backend package `pymssql` not installed")

from exonutils.db.engine import BaseEngine
from exonutils.db.common import sql_identifier

__all__ = []


class Engine(BaseEngine):

    backend = "mssql"

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
            charset='utf8',
            as_dict=True,
            login_timeout=options.get('connect_timeout') or 30,
            timeout=options.get('connect_timeout') or 30)

        return conn

    def post_connect(self, conn, options):
        pass

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
            if 'BOOLEAN' in c[1]:
                expr.append('%s %s' % (
                    sql_identifier(c[0]), c[1].replace('BOOLEAN', 'BIT')))
                constraints.append("CHECK (%s IN (0,1))" % c[0])
            else:
                expr.append('%s %s' % (sql_identifier(c[0]), c[1]))

            if len(c) <= 2:
                continue

            if 'PRIMARY' in c[2]:
                constraints.append('PRIMARY KEY (%s)' % c[0])
            elif 'UNIQUE' in c[2] and 'INDEX' not in c[2]:
                constraints.append('UNIQUE (%s)' % c[0])

            if 'PRIMARY' in c[2] or 'INDEX' in c[2]:
                u = 'UNIQUE ' if 'PRIMARY' in c[2] or 'UNIQUE' in c[2] else ''
                indexes.append(
                    "IF NOT EXISTS (SELECT * FROM sys.indexes " +
                    "WHERE name='ix_%s_%s')\n" % (tblname, c[0]) +
                    "CREATE %sINDEX " % u +
                    "ix_%s_%s " % (tblname, c[0]) +
                    "ON %s (%s);" % (tblname, c[0]))

        expr.extend(constraints)
        expr.extend(model.table_constraints())

        stmt = "IF OBJECT_ID(N'%s', N'U') IS NULL\n" % tblname
        stmt += "CREATE TABLE %s (\n" % tblname
        stmt += ",\n".join(expr)
        stmt += "\n);"

        result = [stmt]
        result.extend(indexes)
        return result

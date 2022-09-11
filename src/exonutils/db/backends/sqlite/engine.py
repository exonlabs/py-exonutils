# -*- coding: utf-8 -*-
from exonutils.db.engine import BaseEngine
from exonutils.db.common import sql_identifier

from .session import Session
from .adapters import register_adapters

__all__ = []


class Engine(BaseEngine):

    def __init__(self):
        register_adapters()

    def backend_name(self):
        return "sqlite"

    def session_factory(self):
        return Session

    # columns:
    #   [(colname, definition [, constraint]), ...]
    # example:
    #   [('col1', 'TEXT NOT NULL', 'INDEX UNIQUE'), ...]

    # constraints
    # example:
    #   ['CHECK (col1 IN (0, 1))',
    #    'FOREIGN KEY (tbl1_id) REFERENCES tbl1 (tbl1_id)', ...]

    def table_schema(self, model, **kwargs):
        tblargs = model.table_args()

        tblname = sql_identifier(
            kwargs.get("table_name") or model.table_name())

        tblcolumns = model.table_columns()
        if tblcolumns[0][0] != "guid":
            tblcolumns.insert(
                0, ("guid", "TEXT NOT NULL", "PRIMARY"))

        expr, constraints, indexes = [], [], []
        for c in tblcolumns:
            expr.append('"%s" %s' % (sql_identifier(c[0]), c[1]))

            if 'BOOLEAN' in c[1]:
                constraints.append('CHECK ("%s" IN (0,1))' % c[0])

            if len(c) <= 2:
                continue

            if 'PRIMARY' in c[2]:
                constraints.append('PRIMARY KEY ("%s")' % c[0])
            elif 'UNIQUE' in c[2] and 'INDEX' not in c[2]:
                constraints.append('UNIQUE ("%s")' % c[0])

            if 'PRIMARY' in c[2] or 'INDEX' in c[2]:
                u = 'UNIQUE ' if 'PRIMARY' in c[2] or 'UNIQUE' in c[2] else ''
                indexes.append(
                    'CREATE %sINDEX IF NOT EXISTS ' % u +
                    '"ix_%s_%s" ' % (tblname, c[0]) +
                    'ON "%s" ("%s");' % (tblname, c[0]))

        expr.extend(constraints)
        expr.extend(model.table_constraints())

        sql = 'CREATE TABLE IF NOT EXISTS "%s" (\n' % tblname
        sql += ',\n'.join(expr)
        if tblargs.get('sqlite_without_rowid', True):
            sql += '\n) WITHOUT ROWID;\n'
        else:
            sql += '\n);\n'

        result = [sql]
        result.extend(indexes)
        return result

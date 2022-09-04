# -*- coding: utf-8 -*-
from exonutils.db.common import sql_identifier
from exonutils.db.query import BaseQuery

__all__ = []


class Query(BaseQuery):

    # columns:
    #   [(colname, definition [, constraint]), ...]
    # example:
    #   [('col1', 'TEXT NOT NULL', 'INDEX UNIQUE'), ...]

    # constraints
    # example:
    #   ['CHECK (col1 IN (0, 1))',
    #    'FOREIGN KEY (tbl1_id) REFERENCES tbl1 (tbl1_id)', ...]

    def create_schema(self):
        tblargs = self.model.table_args()

        columns = self.model.table_columns()
        if columns[0][0] != "guid":
            columns.insert(0, ('guid', 'TEXT NOT NULL', 'PRIMARY'))

        expr, constraints, indexes = [], [], []
        for c in columns:
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
                    '"ix_%s_%s" ' % (self.table_name, c[0]) +
                    'ON "%s" ("%s");' % (self.table_name, c[0]))

        expr.extend(constraints)
        expr.extend(self.model.table_constraints())

        self.dbs.begin()

        # create table
        sql = 'CREATE TABLE IF NOT EXISTS "%s" (\n' % self.table_name
        sql += ',\n'.join(expr)
        if tblargs.get('without_rowid', True):
            sql += '\n) WITHOUT ROWID;\n'
        else:
            sql += '\n);\n'
        self.dbs.execute(sql)

        # create indexes
        for sql in indexes:
            self.dbs.execute(sql)

        self.dbs.commit()

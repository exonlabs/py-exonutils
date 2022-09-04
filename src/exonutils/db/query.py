# -*- coding: utf-8 -*-
from .common import generate_guid, sql_identifier, data_mapping

__all__ = []


class BaseQuery(object):

    def __init__(self, dbs, model, **kwargs):
        self.dbs = dbs
        self.model = model

        # set runtime table name to use, this allows for mapping
        # same model to multiple tables
        self.table_name = \
            kwargs.get("table_name") or self.model.table_name()

        self._columns = []
        self._filters = []
        self._execargs = []
        self._groupby = []
        self._orderby = []
        self._having = ""
        self._limit = 0
        self._offset = 0

    # set columns to retreive
    def columns(self, *columns):
        self._columns = [sql_identifier(v) for v in columns]
        return self

    # add query filters
    def filter(self, expr, *params):
        self._filters.append(expr)
        self._execargs.extend(params)
        return self

    # add query filters
    def filterby(self, column, value):
        cond = "AND " if self._filters else ""
        self._filters.append("%s%s=%s" % (
            cond, sql_identifier(column),
            self.dbs.options['sql_placeholder']))
        self._execargs.append(value)
        return self

    # set grouping
    def groupby(self, *groupby):
        self._groupby = [sql_identifier(v) for v in groupby]
        return self

    # set ordering: "colname ASC|DESC"
    def orderby(self, *orderby):
        self._orderby = []
        for val in orderby:
            v = val.split(" ")
            if len(v) < 2:
                raise ValueError("invalid query ordering: %s" % val)
            v[1] = v[1].upper()
            if v[1] not in ['ASC', 'DESC']:
                raise ValueError("invalid query ordering: %s" % val)
            self._orderby.append("%s %s" % (sql_identifier(v[0]), v[1]))
        return self

    # add having expr
    def having(self, expr, param):
        self._having = expr
        self._execargs.append(param)
        return self

    # add limit
    def limit(self, limit):
        self._limit = int(limit)
        return self

    # add offset
    def offset(self, offset):
        self._offset = int(offset)
        return self

    # return all elements matching filter params
    def all(self):
        q = "SELECT %s FROM %s" % (
            ", ".join(self._columns) if self._columns else "*",
            sql_identifier(self.table_name))

        if self._filters:
            q += "\nWHERE %s" % (" ".join(self._filters))
        if self._groupby:
            q += "\nGROUP BY %s" % (", ".join(self._groupby))
        if self._having:
            q += "\nHAVING %s" % self._having
        if self._orderby:
            q += "\nORDER BY %s" % (", ".join(self._orderby))
        if self._limit > 0:
            q += "\nLIMIT %s" % int(self._limit)
        if self._offset > 0:
            q += "\nOFFSET %s" % int(self._offset)
        q += ";"

        result = []
        for data in self.dbs.fetchall(q, params=self._execargs):
            result.append(
                data_mapping(self.model.data_converters(), data))

        return result

    # return first element matching filter params or None
    def first(self):
        self._limit, self._offset = 1, 0
        result = self.all()
        if result:
            return result[0]
        return None

    # return one element matching filter params or None
    # there must be only one element or none
    def one(self):
        self._limit, self._offset = 2, 0
        result = self.all()
        if result:
            if len(result) > 1:
                raise ValueError("multiple entries found")
            return result[0]
        return None

    def get(self, guid):
        self._filters = ["guid=%s" % self.dbs.options['sql_placeholder']]
        self._execargs = [guid]
        self._groupby, self._orderby, self._having = [], [], ""
        return self.one()

    def count(self):
        q = "SELECT count(*) as count FROM %s" % (
            sql_identifier(self.table_name))

        if self._filters:
            q += "\nWHERE %s" % (" ".join(self._filters))
        if self._groupby:
            q += "\nGROUP BY %s" % (", ".join(self._groupby))
        q += ";"

        result = self.dbs.fetchall(q, params=self._execargs)
        return int(result[0]['count'])

    def insert(self, data):
        if type(data) is not dict:
            raise ValueError("invalid data type")

        data = data_mapping(self.model.data_adapters(), data)
        if 'guid' in data:
            guid = data['guid']
            del(data['guid'])
        else:
            guid = generate_guid()

        columns, params = ['guid'], [guid]
        for k, v in data.items():
            columns.append(sql_identifier(k))
            params.append(v)

        q = "INSERT INTO %s" % self.table_name
        q += "\n(%s)" % (", ".join(columns))
        q += "\nVALUES"
        q += "\n(%s)" % (", ".join(
            [self.dbs.options['sql_placeholder']] * len(columns)))
        q += ";"

        self.dbs.execute(q, params=params)
        if not self.dbs.in_transaction():
            self.dbs.commit()

        return guid

    def update(self, data):
        if type(data) is not dict:
            raise ValueError("invalid data type")

        data = data_mapping(self.model.data_adapters(), data)
        if 'guid' in data:
            del(data['guid'])

        columns, params = [], []
        for k, v in data.items():
            if type(v) is str and 'CASE' in v:
                columns.append('%s=%s' % (sql_identifier(k), v))
            else:
                columns.append('%s=%s' % (
                    sql_identifier(k), self.dbs.options['sql_placeholder']))
                params.append(v)

        params.extend(self._execargs)

        q = "UPDATE %s" % self.table_name
        q += "\nSET %s" % ", ".join(columns)
        if self._filters:
            q += "\nWHERE %s" % (" ".join(self._filters))
        q += ";"

        self.dbs.execute(q, params=params)
        if not self.dbs.in_transaction():
            self.dbs.commit()

        return self.dbs.rowsaffected()

    def delete(self):
        q = "DELETE FROM %s" % self.table_name
        if self._filters:
            q += "\nWHERE %s" % (" ".join(self._filters))
        q += ";"

        self.dbs.execute(q, params=self._execargs)
        if not self.dbs.in_transaction():
            self.dbs.commit()

        return self.dbs.rowsaffected()

    def create_schema(self):
        raise NotImplementedError()

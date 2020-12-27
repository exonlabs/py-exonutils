# -*- coding: utf-8 -*-
"""
    :copyright: 2021, ExonLabs. All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
import re
import logging
import sqlite3

__all__ = ['BaseModel', 'DatabaseHandler']

_logger = logging.getLogger('sqlitedb')


def init_db_logging(debug=0):
    global _logger
    if debug >= 5:
        _logger.setLevel(logging.DEBUG)
    elif debug >= 4:
        _logger.setLevel(logging.INFO)
    else:
        _logger.setLevel(logging.ERROR)


class BaseModel(object):
    __tablename__ = None
    __columns__ = []

    def __init__(self, data):
        self.__data__ = data

    def __getattr__(self, attr):
        return self.__data__[attr]

    def __repr__(self):
        attrs = self.__columns__[1:]
        return "%s(%s)" % (
            self.__class__.__name__,
            ', '.join(['%s=%s' % (a, self.__data__[a]) for a in attrs]))

    @classmethod
    def default_orders(cls):
        if len(cls.__columns__) >= 2:
            return '%s ASC' % cls.__columns__[1]
        return None

    @classmethod
    def get(cls, dbs, guid):
        return dbs.query(cls).filter_by(guid=guid).one_or_none()

    @classmethod
    def find(cls, dbs, filters, orders=None, limit=-1, offset=0):
        q = dbs.query(cls)
        if filters:
            q = q.filter(filters)
        orders = orders or cls.default_orders()
        if orders:
            q = q.order_by(orders)
        return q.limit(limit).offset(offset).all() or []

    @classmethod
    def find_one(cls, dbs, filters):
        q = dbs.query(cls)
        if filters:
            q = q.filter(filters)
        return q.one_or_none()

    @classmethod
    def count(cls, dbs, filters):
        q = dbs.query(cls)
        if filters:
            q = q.filter(filters)
        return q.count()

    @classmethod
    def initial_data(cls, dbs):
        # Usage:
        # cls.create(dbs, ...)
        pass

    @classmethod
    def migrate(cls, dbs):
        pass


class _Query(object):

    def __init__(self, dbs, model):
        self.dbs = dbs
        self.model = model

        self._filters = None
        self._filterparams = None
        self._groupby = None
        self._orderby = None
        self._limit = None
        self._offset = None

    def filter(self, filters):
        if type(filters) is str:
            self._filters = filters
        elif type(filters) is list:
            self._filters = filters[0]
            self._filterparams = filters[1]
        else:
            raise RuntimeError("unsupported filters type")
        return self

    def filter_by(self, **kwargs):
        self._filters = ' AND '.join([
            '%s=:%s' % (k, k) for k in kwargs.keys()])
        self._filterparams = kwargs
        return self

    def group_by(self, groupby):
        self._groupby = groupby
        return self

    def order_by(self, orderby):
        self._orderby = orderby
        return self

    def limit(self, limit):
        self._limit = limit
        return self

    def offset(self, offset):
        self._offset = offset
        return self

    def all(self):
        q = "SELECT * FROM %s" % self.model.__tablename__
        if self._filters:
            q += "\nWHERE %s" % self._filters
        if self._groupby:
            q += "\nGROUP BY %s" % self._groupby
        if self._orderby:
            q += '\nORDER BY %s' % self._orderby
        if self._limit:
            q += '\nLIMIT %s' % self._limit
        if self._offset:
            q += '\nOFFSET %s' % self._offset
        q += ";"

        res = self.dbs.run(q, params=self._filterparams)
        if res:
            return [self.model(d) for d in res]

        return None

    def first(self):
        q = "SELECT * FROM %s" % self.model.__tablename__
        if self._filters:
            q += "\nWHERE %s" % self._filters
        if self._groupby:
            q += "\nGROUP BY %s" % self._groupby
        if self._orderby:
            q += '\nORDER BY %s' % self._orderby
        q += '\nLIMIT 1;'

        res = self.dbs.run(q, params=self._filterparams)
        if res:
            return self.model(res[0])

        return None

    def one(self):
        res = self.one_or_none()
        if res:
            return res

        raise RuntimeError("no results found")

    def one_or_none(self):
        q = "SELECT * FROM %s" % self.model.__tablename__
        if self._filters:
            q += "\nWHERE %s" % self._filters
        if self._groupby:
            q += "\nGROUP BY %s" % self._groupby
        if self._orderby:
            q += '\nORDER BY %s' % self._orderby
        q += '\nLIMIT 10;'

        res = self.dbs.run(q, params=self._filterparams)
        if res:
            if len(res) > 1:
                raise RuntimeError("multiple entries found")
            return self.model(res[0])

        return None

    def count(self):
        q = "SELECT count(*) as count FROM %s" % self.model.__tablename__
        if self._filters:
            q += "\nWHERE %s" % self._filters
        if self._groupby:
            q += "\nGROUP BY %s" % self._groupby
        q += ";"

        res = self.dbs.run(q, params=self._filterparams)
        if res:
            return res[0]['count']

        return 0


class _Session(object):

    connect_timeout = 30

    def __init__(self, database, debug=0):
        self.debug = debug
        self.database = database
        self.connection = None
        self.cursor = None

    def connect(self):
        global _logger
        _logger.debug("open connection [%s]" % self.database)
        self.connection = sqlite3.connect(
            self.database,
            timeout=self.connect_timeout,
            detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        self.connection.isolation_level = None
        self.connection.row_factory = sqlite3.Row

    def close(self):
        global _logger
        if self.connection:
            _logger.debug("close connection [%s]" % self.database)
            self.connection.close()
        self.connection = None

    def query(self, model):
        return _Query(self, model)

    def run(self, sql, params=None):
        global _logger

        if not self.connection:
            self.connect()

        # clean extra newlines with spaces
        sql = re.sub('\n\\s+', '\n', sql).strip()
        _logger.info("SQL:\n%s\nPARAMS: %s" % (sql, params))

        self.cursor = self.connection.cursor()
        if params:
            self.cursor.execute(sql, params)
        else:
            self.cursor.execute(sql)
        if sql.strip()[:6].upper() == 'SELECT':
            return self.cursor.fetchall()
        else:
            self.cursor.connection.commit()
            return True


class DatabaseHandler(object):

    def __init__(self, database, debug=0):
        self.debug = debug
        self.database = database
        self.session = None

    def __enter__(self):
        return self.create_session()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_session()

    def create_session(self):
        self.session = _Session(self.database, debug=self.debug)
        return self.session

    def close_session(self):
        if self.session:
            self.session.close()
        self.session = None


def init_database(dbh, models):
    with dbh as dbs:
        pass

        # # create database structure
        # for Model in models:
        #     Model.create_table(dbh)

        # # execute migrations
        # for Model in models:
        #     Model.migrate(dbh)

        # # load initial models data
        # for Model in models:
        #     Model.initial_data(dbh)

    return True


def interactive_db_config(backends=None, defaults={}):
    from .console import ConsoleInput as Input

    default_database = defaults.get('database', None)

    cfg = {}
    cfg['database'] = Input.get(
        "Enter db path", default=default_database, required=True)

    return cfg


def interactive_db_setup(cfg=None, defaults={}, quiet=False):
    if not cfg:
        cfg = interactive_db_config(defaults=defaults)

    database = cfg.get('database', '')
    if not database:
        raise RuntimeError("empty database name")

    # create db file
    open(database, 'a').close()

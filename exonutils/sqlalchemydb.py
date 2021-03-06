# -*- coding: utf-8 -*-
"""
    :copyright: 2021, ExonLabs. All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
import uuid
import logging
import sqlalchemy as sa
from sqlalchemy.ext.declarative import as_declarative

__all__ = []


@as_declarative()
class BaseModel(object):
    __tablename__ = ''
    __table_args__ = {
        'mysql_engine': 'InnoDB',
    }

    guid = sa.Column(
        sa.String(32), primary_key=True, index=True, unique=True,
        autoincrement=False, nullable=False)

    def __repr__(self):
        attrs = self.__mapper__.columns.keys()[1:]
        return "%s(%s)" % (
            self.__class__.__name__,
            ', '.join(['%s=%s' % (a, getattr(self, a)) for a in attrs]))

    @classmethod
    def _orders(cls):
        # return tuple (cls.COLUMN.asc(), ...)
        cols = cls.__mapper__.columns.values()[1:]
        if cols:
            return (cols[0].asc(),)
        return None

    def modify(self, dbs, data, commit=True):
        if 'guid' in data.keys():
            del(data['guid'])
        for attr, value in data.items():
            setattr(self, attr, value)
        dbs.add(self)
        if commit:
            dbs.commit()
        return True

    def remove(self, dbs, commit=True):
        dbs.delete(self)
        if commit:
            dbs.commit()
        return True

    @classmethod
    def get(cls, dbs, guid):
        return dbs.query(cls).get(guid)

    @classmethod
    def select(cls, dbs, filters=None, orders=None, limit=100, offset=0):
        q = dbs.query(cls)
        if filters:
            q = q.filter(*filters)
        orders = orders or cls._orders()
        if orders:
            q = q.order_by(*orders)
        return q.limit(limit).offset(offset).all() or []

    @classmethod
    def find_all(cls, dbs, filters, orders=None):
        q = dbs.query(cls)
        if filters:
            q = q.filter(*filters)
        orders = orders or cls._orders()
        if orders:
            q = q.order_by(*orders)
        return q.all() or []

    @classmethod
    def find_one(cls, dbs, filters):
        q = dbs.query(cls)
        if filters:
            q = q.filter(*filters)
        return q.one_or_none()

    @classmethod
    def count(cls, dbs, filters):
        q = dbs.query(cls)
        if filters:
            q = q.filter(*filters)
        return q.count()

    @classmethod
    def create(cls, dbs, data, commit=True):
        if 'guid' in data.keys():
            del(data['guid'])
        obj = cls()
        obj.guid = uuid.uuid5(uuid.uuid1(), uuid.uuid4().hex).hex
        for attr, value in data.items():
            setattr(obj, attr, value)
        dbs.add(obj)
        if commit:
            dbs.commit()
        return obj

    @classmethod
    def update(cls, dbs, filters, data, commit=True):
        if 'guid' in data.keys():
            del(data['guid'])
        q = dbs.query(cls)
        if filters:
            q = q.filter(*filters)
        res = q.update(data, synchronize_session=False)
        if commit:
            dbs.commit()
        return res

    @classmethod
    def delete(cls, dbs, filters, commit=True):
        q = dbs.query(cls)
        if filters:
            q = q.filter(*filters)
        res = q.delete(synchronize_session=False)
        if commit:
            dbs.commit()
        return res

    @classmethod
    def initial_data(cls, dbs):
        # Usage:
        # cls.create(dbs, ...)
        pass

    @classmethod
    def table_migrate(cls, op, dbs):
        # Usage:
        # op.drop_table(...)
        pass


class SessionHandler(object):

    def __init__(self, session):
        self._session = session

    def __enter__(self):
        return self._session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._session.close()


class DatabaseHandler(object):

    def __init__(self, backend, database, host=None, port=None,
                 username=None, password=None, debug=0):
        self.debug = debug
        self.engine = None
        self._session_factory = None

        if backend == 'sqlite':
            driver = 'sqlite'
            query = {}
        elif backend == 'pgsql':
            driver = 'postgresql+psycopg2'
            query = {'client_encoding': 'utf8'}
        elif backend in ['mysql', 'mariadb']:
            driver = 'mysql+mysqldb'
            query = {'charset': 'utf8mb4'}
        else:
            raise RuntimeError("invalid backend: %s" % backend)

        self.url = sa.engine.url.URL(
            driver, database=database, host=host, port=port,
            username=username, password=password, query=query)

    def init_engine(self, pool=None, connect_timeout=0, query_timeout=0):
        if not self.url:
            raise RuntimeError("no database url specified")

        backend = self.url.get_backend_name()
        if backend == 'sqlite':
            self.engine = sa.create_engine(
                self.url, poolclass=sa.pool.NullPool)
        else:
            connect_args = {'connect_timeout': connect_timeout}
            if backend == 'pgsql':
                connect_args.update({
                    'options': "-c statement_timeout=%s" % query_timeout,
                })
            elif backend in ['mysql', 'mariadb']:
                connect_args.update({
                    'read_timeout': query_timeout,
                    'write_timeout': query_timeout,
                })

            if pool and pool.get('size', 0) > 0:
                self.engine = sa.create_engine(
                    self.url,
                    pool_size=pool['size'],
                    max_overflow=pool.get('overflow', 8),
                    pool_timeout=pool.get('timeout', 10),
                    pool_recycle=pool.get('recycle', 1800),
                    connect_args=connect_args)
            else:
                self.engine = sa.create_engine(
                    self.url,
                    poolclass=sa.pool.NullPool,
                    connect_args=connect_args)

    def session_factory(self):
        # initialize session factory
        if not self._session_factory:
            if not self.engine:
                self.init_engine()
            self._session_factory = sa.orm.scoped_session(
                sa.orm.sessionmaker(bind=self.engine))

        return self._session_factory

    def session_handler(self):
        return SessionHandler(self.session_factory())


# adjust logging for sqlalchemy and alembic
def init_logging(debug=0):
    sqlalchemy_logger = logging.getLogger('sqlalchemy')
    alembic_logger = logging.getLogger('alembic')
    if debug >= 5:
        sqlalchemy_logger.setLevel(logging.DEBUG)
        alembic_logger.setLevel(logging.DEBUG)
    elif debug >= 4:
        sqlalchemy_logger.setLevel(logging.INFO)
        alembic_logger.setLevel(logging.INFO)
    else:
        sqlalchemy_logger.setLevel(logging.ERROR)
        alembic_logger.setLevel(logging.ERROR)


# create database tables and initial data
def init_database(dbh, models):
    from alembic.operations import Operations
    from alembic.migration import MigrationContext

    # init engine and disable pooling
    dbh.init_engine(pool=None)

    # create database structure
    BaseModel.metadata.create_all(dbh.engine)

    # execute migrations
    with dbh.session_handler() as dbs:
        conn = dbh.engine.connect()
        op = Operations(MigrationContext.configure(conn))
        for Model in models:
            Model.table_migrate(op, dbs)

    # load initial models data
    with dbh.session_handler() as dbs:
        for Model in models:
            Model.initial_data(dbs)

    return True

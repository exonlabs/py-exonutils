# -*- coding: utf-8 -*-
import copy
import logging
import sqlalchemy as sa

__all__ = []


class DBHandler(object):

    def __init__(self, options={}):
        self.options = copy.deepcopy(options)

        # adjust logging for sqlalchemy
        logging.getLogger('sqlalchemy').setLevel(logging.ERROR)

        # database engine backend
        self.backend = self.options.get('backend')
        if self.backend == 'sqlite':
            driver = 'sqlite'
            query_opts = {}
        elif self.backend == 'pgsql':
            driver = 'postgresql+psycopg2'
            query_opts = {'client_encoding': 'utf8'}
        elif self.backend == 'mysql':
            driver = 'mysql+mysqldb'
            query_opts = {'charset': 'utf8mb4'}
        elif self.backend == 'mssql':
            driver = 'mssql+pymssql'
            query_opts = {'charset': 'utf8'}
        else:
            raise RuntimeError("invalid backend: %s" % self.backend)

        # set default options
        if not self.options.get("connect_timeout"):
            self.options["connect_timeout"] = 30
        if not self.options.get("retries"):
            self.options["retries"] = 10
        if not self.options.get("retry_delay"):
            self.options["retry_delay"] = 0.5

        self.engine = None
        self.url = sa.engine.url.URL(
            driver,
            database=self.options.get('database'),
            host=self.options.get('host'),
            port=self.options.get('port'),
            username=self.options.get('username'),
            password=self.options.get('password'),
            query=query_opts,
        )

        self._session_factory = None

    def init_engine(self, **kwargs):
        if not self.url:
            raise RuntimeError("invalid engine URL")

        backend = self.url.get_backend_name()
        if backend == 'sqlite':
            self.engine = sa.create_engine(
                self.url, poolclass=sa.pool.NullPool)
        else:
            pool = kwargs.get('pool')
            connect_timeout = kwargs.get('connect_timeout') or 0
            query_timeout = kwargs.get('query_timeout') or 0

            if backend == 'pgsql':
                connect_args = {
                    'connect_timeout': connect_timeout,
                    'options': "-c statement_timeout=%s" % query_timeout,
                }
            elif backend == 'mysql':
                connect_args = {
                    'connect_timeout': connect_timeout,
                    'read_timeout': query_timeout,
                    'write_timeout': query_timeout,
                }
            elif backend == 'mssql':
                connect_args = {
                    'login_timeout': connect_timeout,
                    'timeout': query_timeout,
                }
            else:
                connect_args = {}

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

    def init_logging(self, level):
        logging.getLogger('sqlalchemy').setLevel(level)

    def session(self):
        if not self._session_factory:
            if not self.engine:
                self.init_engine()
            self._session_factory = sa.orm.scoped_session(
                sa.orm.sessionmaker(bind=self.engine))

        return self._session_factory()

    # create database tables and initialize table data
    def init_database(self, models, **kwargs):
        from .model import BaseModel

        # create database structure
        if not self.engine:
            self.init_engine(pool=None)
        BaseModel.metadata.create_all(self.engine)

        with self.session() as dbs:
            # build database schema
            for model in models:
                model.upgrade_schema(dbs, **kwargs)

            # initialize models data
            for model in models:
                model.initialize_data(dbs, **kwargs)

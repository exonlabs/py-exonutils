# -*- coding: utf-8 -*-
import sys
import logging
from pprint import pprint
from importlib import import_module
from argparse import ArgumentParser

from exonutils.db.model import BaseModel
from exonutils.db.handlers import DBHandler

logging.basicConfig(
    level=logging.INFO, stream=sys.stdout,
    format='%(asctime)s %(levelname)-5.5s [%(name)s] %(message)s')
logging.addLevelName(logging.WARNING, "WARN")
logging.addLevelName(logging.CRITICAL, "FATAL")


BACKENDS = ['sqlite', 'mysql', 'pgsql', 'mssql']

DB_OPTIONS = {
    "database": "test",
    "username": "user1",
    "password": "123456",

    # -- Optional args --
    # "connect_timeout": 30,
    # "retries": 10,
    # "retry_delay": 0.5,
    # "sql_placeholder": "$?",
    # "foreign_keys_constraints": True,

    # -- sqlite args --
    # "isolation_level": None,
}


class Foobar(BaseModel):

    @classmethod
    def table_name(cls):
        return 'foobar'

    @classmethod
    def table_columns(cls):
        return [
            ("col1", "VARCHAR(128) NOT NULL", "UNIQUE INDEX"),
            ("col2", "TEXT"),
            ("col3", "INTEGER"),
            ("col4", "BOOLEAN NOT NULL DEFAULT 0"),
        ]

    @classmethod
    def default_orderby(cls):
        return ["col1 ASC"]

    @classmethod
    def initialize_data(cls, dbs, **kwargs):
        for i in range(5):
            data = dbs.query(cls, **kwargs) \
                .filter("col1=$?", 'foo_%s' % i).first()
            if not data:
                cls(dbs, **kwargs).insert({
                    'col1': 'foo_%s' % i,
                    'col2': 'description %s' % i,
                    'col3': i,
                })


def run_operations(dbh):
    dbh.init_database([Foobar])
    print("DB initialize: Done")

    # checking DB
    print("\nAll entries:")
    with dbh.session() as dbs:
        for item in Foobar(dbs).all():
            pprint(item)
        print("\nTotal Items: %s" % Foobar(dbs).count())

    # update entries
    print("\nEntries to Modify:")
    with dbh.session() as dbs:
        qry = Foobar(dbs).filter("col3>=$?", 2)

        data = qry.columns('col1', 'col2', 'col3').all()
        for item in data:
            pprint(item)
            Foobar(dbs).filter("col1=$?", item['col1']) \
                .update({
                    'col3': item['col3'] + 10,
                })

        print("\n -- After Modify:")
        for item in qry.columns().all():
            pprint(item)

    # update entries
    print("\nEntries to Delete:")
    with dbh.session() as dbs:
        qry = Foobar(dbs).filter("col3<$?", 2)
        for item in qry.all():
            pprint(item)

        print('\n -- Affected:', qry.delete())

        print("\n -- After Delete:")
        for item in Foobar(dbs).all():
            pprint(item)


def main():
    logger = logging.getLogger()
    logger.name = 'main'

    db_logger = logging.getLogger('db')
    db_logger.parent = logger
    db_logger.setLevel(logging.WARNING)

    try:
        pr = ArgumentParser(prog=None)
        pr.add_argument(
            '-x', dest='debug', action='count', default=0,
            help="set debug modes")
        pr.add_argument(
            '--backend', dest='backend', default=BACKENDS[0],
            help="select backend [%s]" % '|'.join(BACKENDS))
        pr.add_argument(
            '--setup', dest='setup', action='store_true',
            help="perform database setup before operation")
        args = pr.parse_args()

        if args.debug > 0:
            logger.setLevel(logging.DEBUG)
        if args.debug >= 3:
            db_logger.setLevel(logging.DEBUG)

        if args.backend not in BACKENDS:
            print("\nError!! invalid DB backend\n")
            sys.exit(1)

        print("\n* Using backend: %s" % args.backend)

        if args.backend == 'sqlite':
            DB_OPTIONS['database'] = "/tmp/%s.db" % DB_OPTIONS['database']

        mod = import_module(
            '.%s.engine' % args.backend, package='exonutils.db.backends')
        engine = mod.Engine()

        mod = import_module(
            '.%s.utils' % args.backend, package='exonutils.db.backends')

        print("\nDB Options:")
        cfg = mod.interactive_config(defaults=DB_OPTIONS)
        pprint(cfg)
        print()

        if args.setup:
            print("DB setup:")
            mod.interactive_setup(cfg)
            print("Done")

        dbh = DBHandler(engine, cfg)
        dbh.logger = db_logger

        run_operations(dbh)

        print()

    except Exception as e:
        logger.fatal(str(e), exc_info=args.debug)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n-- terminated --")


if __name__ == '__main__':
    main()

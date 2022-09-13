# -*- coding: utf-8 -*-
import sys
import logging
from pprint import pprint
from argparse import ArgumentParser

import sqlalchemy as sa

from exonutils.db.sqlalchemy.handlers import DBHandler
from exonutils.db.sqlalchemy.model import BaseModel
from exonutils.db.sqlalchemy.utils import \
    interactive_config, interactive_setup

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
}


class Foobar(BaseModel):
    __tablename__ = 'foobar'

    col1 = sa.Column(
        sa.Unicode(128), index=True, unique=True, nullable=False)
    col2 = sa.Column(sa.UnicodeText)
    col3 = sa.Column(sa.Integer)
    col4 = sa.Column(sa.Boolean, nullable=False, default=False)

    @classmethod
    def initialize_data(cls, dbs, **kwargs):
        for i in range(5):
            data = dbs.query(cls) \
                .filter(cls.col1 == 'foo_%s' % i).first()
            if not data:
                cls.create(dbs, {
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
        for item in dbs.query(Foobar) \
                .order_by(Foobar.col1.asc()).limit(100).all():
            pprint(dict(item))
        print("\nTotal Items: %s" % dbs.query(Foobar).count())

    # update entries
    print("\nEntries to Modify:")
    with dbh.session() as dbs:
        qry = dbs.query(Foobar) \
            .filter(Foobar.col3 >= 2).order_by(Foobar.col1.asc())

        data = qry.all()
        for item in data:
            pprint(dict(item))
            Foobar.update(
                dbs.query(Foobar).filter(Foobar.col1 == item.col1), {
                    'col3': item.col3 + 10,
                })

        print("\n -- After Modify:")
        for item in qry.all():
            pprint(dict(item))

    # update entries
    print("\nEntries to Delete:")
    with dbh.session() as dbs:
        qry = dbs.query(Foobar).filter(Foobar.col3 < 2)
        for item in qry.order_by(Foobar.col1.asc()).all():
            pprint(dict(item))

        print('\n -- Affected:', Foobar.delete(qry))

        print("\n -- After Delete:")
        for item in dbs.query(Foobar).order_by(Foobar.col1.asc()).all():
            pprint(dict(item))


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

        print("\nDB Options:")
        cfg = interactive_config(args.backend, defaults=DB_OPTIONS)
        pprint(cfg)
        print()

        if args.setup:
            print("DB setup:")
            interactive_setup(args.backend, cfg)
            print("Done")

        dbh = DBHandler(cfg)
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

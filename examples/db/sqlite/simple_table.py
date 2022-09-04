# -*- coding: utf-8 -*-
import sys
import logging
from pprint import pprint
from argparse import ArgumentParser

from exonutils.db.model import BaseModel

from exonutils.db.backends.sqlite.handlers import DBHandler
from exonutils.db.backends.sqlite.utils import \
    interactive_config, interactive_setup

logging.basicConfig(
    level=logging.INFO, stream=sys.stdout,
    format='%(asctime)s %(levelname)-5.5s [%(name)s] %(message)s')
logging.addLevelName(logging.WARNING, "WARN")
logging.addLevelName(logging.CRITICAL, "FATAL")

DB_OPTIONS = {
    "database": "/tmp/test.db",

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
            ("col1", "TEXT NOT NULL", "UNIQUE INDEX"),
            ("col2", "TEXT"),
            ("col3", "INTEGER"),
            ("col4", "BOOLEAN NOT NULL DEFAULT 0"),
        ]

    @classmethod
    def initialize_data(cls, dbs, **kwargs):
        for i in range(5):
            data = dbs.query(cls, **kwargs) \
                .filter("col1=$?", 'foo_%s' % i).first()
            if not data:
                dbs.query(cls, **kwargs).insert({
                    'col1': 'foo_%s' % i,
                    'col2': 'description %s' % i,
                    'col3': i,
                })


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
            help='set debug modes')
        args = pr.parse_args()

        if args.debug > 0:
            logger.setLevel(logging.DEBUG)
        if args.debug >= 3:
            db_logger.setLevel(logging.DEBUG)

        print("\nDB Options:")
        cfg = interactive_config(defaults=DB_OPTIONS)
        pprint(cfg)
        print()

        interactive_setup(cfg)
        print("DB setup: Done")

        dbh = DBHandler(cfg)
        dbh.logger = db_logger

        dbh.init_database([Foobar])
        print("DB initialize: Done")

        # checking DB
        print("\nAll entries:")
        with dbh.session() as dbs:
            for item in dbs.query(Foobar).orderby('col1 ASC').all():
                pprint(item)
            print("\nTotal Items: %s" % dbs.query(Foobar).count())

        # update entries
        print("\nEntries to Modify:")
        with dbh.session() as dbs:
            qry = dbs.query(Foobar) \
                .filter("col3>=$?", 2).orderby('col1 ASC')

            data = qry.columns('col1', 'col2', 'col3').all()
            for item in data:
                pprint(item)
                dbs.query(Foobar).filter("col1=$?", item['col1']) \
                    .update({
                        'col3': item['col3'] + 10,
                    })

            print("\n -- After Modify:")
            for item in qry.columns().all():
                pprint(item)

        # update entries
        print("\nEntries to Delete:")
        with dbh.session() as dbs:
            qry = dbs.query(Foobar) \
                .filter("col3<$?", 2).orderby('col1 ASC')
            for item in qry.all():
                pprint(item)

            print('\n -- Affected:', qry.delete())

            print("\n -- After Delete:")
            for item in dbs.query(Foobar).orderby('col1 ASC').all():
                pprint(item)

        print()

    except Exception as e:
        logger.fatal(str(e), exc_info=args.debug)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n-- terminated --")


if __name__ == '__main__':
    main()

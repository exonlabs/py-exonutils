# -*- coding: utf-8 -*-
import sys
import random
import logging
from datetime import datetime
from argparse import ArgumentParser
from traceback import format_exc

from exonutils import sqlitedb as db
from exonutils import dbutils

logging.basicConfig(
    level=logging.INFO, stream=sys.stdout,
    format='%(asctime)s %(levelname)-5.5s [%(name)s] %(message)s')
logging.addLevelName(logging.WARNING, "WARN")
logging.addLevelName(logging.CRITICAL, "FATAL")


class User(db.BaseModel):
    __tablename__ = 'users'
    __table_columns__ = [
        ('name', 'TEXT NOT NULL'),
        ('email', 'TEXT'),
        ('age', 'INTEGER'),
        ('enable', 'BOOLEAN NOT NULL DEFAULT 0'),
        ('created', 'DATETIME'),
    ]

    @classmethod
    def initial_data(cls, dbs):
        for i in range(5):
            users = cls.find_all(
                dbs, "name like 'foobar_%s_%%'" % i)
            if not users:
                for j in range(2):
                    cls.create(dbs, {
                        'name': 'foobar_%s_%s' % (i, j),
                        'email': 'foobar_%s@domain_%s' % (i, j),
                        'age': 0,
                        'enable': False,
                        'created': datetime.now(),
                    })


if __name__ == '__main__':
    try:
        pr = ArgumentParser(prog=None)
        pr.add_argument(
            '-x', dest='debug', action='count', default=0,
            help='set debug modes')
        args = pr.parse_args()

        db.init_logging(debug=args.debug)

        cfg = dbutils.interactive_config('sqlite', defaults={
            'database': '/tmp/test.db',
        })
        print("DB config: %s" % cfg)

        dbh = db.DatabaseHandler(
            cfg['database'],
            debug=args.debug)

        dbutils.interactive_setup(cfg)
        print("DB setup: Done")

        models = [User]
        db.init_database(dbh, models)
        print("DB initialize: Done")

        # checking DB
        print("\nAll entries:")
        with dbh.session_handler() as dbs:
            for usr in User.find_all(dbs, None):
                print(usr)
            print("Total: %s" % User.count(dbs, None))

        print("\nCreate new entries:")
        with dbh.session_handler() as dbs:
            usr = User.create(dbs, {
                'name': 'foobar_NEW',
                'email': 'foobar_NEW@domain',
                'age': 4,
                'enable': True,
            })
            print(usr)

        print("\nFilter & modify entries:")
        with dbh.session_handler() as dbs:
            users = User.find_all(
                dbs, "name like 'foobar_2_%%' OR name like 'foobar_4_%%'")
            for usr in users:
                usr.modify(dbs, {
                    'name': usr.name + '_#',
                    'enable': not usr.enable,
                    'created': datetime.now(),
                })
                print(usr)

        print("\nFilter & delete entries:")
        with dbh.session_handler() as dbs:
            users = User.find_all(
                dbs, "name like 'foobar_4_%%_#_#_#'")
            for usr in users:
                print(usr)
                usr.remove(dbs)

        print("\nUpdate multiple entries:")
        with dbh.session_handler() as dbs:
            res = User.update(
                dbs, "name like 'foobar_0_%%'", {
                    'age': random.randint(1, 10),
                })
            print("Modified rows: %s" % res)

        print("\nDelete multiple entries:")
        with dbh.session_handler() as dbs:
            res = User.delete(
                dbs, "name like 'foobar_3_%%'")
            print("Modified rows: %s" % res)

        print("\nAll entries after changes:")
        with dbh.session_handler() as dbs:
            for usr in User.find_all(dbs, None):
                print(usr)
            print("Total: %s" % User.count(dbs, None))

    except Exception:
        print(format_exc())
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n-- terminated --")

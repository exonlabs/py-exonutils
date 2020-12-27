# -*- coding: utf-8 -*-
import sys
import logging
from argparse import ArgumentParser
from traceback import format_exc

from exonutils import sqlitedb as sql

logging.basicConfig(
    level=logging.INFO, stream=sys.stdout,
    format='%(asctime)s %(levelname)-5.5s [%(name)s] %(message)s')
logging.addLevelName(logging.WARNING, "WARN")
logging.addLevelName(logging.CRITICAL, "FATAL")


class User(sql.BaseModel):
    __tablename__ = 'users'

    __columns__ = ['guid', 'name', 'email', 'age']

    # __metadata__ = {
    #     'create_table': '''
    #         CREATE TABLE users IF NOT EXISTS (
    #             guid TEXT PRIMARY KEY NOT NULL,
    #             name TEXT NOT NULL DEFAULT '',
    #             email TEXT NOT NULL DEFAULT '',
    #             age INTEGER NOT NULL DEFAULT 0
    #         ) WITHOUT ROWID;''',
    # }

    @classmethod
    def initial_data(cls, dbs):
        pass

    # @classmethod
    # def initial_data(cls, dbs):
    #     for i in range(5):
    #         users = cls.find(dbs, (cls.name.like('foobar_%s_%%' % i),))
    #         if not users:
    #             for j in range(2):
    #                 cls.create(dbs, {
    #                     cls.name: 'foobar_%s_%s' % (i, j),
    #                     cls.email: 'foobar_%s@domain_%s' % (i, j),
    #                 })


if __name__ == '__main__':
    try:
        pr = ArgumentParser(prog=None)
        pr.add_argument(
            '-x', dest='debug', action='count', default=0,
            help='set debug modes')
        args = pr.parse_args()

        sql.init_db_logging(debug=args.debug)

        cfg = sql.interactive_db_config(defaults={
            'database': '/tmp/test.db',
        })
        print("DB config: %s" % cfg)

        dbh = sql.DatabaseHandler(
            cfg['database'],
            debug=args.debug)

        # interactive_db_setup(cfg)
        # print("DB setup: Done")

        # models = [User]
        # init_database(dbh, models)
        # print("DB initialize: Done")

        # checking DB
        print("*" * 50)
        print("All entries:")
        with dbh as dbs:
            for usr in User.find(dbs, None):
                print(usr)
            print("Total: %s" % User.count(dbs, None))
        print("*" * 50)

        # print("Filter & modify entries:")
        # with dbh as dbs:
        #     users = User.find(dbs, (User.or_(
        #         User.name.like('foobar_2_%%'),
        #         User.name.like('foobar_4_%%')),))
        # with dbh as dbs:
        #     for usr in users:
        #         print(usr)
        #         usr.modify(dbs, {
        #             User.name: usr.name + '_#',
        #         })
        # print("*" * 50)
        # print("All entries after modify:")
        # with dbh as dbs:
        #     for usr in User.find(dbs, None):
        #         print(usr)
        # print("*" * 50)

    except Exception:
        print(format_exc())
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n-- terminated --")

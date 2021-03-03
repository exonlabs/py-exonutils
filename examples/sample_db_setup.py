# -*- coding: utf-8 -*-
import sys
import random
import logging
from argparse import ArgumentParser
from traceback import format_exc

import sqlalchemy as sa
from exonutils.database import BaseModel, DatabaseHandler, init_db_logging, \
    init_database, interactive_db_config, interactive_db_setup

logging.basicConfig(
    level=logging.INFO, stream=sys.stdout,
    format='%(asctime)s %(levelname)-5.5s [%(name)s] %(message)s')
logging.addLevelName(logging.WARNING, "WARN")
logging.addLevelName(logging.CRITICAL, "FATAL")


class User(BaseModel):
    __tablename__ = 'users'
    __table_args__ = {'mysql_engine': 'InnoDB'}

    name = sa.Column(sa.Unicode(32), nullable=False)
    email = sa.Column(sa.Unicode(256), nullable=False, default='')
    age = sa.Column(sa.Integer, nullable=False, default=0)

    @classmethod
    def initial_data(cls, dbs):
        for i in range(5):
            users = cls.find(dbs, (cls.name.like('foobar_%s_%%' % i),))
            if not users:
                for j in range(2):
                    cls.create(dbs, {
                        'name': 'foobar_%s_%s' % (i, j),
                        'email': 'foobar_%s@domain_%s' % (i, j),
                        'age': 0,
                    })


if __name__ == '__main__':
    try:
        pr = ArgumentParser(prog=None)
        pr.add_argument(
            '-x', dest='debug', action='count', default=0,
            help='set debug modes')
        args = pr.parse_args()

        init_db_logging(debug=args.debug)

        cfg = interactive_db_config(defaults={
            'backend': 'sqlite',
            'database': '/tmp/test.db',
        })
        print("DB config: %s" % cfg)

        dbh = DatabaseHandler(
            cfg['backend'],
            cfg['database'],
            host=cfg.get('host', None),
            port=cfg.get('port', None),
            username=cfg.get('username', None),
            password=cfg.get('password', None),
            debug=args.debug)

        interactive_db_setup(cfg)
        print("DB setup: Done")

        models = [User]
        init_database(dbh, models)
        print("DB initialize: Done")

        # checking DB
        print("*" * 50)
        print("All entries:")
        with dbh.session_handler() as dbs:
            for usr in User.find(dbs, None):
                print(usr)
            print("Total: %s" % User.count(dbs, None))
        print("*" * 50)

        print("\nCreate new entries:")
        with dbh.session_handler() as dbs:
            usr = User.create(dbs, {
                'name': 'foobar_NEW',
                'email': 'foobar_NEW@domain',
                'age': 0,
            })
            print(usr)

        print("\nFilter & modify entries:")
        with dbh.session_handler() as dbs:
            users = User.find(
                dbs, (sa.or_(
                    User.name.like('foobar_2_%%'),
                    User.name.like('foobar_4_%%')),))
            for usr in users:
                print(usr)
                usr.modify(dbs, {
                    'name': usr.name + '_#',
                })

        print("\nFilter & delete entries:")
        with dbh.session_handler() as dbs:
            users = User.find(
                dbs, (User.name.like('foobar_4_%%_#_#_#'),))
            for usr in users:
                print(usr)
                usr.remove(dbs)

        print("\nUpdate multiple entries:")
        with dbh.session_handler() as dbs:
            res = User.update(
                dbs, (User.name.like('foobar_0_%%'),), {
                    'age': random.randint(1, 10),
                })
            print("Modified rows: %s" % res)

        print("\nDelete multiple entries:")
        with dbh.session_handler() as dbs:
            res = User.delete(
                dbs, (User.name.like('foobar_3_%%'),))
            print("Modified rows: %s" % res)

        print("*" * 50)
        print("All entries after changes:")
        with dbh.session_handler() as dbs:
            for usr in User.find(dbs, None):
                print(usr)
            print("Total: %s" % User.count(dbs, None))
        print("*" * 50)

    except Exception:
        print(format_exc())
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n-- terminated --")

# -*- coding: utf-8 -*-
import sys
import logging
from argparse import ArgumentParser
from traceback import format_exc

import sqlalchemy as sa
from exonutils.database import BaseModel, DatabaseHandler, init_db_logging, \
    init_database, interactive_db_config, interactive_db_setup

logging.basicConfig(
    level=logging.DEBUG, stream=sys.stdout,
    format='%(asctime)s [%(name)s] %(levelname)s %(message)s')


class User(BaseModel):
    __tablename__ = 'users'
    __table_args__ = {'mysql_engine': 'InnoDB'}

    name = sa.Column(sa.Unicode(32), nullable=False)
    email = sa.Column(sa.Unicode(256), nullable=False, default='')

    @classmethod
    def initial_data(cls, dbs):
        users = cls.find(dbs, name=u'foobar')
        if not users:
            for i in range(10):
                cls.create(
                    dbs, name='foobar',
                    email='foobar_%s@something.local' % i)


if __name__ == '__main__':
    try:
        pr = ArgumentParser(prog=None)
        pr.add_argument(
            '-x', dest='debug', action='count', default=0,
            help='set debug modes')
        args = pr.parse_args()

        init_db_logging(debug=args.debug)

        cfg = interactive_db_config(default='sqlite')
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
        print("******************************")
        print("Checking DB entries:")
        with dbh as dbs:
            users = User.find(dbs, name=u'foobar')
        for usr in users:
            print('User:  name=%s  email=%s' % (usr.name, usr.email))
        print("******************************")

    except Exception:
        print(format_exc())
        sys.exit(1)

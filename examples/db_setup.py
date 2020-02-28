# -*- coding: utf-8 -*-
import sys
import logging
from argparse import ArgumentParser
from traceback import format_exc

import sqlalchemy as sa
from exonutils.database import BaseModel, DatabaseHandler, \
    init_database, interactive_db_config, interactive_db_setup

logging.basicConfig(
    level=logging.DEBUG, stream=sys.stdout,
    format='%(asctime)s [%(name)s] %(levelname)s %(message)s')


class User(BaseModel):
    __tablename__ = 'users'
    __table_args__ = {'mysql_engine': 'InnoDB'}

    name = sa.Column(sa.String(32), nullable=False, unique=True)
    email = sa.Column(sa.String(256), nullable=False, default='')

    @classmethod
    def initial_data(cls, dbs):
        user = cls.find_one(dbs, name='foobar')
        if not user:
            cls.create(dbs, name='foobar')


if __name__ == '__main__':
    try:
        pr = ArgumentParser(prog=None)
        pr.add_argument('-x', dest='debug', action='store_true',
                        help='enable debug mode')
        args = pr.parse_args()

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
        print("Checking Models")
        dbs = dbh.create_session()
        res = User.find(dbs, name='foobar')
        print(res)
        print("******************************")

    except Exception:
        print(format_exc())
        sys.exit(1)

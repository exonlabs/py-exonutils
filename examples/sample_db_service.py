# -*- coding: utf-8 -*-
import sys
import logging
from argparse import ArgumentParser
from traceback import format_exc

import sqlalchemy as sa
from exonutils.database import BaseModel, DatabaseHandler, init_db_logging, \
    init_database, interactive_db_config, interactive_db_setup
from exonutils.service import BaseService, BaseServiceTask

logging.basicConfig(
    level=logging.INFO, stream=sys.stdout,
    format='%(asctime)s %(levelname)-5.5s [%(name)s] %(message)s')
logging.addLevelName(logging.WARNING, "WARN")
logging.addLevelName(logging.CRITICAL, "FATAL")

dbh = None


class User(BaseModel):
    __tablename__ = 'users'
    __table_args__ = {'mysql_engine': 'InnoDB'}

    name = sa.Column(sa.Unicode(32), nullable=False)
    email = sa.Column(sa.Unicode(128), nullable=False, default='')
    count = sa.Column(sa.Integer, nullable=False, default=0)

    @classmethod
    def initial_data(cls, dbs):
        for i in range(5):
            users = cls.find(dbs, (cls.name.like('foobar_%s_%%' % i),))
            if not users:
                for j in range(2):
                    cls.create(dbs, {
                        'name': 'foobar_%s_%s' % (i, j),
                        'email': 'foobar_%s@domain_%s' % (i, j),
                        'count': 0,
                    })


class Task1(BaseServiceTask):

    def initialize(self):
        self.log.info("initializing")

    def execute(self):
        with dbh.session_context() as dbs:
            users = User.find(dbs, None)[:2]

        with dbh.session_context() as dbs:
            for usr in users:
                usr.modify(dbs, {
                    'name': usr.name + '_#',
                })
            User.update(dbs, None, {
                'count': User.count + 1,
            })

        self.sleep(3)

    def terminate(self):
        self.log.info("terminating")


class Task2(BaseServiceTask):

    def initialize(self):
        self.log.info("initializing")

    def execute(self):
        print("*" * 50)
        print("All entries:")
        with dbh.session_context() as dbs:
            for usr in User.find(dbs, None):
                print(usr)
        print("*" * 50)
        self.sleep(2)

    def terminate(self):
        self.log.info("terminating")


if __name__ == '__main__':
    log = logging.getLogger()
    log.name = 'main'
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

        srv = BaseService('SampleDBService', logger=log, debug=args.debug)
        srv.tasks = [Task1, Task2]
        srv.start()

    except Exception:
        print(format_exc())
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n-- terminated --")

# -*- coding: utf-8 -*-
import sys
import random
import logging
import hashlib
from datetime import datetime
from argparse import ArgumentParser
from traceback import format_exc

import sqlalchemy as sa
from exonutils import sqlalchemydb as db
from exonutils import dbutils

logging.basicConfig(
    level=logging.INFO, stream=sys.stdout,
    format='%(asctime)s %(levelname)-5.5s [%(name)s] %(message)s')
logging.addLevelName(logging.WARNING, "WARN")
logging.addLevelName(logging.CRITICAL, "FATAL")


# convert string to hash
class HashStr(sa.types.TypeDecorator):
    impl = sa.types.String
    cache_ok = True

    def process_bind_param(self, str_value, dialect):
        if str_value is None:
            return None
        if type(str_value) is str:
            str_value = str_value.encode()
        return hashlib.sha256(str_value).hexdigest()


class Role(db.BaseModel):
    __tablename__ = 'roles'
    title = sa.Column(
        sa.Unicode(32), nullable=False, unique=True, index=True)
    description = sa.Column(
        sa.UnicodeText, nullable=True)

    @classmethod
    def initial_data(cls, dbs):
        role = cls.find_one(dbs, (cls.title == 'Administrator',))
        if not role:
            role = cls.create(dbs, {
                'title': 'Administrator',
                'description': "Administrator Role",
            })
        return role


class User(db.BaseModel):
    __tablename__ = 'users'
    username = sa.Column(
        sa.Unicode(32), nullable=False, unique=True, index=True)
    password = sa.Column(
        HashStr(256), nullable=False)
    email = sa.Column(
        sa.Unicode(256), nullable=True)
    age = sa.Column(
        sa.Integer, nullable=True)
    enable = sa.Column(
        sa.Boolean, nullable=False, default=False)
    created = sa.Column(
        sa.DateTime)
    role_guid = sa.Column(
        sa.String(32), sa.ForeignKey(
            'roles.guid', onupdate='CASCADE', ondelete='NO ACTION'),
        nullable=False)

    role = sa.orm.relationship(
        'Role', lazy='joined',
        backref=sa.orm.backref(
            'users', lazy='dynamic', order_by='User.username'))

    @classmethod
    def initial_data(cls, dbs):
        role = Role.initial_data(dbs)
        for i in range(5):
            users = cls.find_all(
                dbs, (cls.username.like('foobar_%s_%%' % i),))
            if not users:
                for j in range(2):
                    cls.create(dbs, {
                        'username': 'foobar_%s_%s' % (i, j),
                        'password': 'foopass_%s_%s' % (i, j),
                        'email': 'foobar_%s@domain_%s' % (i, j),
                        'age': 0,
                        'enable': False,
                        'created': datetime.now(),
                        'role_guid': role.guid,
                    })


if __name__ == '__main__':
    try:
        pr = ArgumentParser(prog=None)
        pr.add_argument(
            '-x', dest='debug', action='count', default=0,
            help='set debug modes')
        args = pr.parse_args()

        db.init_logging(debug=args.debug)

        cfg = dbutils.interactive_config(defaults={
            'backend': 'sqlite',
            'database': '/tmp/test.db',
        })
        print("DB config: %s" % cfg)

        dbh = db.DatabaseHandler(
            cfg['backend'],
            cfg['database'],
            host=cfg.get('host', None),
            port=cfg.get('port', None),
            username=cfg.get('username', None),
            password=cfg.get('password', None),
            debug=args.debug)

        dbutils.interactive_setup(cfg)
        print("DB setup: Done")

        models = [Role, User]
        db.init_database(dbh, models)
        print("DB initialize: Done")

        # checking DB
        print("\nAll entries:")
        with dbh.session_handler() as dbs:
            for role in Role.find_all(dbs, None):
                print(role)
            for usr in User.find_all(dbs, None):
                print(usr)
            print("Total Users: %s" % User.count(dbs, None))

        print("\nCreate new entry and delete it:")
        with dbh.session_handler() as dbs:
            usr = User.create(dbs, {
                'username': 'foobar_NEW',
                'password': 'admin',
                'email': 'foobar_NEW@domain',
                'age': 8,
                'enable': True,
                'role_guid': role.guid,
            })
            print(usr)
            usr.remove(dbs)
            print('-- deleted --')

        print("\nFilter & modify entries:")
        with dbh.session_handler() as dbs:
            users = User.find_all(
                dbs, (sa.or_(
                    User.username.like('foobar_2_%%'),
                    User.username.like('foobar_4_%%')),))
            for usr in users:
                usr.modify(dbs, {
                    'username': usr.username + '_#',
                    'enable': not usr.enable,
                    'created': datetime.now(),
                })
                print(usr)

        print("\nFilter & delete entries:")
        with dbh.session_handler() as dbs:
            users = User.find_all(
                dbs, (User.username.like('foobar_4_%%_#_#_#'),))
            for usr in users:
                print(usr)
                usr.remove(dbs)

        print("\nUpdate multiple entries:")
        with dbh.session_handler() as dbs:
            res = User.update(
                dbs, (User.username.like('foobar_0_%%'),), {
                    'age': random.randint(1, 10),
                })
            print("Modified rows: %s" % res)

        print("\nDelete multiple entries:")
        with dbh.session_handler() as dbs:
            res = User.delete(
                dbs, (User.username.like('foobar_3_%%'),))
            print("Modified rows: %s" % res)

        print("\nAll entries after changes:")
        with dbh.session_handler() as dbs:
            for usr in User.find_all(dbs, None):
                print(usr)
            print("Total: %s" % User.count(dbs, None))

        print()

    except Exception:
        print(format_exc())
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n-- terminated --")

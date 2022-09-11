# -*- coding: utf-8 -*-
import sqlalchemy as sa
from sqlalchemy.ext.declarative import as_declarative

from exonutils.db.common import generate_guid

__all__ = []


@as_declarative()
class BaseModel(object):
    __tablename__ = ''
    __table_args__ = {
        'mysql_engine': 'InnoDB',
    }

    guid = sa.Column(
        sa.String(32), primary_key=True, index=True, unique=True,
        autoincrement=False, nullable=False)

    def __iter__(self):
        return iter([
            (k, getattr(self, k))
            for k in self.__mapper__.columns.keys()
        ])

    @classmethod
    def create(cls, dbs, data):
        if type(data) is not dict:
            raise ValueError("invalid data type")

        if 'guid' in data:
            guid = data['guid']
            del(data['guid'])
        else:
            guid = generate_guid()

        obj = cls()
        obj.guid = guid
        for k, v in data.items():
            setattr(obj, k, v)

        dbs.add(obj)
        if not dbs.in_nested_transaction():
            dbs.commit()

        return guid

    @classmethod
    def update(cls, query, data):
        if type(data) is not dict:
            raise ValueError("invalid data type")

        if 'guid' in data:
            del(data['guid'])

        res = query.update(data)
        if not query.session.in_nested_transaction():
            query.session.commit()

        return res

    @classmethod
    def delete(cls, query):
        res = query.delete()
        if not query.session.in_nested_transaction():
            query.session.commit()

        return res

    @classmethod
    def upgrade_schema(cls, dbs, **kwargs):
        pass

    @classmethod
    def initialize_data(cls, dbs, **kwargs):
        pass

# -*- coding: utf-8 -*-

__all__ = []


class BaseModel(object):

    # shorthand to create query instance from model
    def __new__(cls, dbs, **kwargs):
        return dbs.query(cls, **kwargs)

    @classmethod
    def table_name(cls):
        # example:
        # return 'table_name'
        raise NotImplementedError()

    @classmethod
    def table_args(cls):
        # options:
        return {
            # -- sqlite args --
            'sqlite_without_rowid': True,
        }

    @classmethod
    def table_columns(cls):
        # Usage:
        # return [
        #     (colname, definition [, constraint]),
        # ]
        # example:
        # return [
        #     ('col1', 'TEXT NOT NULL', 'INDEX UNIQUE'),
        # ]
        raise NotImplementedError()

    @classmethod
    def table_constraints(cls):
        # example:
        # return [
        #     'CHECK (field1 IN (0, 1))',
        #     'FOREIGN KEY (tbl1_id) REFERENCES tbl1 (tbl1_id)',
        # ]
        return []

    @classmethod
    def default_orderby(cls):
        return []

    @classmethod
    def data_adapters(cls):
        # example:
        # return {
        #     'colname': adapter_callable,
        # }
        return {}

    @classmethod
    def data_converters(cls):
        # example:
        # return {
        #     'colname': converter_callable,
        # }
        return {}

    @classmethod
    def upgrade_schema(cls, dbs, **kwargs):
        pass

    @classmethod
    def initialize_data(cls, dbs, **kwargs):
        pass

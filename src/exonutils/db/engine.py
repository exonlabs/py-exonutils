# -*- coding: utf-8 -*-

__all__ = []


class BaseEngine(object):

    backend = ""

    sql_placeholder = '?'

    Error = Exception
    InterfaceError = Exception
    DatabaseError = Exception
    DataError = Exception
    OperationalError = Exception
    IntegrityError = Exception
    InternalError = Exception
    ProgrammingError = Exception
    NotSupportedError = Exception

    def connection(self, options):
        raise NotImplementedError()

    def post_connect(self, conn, options):
        pass

    def table_schema(self, model, **kwargs):
        raise NotImplementedError()

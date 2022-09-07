# -*- coding: utf-8 -*-
from exonutils.db.handlers import BaseDBHandler

from .session import Session

__all__ = []


class DBHandler(BaseDBHandler):

    def __init__(self, options={}):
        super(DBHandler, self).__init__(options=options)

        self.backend = 'sqlite'
        self.session_factory = Session

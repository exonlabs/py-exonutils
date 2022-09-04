# -*- coding: utf-8 -*-
from exonutils.db.handlers import BaseDBHandler

from .session import Session

__all__ = []


class DBHandler(BaseDBHandler):

    def __init__(self, options={}):
        super(DBHandler, self).__init__(options=options)

        self.backend = 'sqlite'

    # get new session handler
    def session(self):
        sess = Session(options=self.options)
        sess.logger = self.logger
        return sess

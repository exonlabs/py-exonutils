# -*- coding: utf-8 -*-
import sys
from abc import ABCMeta

__all__ = []


class Handler(metaclass=ABCMeta):

    def handle_record(self, r: str):
        pass


# Write log messages to Stdout
class StdoutHandler(Handler):

    def handle_record(self, r: str):
        sys.stdout.write(str(r) + "\n")


# Write log messages to file
class FileHandler(Handler):

    def __init__(self, path: str):
        self.filepath = path

    def handle_record(self, r: str):
        with open(self.filepath, 'a') as f:
            f.write(str(r) + "\n")

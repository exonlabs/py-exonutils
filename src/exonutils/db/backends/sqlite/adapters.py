# -*- coding: utf-8 -*-
import sqlite3 as sqlite
from datetime import datetime, date, time

__all__ = []


# BOOLEAN

def bool_adapter(value):
    return 1 if bool(value) else 0


def bool_converter(value):
    return bool(int(value))


# DATETIME, DATE, TIME, TIMESTAMP

def datetime_adapter(value):
    if value:
        return value.strftime("%Y-%m-%d %H:%M:%S.%f")
    return None


def date_adapter(value):
    if value:
        return value.strftime("%Y-%m-%d")
    return None


def time_adapter(value):
    if value:
        return value.strftime("%H:%M:%S.%f")
    return None


def datetime_converter(value):
    if not value:
        return None

    value = str(value.decode()).strip()
    for fmt in ("%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d %H:%M:%S",
                "%Y-%m-%d", "%H:%M:%S.%f", "%H:%M:%S"):
        try:
            return datetime.strptime(value, fmt)
        except:
            pass

    return value


def register_adapters():
    sqlite.register_adapter(bool, bool_adapter)
    sqlite.register_converter("BOOLEAN", bool_converter)

    sqlite.register_adapter(datetime, datetime_adapter)
    sqlite.register_adapter(date, date_adapter)
    sqlite.register_adapter(time, time_adapter)
    for n in ["DATETIME", "DATE", "TIME", "TIMESTAMP"]:
        sqlite.register_converter(n, datetime_converter)

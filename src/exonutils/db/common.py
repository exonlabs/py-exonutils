# -*- coding: utf-8 -*-
import re
import uuid

__all__ = []


def sql_identifier(name):
    name = str(name)
    if not name:
        raise ValueError("invalid empty sql identifier")

    if not re.match("^[a-zA-Z0-9_]+$", name):
        raise ValueError("invalid sql identifier [%s]" % name)

    return name


def data_mapping(mapper, data):
    for key, mapfn in mapper.items():
        if key in data:
            data[key] = mapfn(data[key])
    return data


def generate_guid():
    return uuid.uuid5(uuid.uuid1(), uuid.uuid4().hex).hex

# -*- coding: utf-8 -*-


# return package version
def get_version() -> str:
    import importlib.metadata
    return importlib.metadata.version("exonutils")

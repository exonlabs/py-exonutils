# -*- coding: utf-8 -*-
from subprocess import Popen, PIPE


# shell operations
class Shell(object):

    # exec commands and get reply
    # return tuple: (return_code, stdout, stderr)
    #  - None value: process hasnot terminated yet.
    #  - negative value -N: process terminated by signal N
    @classmethod
    def run(cls, commands, inputs=None, timeout=None):
        try:
            cmd = '; '.join(commands) \
                if type(commands) is list else commands

            p = Popen(
                cmd, stdout=PIPE, stderr=PIPE, shell=True,
                text=True, executable='/bin/bash')
            stdout, stderr = p.communicate(
                input=inputs, timeout=timeout)

            return p.returncode, stdout, stderr

        except Exception as e:
            err = str(e)

        raise RuntimeError(str(err))

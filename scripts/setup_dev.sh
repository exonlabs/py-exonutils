#!/bin/bash
cd $(dirname $(readlink -f $0))/..

SYS_PYTHON=/usr/bin/python3

SETUPENV_PATH=../venv_py3
ENV_PYTHON=${SETUPENV_PATH}/bin/python
ENV_PIP=${SETUPENV_PATH}/bin/pip


echo -e "\n* Creating DEV virtualenv using '${SYS_PYTHON}'"

if ! test -x ${SYS_PYTHON} ;then
    echo -e "\n-- Failed!! '${SYS_PYTHON}' doesn't exist\n"
    exit 1
fi

echo -e "\n- creating virtualenv ..."
${SYS_PYTHON} -m virtualenv ${SETUPENV_PATH}
if ! (test -x ${ENV_PYTHON} && test -x ${ENV_PIP}) ;then
    echo -e "\n-- Error!! failed to create virtualenv\n"
    exit 1
fi

echo -e "\n- updating virtualenv packages ..."
${ENV_PIP} install -U pip setuptools wheel

echo -e "\n- installing dev requirements ..."
if test -f requirements/dev.txt ;then
    ${ENV_PIP} install -Ur requirements/dev.txt
fi

echo -e "\n- installing in develop mode ..."
${ENV_PIP} install -e ./

echo -e "\n* Done\n"

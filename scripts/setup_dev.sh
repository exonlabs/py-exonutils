#!/bin/bash
cd $(dirname $(readlink -f $0))/..

PYTHON3=python3.7
PYTHON2=python2.7

# python3
echo -e "\n* Setup application in develop mode for Python3"
$PYTHON3 -m virtualenv ../venv3
. ../venv3/bin/activate
pip install -U pip setuptools wheel
pip install -e ./
pip install -r dev_requirements.txt
deactivate

# python2
echo -e "\n* Setup application in develop mode for Python2"
$PYTHON2 -m virtualenv ../venv2
. ../venv2/bin/activate
pip install -U pip setuptools wheel
pip install -e ./
pip install -r dev_requirements.txt
deactivate

echo -e "\n* Done\n"

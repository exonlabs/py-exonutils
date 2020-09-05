#!/bin/bash
cd $(dirname $(readlink -f $0))/..

echo -e "\n* Building Packages:"

if [ ! -z "$1" ];then
    VER=$1
    if $(git tag |grep -q "${VER}") ;then
        # check clean repo
        git diff --quiet || { echo -e "\n-- Error!! uncommitted changes in repo.\n"; exit 1; }

        # checkout to version release commit
        echo -e "\n- checking-out repo to required version release tag ..."
        git checkout ${VER}
    else
        echo -e "\n-- Error!! version tag ${VER} not found in repo.\n"
        exit 1
    fi
fi

PKGNAME=$(grep 'pkgname = "' setup.py |head -n 1 |cut -d'"' -f2 |xargs)
VERSION=$(grep '__version__ = "' ${PKGNAME}/__init__.py |head -n 1 |cut -d'"' -f2 |xargs)


for PYTHON in `cat PYTHON |xargs` ;do
    echo -e "\n- Building for $PYTHON"
    SETUPENV_PATH=../venv_$PYTHON
    . ${SETUPENV_PATH}/bin/activate
    [ -z "${VIRTUAL_ENV}" ] && { echo -e "\n-- Error!! failed to activate virtualenv.\n"; exit 1; }
    python setup.py sdist bdist_wheel clean --all
    deactivate
done

if [ ! -z "$1" ];then
    # back to master latest commit
    echo -e "\n- checking-out repo to master branch ..."
    git checkout master

    # install latest dev after version bump
    echo -e "\n- install latest dev version ..."
    PYTHON=$(head -n 1 PYTHON |xargs)
    SETUPENV_PATH=../venv_$PYTHON
    . ${SETUPENV_PATH}/bin/activate
    [ -z "${VIRTUAL_ENV}" ] && { echo -e "\n-- Error!! failed to activate $PYTHON virtualenv.\n"; exit 1; }
    pip install -e ./
    deactivate
fi

echo -e "\n* created packages: ${PKGNAME} ${VERSION}\n"

#!/bin/bash
cd $(dirname $(readlink -f $0))/..

echo -e "\n* Building Packages:"

VER=$1
if [ ! -z "${VER}" ];then
    if $(git tag |grep -q "${VER}") ;then
        # check clean repo
        git diff --quiet || {
            echo -e "\n-- Error!! uncommitted changes in repo.\n"; exit 1; }

        # checkout to version release commit
        echo -e "\n- checking-out repo to required version release tag ..."
        git checkout ${VER}
    else
        echo -e "\n-- Error!! release tag '${VER}' not found.\n"
        exit 1
    fi
fi

PKGNAME=$(grep 'pkgname = "' setup.py |head -n 1 |cut -d'"' -f2 |xargs)
VERSION=$(grep '__version__ = "' ${PKGNAME}/__init__.py |head -n 1 |cut -d'"' -f2 |xargs)

BUILD_VER=${VERSION}
echo "${BUILD_VER}" |grep -q 'dev' && {
    BUILD_VER=${BUILD_VER}$(date +%y%m%d%H%M%S)
}

# set build version
sed -i "s|^__version__ = \".*|__version__ = \"${BUILD_VER}\"|g" ${PKGNAME}/__init__.py

# create packages
for PYTHON in $(cat PYTHON |xargs) ;do
    echo -e "\n- Building for ${PYTHON}"
    make clean
    SETUPENV_PATH=../venv_${PYTHON}
    . ${SETUPENV_PATH}/bin/activate
    [ -z "${VIRTUAL_ENV}" ] && {
        echo -e "\n-- Error!! failed to activate virtualenv.\n"; exit 1; }
    python setup.py sdist bdist_wheel clean --all
    deactivate
done

# revert to original version
sed -i "s|^__version__ = \".*|__version__ = \"${VERSION}\"|g" ${PKGNAME}/__init__.py

if [ ! -z "${VER}" ];then
    # back to master latest commit
    echo -e "\n- checking-out repo to master branch ..."
    git checkout master
fi

make clean

# install latest dev after version bump
echo -e "\n- install latest dev version ..."
PYTHON=$(head -n 1 PYTHON |xargs)
SETUPENV_PATH=../venv_${PYTHON}
. ${SETUPENV_PATH}/bin/activate
[ -z "${VIRTUAL_ENV}" ] && {
    echo -e "\n-- Error!! failed to activate virtualenv.\n"; exit 1; }
pip install -e ./
deactivate

echo -e "\n* Created packages: ${PKGNAME} ${BUILD_VER}\n"

#!/bin/bash
cd $(dirname $(readlink -f $0))/..

PKGNAME=$(grep 'name = ' pyproject.toml |head -n 1 |cut -d'"' -f2 |xargs)
VERSION=$(grep 'version = ' pyproject.toml |head -n 1 |cut -d'"' -f2 |xargs)

BUILD_VER=${VERSION}
echo "${BUILD_VER}" |grep -q 'dev' && {
    BUILD_VER=${BUILD_VER}$(date +%y%m%d%H%M%S)
}

SETUPENV_PATH=$(realpath ../venv_py3)
ENV_PYTHON=${SETUPENV_PATH}/bin/python
ENV_PIP=${SETUPENV_PATH}/bin/pip

BUILD_FD=build_src
DIST_FD=dist


echo -e "\n* Building Packages:"

if ! (test -x ${ENV_PYTHON} && test -x ${ENV_PIP}) ;then
    echo -e "\n-- Error!! failed to detect virtualenv, rebuild DEV setup\n"
    exit 1
fi

rm -rf ${BUILD_FD}
mkdir -m 775 -p ${BUILD_FD}/src

cp -rf src/${PKGNAME} ${BUILD_FD}/src/
cp -rf pyproject.toml MANIFEST.in *.md *.txt examples/ ${BUILD_FD}/

# set build version
sed -i "s|^version = \".*|version = \"${BUILD_VER}\"|g" pyproject.toml

# create packages
${ENV_PYTHON} -m build ${BUILD_FD}/
if [ "$?" != "0" ]  ;then
    echo -e "\n-- Error!! failed to build packages\n"
    exit 1
fi

# revert original version
sed -i "s|^version = \".*|version = \"${VERSION}\"|g" pyproject.toml

# create dist and clean
mkdir -m 775 -p ${DIST_FD}
mv -f ${BUILD_FD}/dist/* ${DIST_FD}/
rm -rf ${BUILD_FD}

echo -e "\n* Created packages: ${PKGNAME} ${BUILD_VER}\n"

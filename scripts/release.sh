#!/bin/bash
cd $(dirname $(readlink -f $0))/..

PKGNAME=$(grep 'name = ' pyproject.toml |head -n 1 |cut -d'"' -f2 |xargs)
VERSION=$(grep 'version = ' pyproject.toml \
    |head -n 1 |cut -d'"' -f2 |xargs |sed 's|\.dev.*||g')

RELEASE_TAG=v${VERSION}

SETUPENV_PATH=../venv_py3
ENV_PYTHON=${SETUPENV_PATH}/bin/python
ENV_PIP=${SETUPENV_PATH}/bin/pip


echo -e "\n* Releasing: ${RELEASE_TAG}"

# check previous versions tags
if git tag |grep -wq "${RELEASE_TAG}" ;then
    echo -e "\n-- Error!! tag '${RELEASE_TAG}' already exists\n"
    exit 1
fi

# adjust release version
sed -i "s|^version = \".*|version = \"${VERSION}\"|g" pyproject.toml

# building release packages
if ! ./scripts/build.sh ;then
    echo -e "\n-- Error!! failed building new release packages.\n"
    exit 1
fi

# setting release tag
git commit -m "Release version '${VERSION}'" pyproject.toml
if ! git tag "${RELEASE_TAG}" ;then
    echo -e "\n-- Error!! failed adding tag '${RELEASE_TAG}'\n"
    exit 1
fi

# bump new version
NEW_VER=$(echo "${VERSION}" \
    |awk -F. '{for(i=1;i<NF;i++){printf $i"."}{printf $NF+1".dev"}}')
sed -i "s|^version = \".*|version = \"${NEW_VER}\"|g" pyproject.toml
git commit -m "Bump version to '${NEW_VER}'" pyproject.toml

# install latest dev after version bump
${ENV_PIP} install -e ./

echo -e "\n* Released: ${PKGNAME} ${VERSION}\n"

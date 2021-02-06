#!/bin/bash
cd $(dirname $(readlink -f $0))/..

PKGNAME=$(grep 'pkgname = "' setup.py |head -n 1 |cut -d'"' -f2 |xargs)
VERSION=$(grep '__version__ = "' ${PKGNAME}/__init__.py |head -n 1 |cut -d'"' -f2 |xargs |sed 's|\.dev.*||g')

RELEASE_TAG=${VERSION}

echo -e "\n* Releasing: ${RELEASE_TAG}"

# check previous versions tags
git tag |grep -q "${RELEASE_TAG}" && {
    echo -e "\n-- Error!! release tag [${RELEASE_TAG}] already exist.\n";
    exit 1;
}

# adjust version and release
sed -i "s|^__version__ = \".*|__version__ = \"${VERSION}\"|g" ${PKGNAME}/__init__.py
git commit -m "Release version '${VERSION}'" ${PKGNAME}/__init__.py
git tag "${RELEASE_TAG}" || {
    echo -e "\n-- Error!! failed adding release tag [${RELEASE_TAG}]\n";
    exit 1;
}

# bump new version
NEW_VER=$(echo "${VERSION}" |awk -F. '{for(i=1;i<NF;i++){printf $i"."}{printf $NF+1".dev"}}')
sed -i "s|^__version__ = \".*|__version__ = \"${NEW_VER}\"|g" ${PKGNAME}/__init__.py
git commit -m "Bump version to '${NEW_VER}'" ${PKGNAME}/__init__.py

# building release packages
./scripts/build.sh ${VERSION} || {
    echo -e "\n-- Error!! failed building new release packages.\n";
    exit 1;
}

echo -e "* Released: ${PKGNAME} ${VERSION}\n"

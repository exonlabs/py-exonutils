#!/bin/bash
cd $(dirname $(readlink -f $0))/..

PKGNAME=exonutils
VERSION=$(grep '__version__ = "' src/${PKGNAME}/__init__.py \
    |head -n 1 |cut -d'"' -f2 |xargs |sed 's|\.dev.*||g')

RELEASE_TAG=v${VERSION}


echo -e "\n* Releasing: ${RELEASE_TAG}"

# check previous versions tags
if git tag |grep -wq "${RELEASE_TAG}" ;then
    echo -e "\n-- Error!! tag '${RELEASE_TAG}' already exists\n"
    exit 1
fi

# adjust release version
sed -i "s|^__version__ = \".*|__version__ = \"${VERSION}\"|g" \
    src/${PKGNAME}/__init__.py

# building release packages
if ! ./scripts/build.sh ;then
    echo -e "\n-- Error!! failed building new release packages.\n"
    exit 1
fi

# setting release tag
git commit -m "Release version '${VERSION}'" src/${PKGNAME}/__init__.py
if ! git tag "${RELEASE_TAG}" ;then
    echo -e "\n-- Error!! failed adding tag '${RELEASE_TAG}'\n"
    exit 1
fi

# bump new version
NEW_VER=$(echo "${VERSION}" \
    |awk -F. '{for(i=1;i<NF;i++){printf $i"."}{printf $NF+1".dev"}}')
sed -i "s|^__version__ = \".*|__version__ = \"${NEW_VER}\"|g" \
    src/${PKGNAME}/__init__.py
git commit -m "Bump version to '${NEW_VER}'" src/${PKGNAME}/__init__.py

echo -e "* Released: ${PKGNAME} ${VERSION}\n"

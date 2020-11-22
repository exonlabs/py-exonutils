#!/bin/bash
cd $(dirname $(readlink -f $0))/..

PKGNAME=$(grep 'pkgname = "' setup.py |head -n 1 |cut -d'"' -f2 |xargs)
VERSION=$(grep '__version__ = "' ${PKGNAME}/__init__.py |head -n 1 |cut -d'"' -f2 |xargs |sed 's/\.dev0.*//g')


echo -e "\n* Releasing new version: ${VERSION}"

# check clean repo
git diff --quiet || { echo -e "\n-- Error!! uncommitted changes in repo.\n"; exit 1; }

# check previous versions tags
git tag |grep -q "${VERSION}" && { echo -e "\n-- Error!! release tag ${VERSION} already exist in repo.\n"; exit 1; }

# checkout to latest commit
echo -e "\n- checking-out repo to legacy_py2 branch ..."
git checkout legacy_py2
echo -e "\n- setting new release version ..."
sed -i "s/^__version__ = \".*/__version__ = \"${VERSION}\"/g" ${PKGNAME}/__init__.py
git commit -am "Release version '${VERSION}'"
git tag ${VERSION} || { echo -e "\n-- Error!! failed adding release tag in repo.\n"; exit 1; }

# building
./scripts/build.sh || { echo -e "\n-- Error!! failed building packages.\n"; exit 1; }

# bump version minor
echo -e "- setting new dev version ..."
NEWREL=$(echo "${VERSION}" |awk -F. '{for(i=1;i<NF;i++){printf $i"."}{printf $NF+1".dev0"}}')
sed -i "s/^__version__ = \".*/__version__ = \"${NEWREL}\"/g" ${PKGNAME}/__init__.py
git commit -am "Bump version to '${NEWREL}'"

# install latest dev after version bump
echo -e "\n- install latest dev version ..."
PYTHON=$(head -n 1 PYTHON |xargs)
SETUPENV_PATH=../venv_$PYTHON
. ${SETUPENV_PATH}/bin/activate
[ -z "${VIRTUAL_ENV}" ] && { echo -e "\n-- Error!! failed to activate $PYTHON virtualenv.\n"; exit 1; }
pip install -e ./
deactivate

echo -e "\n* Release Done: ${PKGNAME} ${VERSION}\n"

#!/bin/bash
set -euo pipefail

cd "$(dirname "$(readlink -f "$0")")/.."
source scripts/common.sh

RELEASE_VER=$(echo "${VERSION}" | sed 's|\.dev.*||g')
RELEASE_TAG=v${RELEASE_VER}

NEXT_VER=$(echo "${RELEASE_VER}" \
    |awk -F. '{for(i=1;i<NF;i++){printf $i"."}{printf $NF+1".dev"}}')

# setting version
function set_version() {
    sed -i "s|^version = \".*\"$|version = \"${1}\"|g" ${METAFILE}
}

info_msg "\nReleasing: ${PACKAGE} ver ${RELEASE_VER}"

# Check for uncommitted changes
head_msg "\nChecking for uncommitted changes ..."
if ! git diff --quiet || ! git diff --cached --quiet; then
    error_msg "Error!! Uncommitted changes detected!" \
        "Please commit or stash them before releasing.\n"
    exit 1
fi

# Check if tag already exists
head_msg "\nChecking release tags ..."
if git tag |grep -wq "${RELEASE_TAG}" ;then
    error_msg "Error!! tag '${RELEASE_TAG}' already exists\n"
    exit 1
fi

# building release packages
set_version ${RELEASE_VER}
if ! ./scripts/build.sh ;then
    error_msg "Error!! failed building new release packages.\n"
    text_msg "Reverting ..."
    git checkout -- ${METAFILE}
    exit 1
fi

# Git commit and tag for the release
head_msg "Committing and tagging release ..."
(set -x
    git add ${METAFILE}
    git commit -m "Release version ${RELEASE_VER}" ${METAFILE}
)
if ! git tag "${RELEASE_TAG}" ; then
    error_msg "Error!! Failed adding tag '${RELEASE_TAG}'\n"
    exit 1
fi

# bump to next version
head_msg "\nSetting new version ..."
set_version ${NEXT_VER}
(set -x
    git add ${METAFILE}
    git commit -m "Bump version to ${NEXT_VER}" ${METAFILE}
)

# install latest dev after version bump
head_msg "\nInstalling new version in editable (dev) mode ..."
(set -x
    "${VENV_PIP}" install -e ./[dev]
)

success_msg "\nSuccessfully released:"
text_msg "  ${PACKAGE} ${RELEASE_VER} tag (${RELEASE_TAG})"
echo -e "\n"

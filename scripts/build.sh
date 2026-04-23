#!/bin/bash
set -euo pipefail

cd "$(dirname "$(realpath -e "${BASH_SOURCE[0]}")")/.."
source environ

BUILD_VER=${VERSION}
echo "${BUILD_VER}" |grep -qE '^.*\.dev$' && {
    BUILD_VER=${BUILD_VER}$(date +%y%m%d%H%M%S)
}

BUILD_FD="build_src"
DIST_FD="dist"
PKG_FD=$(echo "${PACKAGE}" | tr "-" "_")


info_msg "\nBuilding: ${PACKAGE} ver ${BUILD_VER}"

# checking python virtualenv
head_msg "\nChecking virtualenv ..."
if ! [[ -x "${VENV_PYTHON}" && -x "${VENV_PIP}" ]]; then
    error_msg "Error!! Failed to detect virtualenv\n"
    exit 1
fi
text_msg "Found virtualenv: ${VENV_PATH}"

head_msg "\nUpdating virtualenv pip and build toolchain ..."
(set -x
    "${VENV_PIP}" install -U pip
    "${VENV_PIP}" install -U setuptools wheel build
)

head_msg "\nPreparing build directory ..."
rm -rf "${BUILD_FD}"
mkdir -m 775 -p "${BUILD_FD}/src/${PKG_FD}"
cp -rf "src/${PKG_FD}/"* "${BUILD_FD}/src/${PKG_FD}/"
cp -rf pyproject.toml MANIFEST.in *.md *.txt "${BUILD_FD}/"
[ -d examples ] && cp -rf examples/ "${BUILD_FD}/"
[ -d tests ] && cp -rf tests/ "${BUILD_FD}/"

# adjust build version
sed -i "s|^version = \".*\"$|version = \"${BUILD_VER}\"|g" \
    "${BUILD_FD}/pyproject.toml"

head_msg "\nBuilding source and wheel packages ..."
(set -x
    ${VENV_PYTHON} -m build "${BUILD_FD}/"
)
if [ "$?" != "0" ]; then
    error_msg "Error!! failed to build packages\n"
    exit 1
fi

# cleanup
mkdir -m 775 -p "${DIST_FD}"
mv -f "${BUILD_FD}/dist/"* "${DIST_FD}/"
rm -rf "${BUILD_FD}"

success_msg "\nCreated packages:"
text_msg "  ${DIST_FD}/${PACKAGE}-${BUILD_VER}.tar.gz"
text_msg "  ${DIST_FD}/${PACKAGE}-${BUILD_VER}-py3-none-any.whl"
echo -e "\n"

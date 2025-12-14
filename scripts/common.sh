#!/bin/bash

# helper functions to print messages with colors
function head_msg() { echo -e "\033[0;33m$*\033[0m"; }
function info_msg() { echo -e "\033[1;34m$*\033[0m"; }
function error_msg() { echo -e "\033[1;31m$*\033[0m"; }
function success_msg() { echo -e "\033[1;32m$*\033[0m"; }
function text_msg() { echo -e "$*"; }

# package info
METAFILE=pyproject.toml
PACKAGE=$(sed -n 's|^name = "\([^"]*\)"$|\1|p' ${METAFILE})
VERSION=$(sed -n 's|^version = "\([^"]*\)"$|\1|p' ${METAFILE})
AUTHOR=$(grep -A 1 'authors =' ${METAFILE} |sed -n 's|.*name = "\([^"]*\)".*|\1|p')


if [[ -z "${PACKAGE}" ]]; then
    error_msg "\nError!! package name not found or empty in ${METAFILE}\n"
    exit 1
fi
if [[ -z "${VERSION}" ]]; then
    error_msg "\nError!! package version not found or empty in ${METAFILE}\n"
    exit 1
fi
if [[ -z "${AUTHOR}" ]]; then
    error_msg "\nError!! package author not found or empty in ${METAFILE}\n"
    exit 1
fi

# application paths
CACHE_PATH="$(realpath -m ~/.cache/${AUTHOR}/py-dev)"
VENV_PATH="${CACHE_PATH}/venv_py3"

# venv python
VENV_PYTHON="${VENV_PATH}/bin/python3"
VENV_PIP="${VENV_PATH}/bin/pip3"

# Find latest available compatible Python (3.20 down to 3.9)
SYS_PYTHON="$(which python3)"
for i in $(seq 20 -1 9); do
    if [[ -x "${SYS_PYTHON}.${i}" ]]; then
        SYS_PYTHON="${SYS_PYTHON}.${i}"
        break
    fi
done

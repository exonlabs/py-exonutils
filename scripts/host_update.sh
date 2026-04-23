#!/bin/bash
set -euo pipefail

cd "$(dirname "$(realpath -e "${BASH_SOURCE[0]}")")/.."
source environ


info_msg "\nInstall and Update host requirements"

# checking python interpreter
head_msg "\nChecking Python interpreter ..."
if ! [[ -x "${SYS_PYTHON}" ]]; then
    error_msg "Error!! no suitable python executable found\n"
    exit 1
fi
text_msg "Found Python interpreter: ${SYS_PYTHON}"

head_msg "\nUpdating python ..."
pypkg="$(basename ${SYS_PYTHON})"
(set -x
    sudo apt update -y
    sudo apt install -y --only-upgrade ${pypkg} ${pypkg}-venv ${pypkg}-dev
)

head_msg "\nUpdating python packages ..."
pip_vars="PIP_BREAK_SYSTEM_PACKAGES=1 PIP_ROOT_USER_ACTION=ignore"
(set -x
    sudo ${pip_vars} ${SYS_PYTHON} -m pip install -U pip
    sudo ${pip_vars} ${SYS_PYTHON} -m pip install -U setuptools virtualenv
)

success_msg "\nDone\n"

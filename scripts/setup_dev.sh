#!/bin/bash
set -euo pipefail

cd "$(dirname "$(readlink -f "$0")")/.."
source scripts/common.sh


info_msg "\nSetting up development environment"

# checking python interpreter
head_msg "\nChecking Python interpreter ..."
if ! [[ -x "${SYS_PYTHON}" ]]; then
    error_msg "Error!! no suitable python executable found\n"
    exit 1
fi
text_msg "Using Python interpreter: ${SYS_PYTHON}"

# checking python virtualenv package
if ! "${SYS_PYTHON}" -m virtualenv --version &>/dev/null; then
    error_msg "Error!! failed checking 'python -m virtualenv --version'\n"
    exit 1
fi

head_msg "\nCreating virtualenv at ${VENV_PATH} ..."
(set -x
    "${SYS_PYTHON}" -m virtualenv "${VENV_PATH}"
)
if ! [[ -x "${VENV_PYTHON}" && -x "${VENV_PIP}" ]]; then
    error_msg "Error!! Failed to create virtualenv\n"
    exit 1
fi
(set -x
    "${VENV_PIP}" install -U pip
    "${VENV_PIP}" install -U setuptools wheel build
)

head_msg "\nInstalling project in editable (dev) mode ..."
(set -x
    "${VENV_PIP}" install -e ./[dev]
)

success_msg "\nDevelopment environment is ready"
text_msg "To activate run:\n    source ${VENV_PATH}/bin/activate\n"

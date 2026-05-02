#!/bin/bash
set -euo pipefail

cd "$(dirname "$(realpath -e "${BASH_SOURCE[0]}")")/.."

ENV_FILE="$(pwd)/.env"

# handle .env before loading environ
if [ -f "${ENV_FILE}" ]; then
    echo -e "\nFound existing .env file:"
    echo "--------------------------------------------------"
    cat "${ENV_FILE}"
    echo "--------------------------------------------------"
    read -rp "  [U]se / [D]elete / [A]bort ? [U]: " _choice || true
    case "${_choice,,}" in
        a|A)
            echo "Aborted."
            exit 0
            ;;
        d|D)
            rm -f "${ENV_FILE}"
            echo "Deleted .env"
            ;;
        *)
            echo "Using existing .env"
            ;;
    esac
fi

if [ ! -f "${ENV_FILE}" ]; then
    _default_venv="$(pwd)/.venv"
    echo -e "\nNo .env file found. Default settings:"
    echo "--------------------------------------------------"
    echo "VENV_PATH=\"${_default_venv}\""
    echo "--------------------------------------------------"
    read -rp "  [C]reate / [S]kip / [A]bort ? [C]: " _choice || true
    case "${_choice,,}" in
        a|A)
            echo "Aborted."
            exit 0
            ;;
        s|S)
            echo "Skipping .env creation."
            ;;
        *)
            echo "VENV_PATH=\"${_default_venv}\"" > "${ENV_FILE}"
            echo "Created .env"
            ;;
    esac
fi

source environ

info_msg "\nSetting up development environment"

# python interpreter
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
    "${VENV_PIP}" install -U setuptools wheel build twine
)

head_msg "\nInstalling project in editable (dev) mode ..."
(set -x
    "${VENV_PIP}" install -e ".[dev,docs]"
)

success_msg "\nDevelopment environment is ready"
text_msg "To activate run:\n    source ${VENV_PATH}/bin/activate\n"

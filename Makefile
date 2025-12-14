.DEFAULT_GOAL := help

SHELL := /bin/bash

METAFILE := pyproject.toml
PACKAGE := $(shell sed -n 's|^name = "\([^"]*\)"$$|\1|p' $(METAFILE))
AUTHOR := $(shell grep -A 1 'authors =' $(METAFILE) |sed -n 's|.*name = "\([^"]*\)".*|\1|p')
VENV_BIN := $(shell realpath -m ~/.cache/$(AUTHOR)/py-dev/venv_py3/bin)

# Color defs
C_RESET = \033[0m
C_HEAD = \033[0;33m
C_INFO = \033[1;34m
C_ERR = \033[1;31m
C_OK = \033[1;32m

.PHONY: help
## Show this help message
help:
	@echo -e "\n$(C_HEAD)Available targets:$(C_RESET)"
	@awk '/^##/{sub(/^##[ ]*/,"",$$0);c=$$0;next}/^[A-Za-z0-9._-]+:([^=]|$$)/ \
		{if(c){t=$$1;sub(/:/,"",t);printf"  $(C_INFO)%-15s$(C_RESET) \
		%s\n",t,c}c="";next}/^[^#]/{c=""}' $(MAKEFILE_LIST)
	@echo -e "\n"

.PHONY: clean
## Cleaning build and cache files
clean:
	@rm -rf build*/ .pytest*/
	@find . -type d -name '__pycache__' -exec rm -rf {} +
	@find . -type f -name '*.pyc' -exec rm -f {} +

.PHONY: clean-dist
## Cleaning dist files
clean-dist:
	@rm -rf dist/

.PHONY: clean-all
## Clean all build, dist and cache files
clean-all: clean clean-dist
	@echo -e "$(C_HEAD)Clean all build, dist and cache files ...$(C_RESET)"
	@find . -type d -name '*.egg-info' -exec rm -rf {} +
	@find . -type d -name '*.dist-info' -exec rm -rf {} +

.PHONY: host-update
## Install and Update host requirements
host-update:
	@bash scripts/host_update.sh

.PHONY: setup-dev
## Create development environment setup
setup-dev: clean-all
	@bash scripts/setup_dev.sh

.PHONY: pip-update
## Update virtualenv pip and installed packages
pip-update:
	@echo -e "\n$(C_INFO)Update virtualenv packages ...$(C_RESET)"
	@bash -c "$(VENV_BIN)/pip3 install -U pip"
	@bash -c "$(VENV_BIN)/pip3 freeze |sed -n 's|^\(.*\)==.*$$|\1|p' \
		|xargs -r $(VENV_BIN)/pip3 install -U"
	@echo -e "\n$(C_OK)Done$(C_RESET)\n"

.PHONY: auto-format
## Auto-format (black) Python code, tests and examples
auto-format:
	@echo -e "\n$(C_INFO)Auto-format Python code with black ...$(C_RESET)"
	@bash -c "$(VENV_BIN)/black src/$(PACKAGE)/ tests/ examples/"
	@echo -e "\n"

.PHONY: lint-all
## Run Python linters (flake8) on code, tests and examples
lint-all:
	@echo -e "\n$(C_INFO)Running flake8 linters ...$(C_RESET)"
	@bash -c "$(VENV_BIN)/flake8 src/$(PACKAGE) tests/ examples/"
	@echo -e "\n"

.PHONY: run-tests
## Run all project tests
run-tests:
	@echo -e "\n$(C_INFO)Running tests ...$(C_RESET)"
	@bash -c "$(VENV_BIN)/pytest tests/"
	@echo -e "\n"

.PHONY: build
## Build the project packages
build: clean
	@bash scripts/build.sh

.PHONY: release
## Prepare and build a release packages
release: clean
	@bash scripts/release.sh

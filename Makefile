.DEFAULT_GOAL := help

.ONESHELL:
SHELL := /bin/bash


.PHONY: help
## Show this help message
help:
	@source environ
	@head_msg "\nAvailable targets:"
	@awk '/^##/{sub(/^##[ ]*/,"",$$0);c=$$0;next}/^[A-Za-z0-9._-]+:([^=]|$$)/ \
		{if(c){t=$$1;sub(/:/,"",t);printf"  %-20s%s\n",t,c}c="";next} \
		/^[^#]/{c=""}' $(MAKEFILE_LIST)
	@echo -e "\n"

.PHONY: clean
## Clean build and cache files
clean:
	@rm -rf build*/ .pytest*/
	@find . -type d -name '__pycache__' -exec rm -rf {} +
	@find . -type f -name '*.pyc' -exec rm -f {} +

.PHONY: clean-dist
## Clean dist files
clean-dist:
	@rm -rf dist/

.PHONY: clean-all
## Clean all build, dist and cache files
clean-all: clean clean-dist
	@source environ
	@head_msg "Cleaning all build, dist and cache files ..."
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
	@source environ
	@info_msg "\nUpdate virtualenv packages ..."
	@bash -c "$${VENV_PIP} install -U pip"
	@bash -c "$${VENV_PIP} freeze |sed -n 's|^\(.*\)==.*$$|\1|p' \
		|xargs -r $${VENV_PIP} install -U"
	@echo -e "\n"

.PHONY: auto-format
## Auto-format (black) Python code, tests and examples
auto-format:
	@source environ
	@info_msg "\nAuto-format Python code with (black) ..."
	@bash -c "$${VENV_PATH}/bin/black src/$${PACKAGE}/ tests/ examples/"
	@echo -e "\n"

.PHONY: lint-all
## Run Python linters (flake8) on code, tests and examples
lint-all:
	@source environ
	@info_msg "\nRunning flake8 linters ..."
	@bash -c "$${VENV_PATH}/bin/flake8 src/$${PACKAGE} tests/ examples/"
	@echo -e "\n"

.PHONY: run-tests
## Run all project tests
run-tests:
	@source environ
	@info_msg "\nRunning tests ..."
	@bash -c "$${VENV_PATH}/bin/pytest tests/"
	@echo -e "\n"

.PHONY: build
## Build the project packages
build: clean
	@bash scripts/build.sh

.PHONY: release
## Prepare and build a release packages
release: clean
	@bash scripts/release.sh

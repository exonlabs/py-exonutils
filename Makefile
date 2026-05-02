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
	@rm -rf build*/ site*/ .pytest*/
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
## Auto-format (ruff) Python code, tests and examples
auto-format:
	@source environ
	@info_msg "\nAuto-format Python code with (ruff) ..."
	@bash -c "$${VENV_PATH}/bin/ruff format src/$${PACKAGE}/ tests/ \
    	$$([ -d examples ] && echo examples/ || true)"
	@echo -e "\n"

.PHONY: lint-all
## Run Python linters (ruff) on code, tests and examples
lint-all:
	@source environ
	@info_msg "\nRunning ruff linters ..."
	@bash -c "$${VENV_PATH}/bin/ruff check src/$${PACKAGE} tests/ \
    	$$([ -d examples ] && echo examples/ || true)"
	@echo -e "\n"

.PHONY: type-check
## Run type checker (mypy) on code
type-check:
	@source environ
	@info_msg "\nRunning mypy type checker ..."
	@bash -c "$${VENV_PATH}/bin/mypy src/$${PACKAGE}/"
	@echo -e "\n"

.PHONY: run-tests
## Run all project tests
run-tests:
	@source environ
	@info_msg "\nRunning tests ..."
	@bash -c "$${VENV_PATH}/bin/pytest \
		--cov=$${PACKAGE} --cov-report=term-missing tests/"
	@echo -e "\n"

.PHONY: check
## Run lint, type check and tests
check: lint-all type-check run-tests

.PHONY: build
## Build the project packages
build: clean
	@bash scripts/build.sh

.PHONY: release
## Prepare and build a release packages
release: clean
	@bash scripts/release.sh

.PHONY: docs-build
## Build static docs site
docs-build:
	@source environ
	@info_msg "\nBuilding docs ..."
	@rm -rf site*/
	@bash -c "$${VENV_PATH}/bin/mkdocs build --clean"
	@echo -e "\n"

.PHONY: docs-deploy
## Deploy versioned docs with mike (usage: make docs-deploy VER=X.Y [ALIAS=latest])
docs-deploy:
	@source environ
	@[ -n "$${VER}" ] || { error_msg "\nError!! VER is required"; \
		text_msg "usage: make docs-deploy VER=X.Y [ALIAS=latest]\n"; exit 1; }
	@info_msg "\nDeploying docs version $${VER} ..."
	@bash -c "PATH=$${VENV_PATH}/bin:$$PATH \
		mike deploy --branch wiki --update-aliases $${VER} $${ALIAS}"
	@bash -c "$${VENV_PATH}/bin/mike set-default --branch wiki latest"
	@echo -e "\n"

.PHONY: docs-serve
## Serve docs locally for preview
docs-serve:
	@source environ
	@info_msg "\nServing docs locally ..."
	@bash -c "$${VENV_PATH}/bin/mike serve --branch wiki"
	@echo -e "\n"

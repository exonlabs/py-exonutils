
SHELL := /bin/bash


.PHONY: clean
clean:
	@rm -rf build/ build_src/
	@find . -type d -name '__pycache__' -exec rm -rf {} +
	@find . -type f -name '*.pyc' -exec rm -f {} +

.PHONY: clean-dist
clean-dist:
	@rm -rf dist/

.PHONY: clean-dev
clean-dev: clean
	@find . -type d -name '*.egg-info' -exec rm -rf {} +
	@find . -type d -name '*.dist-info' -exec rm -rf {} +

.PHONY: clean-all
clean-all: clean-dev clean-dist

.PHONY: setup-dev
setup-dev: clean-dev
	@bash scripts/setup_dev.sh

.PHONY: build
build: clean
	@bash scripts/build.sh

.PHONY: release
release: clean
	@bash scripts/release.sh

.PHONY: pip-update
pip-update:
	pip install -U pip $$(pip freeze |grep -v '-e ' |cut -d'=' -f1 |xargs)

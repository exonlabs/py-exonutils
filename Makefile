.PHONY: clean clean-dist clean-dev clean-all setup-dev build


clean:
	@find . -type d -name '__pycache__' -exec rm -rf {} +
	@find . -type f -name '*.pyc' -exec rm -f {} +
	@rm -rf build/

clean-dist:
	@rm -rf dist/

clean-dev: clean
	@rm -rf *.egg-info/ *.dist-info/

clean-all: clean-dev clean-dist

setup-dev: clean-dev
	pip install -e ./

build: clean
	python setup.py sdist bdist_wheel clean --all

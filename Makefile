SHELL := /bin/bash

REPO := https://github.com/sr-murthy/continuedfractions

PACKAGE_NAME := continuedfractions
BRANCH := $(shell git rev-parse --abbrev-ref HEAD)
HEAD := $(shell git rev-parse --short=8 HEAD)
PACKAGE_VERSION := $(shell grep __version__ src/version.py | cut -d '=' -f 2 | xargs)

ROOT := $(PWD)

TESTS_ROOT := $(ROOT)/tests


# Make everything (possible)
all:

# Git
git_stage:
	@echo "\n$(PACKAGE_NAME)[$(BRANCH)@$(HEAD)]: Staging new, modified, deleted and/or renamed files in Git\n"
	git status -uno | grep modified | tr -s ' ' | cut -d ' ' -f 2 | xargs git add && \
	git status -uno | grep deleted | tr -s ' ' | cut -d ' ' -f 2 | xargs git add -A && \
	git status -uno

# Housekeeping
clean:
	@echo "\n$(PACKAGE_NAME)[$(BRANCH)@$(HEAD)]: Deleting all temporary files\n"
	rm -fr docs/_build/* .pytest_cache *.pyc *__pycache__* ./dist/* ./build/* *.egg-info*

# A simple version check for the installed package (local, sdist or wheel)
version_check:
	@echo "\n$(PACKAGE_NAME)[$(BRANCH)@$(HEAD)]: Checking installed package version (if it is installed)\n"
	python3 -c "import os; os.chdir('src'); from version import __version__; print(__version__); os.chdir('../')"

version_extract:
	echo "$(PACKAGE_VERSION)"

# Running tests
test_docstrings: clean
	@echo "\n$(PACKAGE_NAME)[$(BRANCH)@$(HEAD)]: Running doctests in all core libraries\n"
	cd "$(PROJECT_ROOT)" && \
	python -m doctest --verbose src/continuedfractions/*.py

test_units: clean
	@echo "\n$(PACKAGE_NAME)[$(BRANCH)@$(HEAD)]: Running package unit tests + measuring coverage\n"
	cd "$(PROJECT_ROOT)" && \
	python -m \
		coverage run --branch --source=src \
		-m pytest \
			--cache-clear \
			--capture=no \
			--code-highlight=yes \
			--color=yes \
			--tb=native \
			--verbosity=3 \
 		tests/units \
 	&& \
 	python -m coverage report --skip-empty --show-missing --omit="*/tests*" --precision=3

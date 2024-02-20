SHELL := /bin/bash

REPO := https://github.com/sr-murthy/continuedfractions

PACKAGE_NAME := continuedfractions
BRANCH := $(shell git rev-parse --abbrev-ref HEAD)
HEAD := $(shell git rev-parse --short=8 HEAD)
PACKAGE_VERSION := $(shell grep __version__ src/continuedfractions/version.py | cut -d '=' -f 2 | xargs)

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

# Linting
lint: clean
	@echo "\n$(PACKAGE_NAME)[$(BRANCH)@$(HEAD)]: Linting source code with Ruff\n"
	cd "$(PROJECT_ROOT)" && ruff check

# Running tests
doctests: clean
	@echo "\n$(PACKAGE_NAME)[$(BRANCH)@$(HEAD)]: Running doctests in all core libraries\n"
	cd "$(PROJECT_ROOT)" && \
	python3 -m doctest --verbose src/continuedfractions/*.py

unittests: clean
	@echo "\n$(PACKAGE_NAME)[$(BRANCH)@$(HEAD)]: Running package unit tests + measuring coverage\n"
	cd "$(PROJECT_ROOT)" && \
	python3 -m pytest \
				--cache-clear \
				--capture=no \
				--code-highlight=yes \
				--color=yes \
				--cov=src \
				--cov-report=term-missing:skip-covered \
				--dist worksteal \
				--numprocesses=auto \
				--tb=native \
				--verbosity=3 \
				tests/units

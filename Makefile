SHELL := /bin/bash

REPO := https://github.com/sr-murthy/tenpins

PACKAGE_NAME := tenpins
BRANCH := $(shell git rev-parse --abbrev-ref HEAD)
HEAD := $(shell git rev-parse --short=8 HEAD)
PACKAGE_VERSION := $(shell grep __version__ src/__version__.py | cut -d '=' -f 2 | xargs)

ROOT := $(PWD)

TESTS_ROOT := $(ROOT)/tests

# The TESTS_ENV env. variable is used to indicate whether tests are being run
# in an upstream CI environment (set a value of "ci" in this case), or locally
# (set a value of "local" if running locally, but it could be anything other
# than "ci").
ifeq "$(TEST_ENV)" "ci"
	# This branch assumes that the runner has at least  22 cores available - 
	# check the monorepo runner settings.
	#
	# NOTE: when trying to use cores on a multi-core host do not try to use all
	# available cores,  as it can overload the host. Try to follow a 75% core
	# utilisation rule - the number of cores used for tests should not exceed
	# 75% of all available cores on the host.
	TESTS_NUMPROCESSES := 4
else
	TESTS_NUMPROCESSES := 1
endif

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
	rm -fr docs/_build/* .pytest_cache *.pyc *__pycache__* ./dist/* ./build/* *.egg-info* *.log batch-inference-input*.json*

# A simple version check for the installed package (local, sdist or wheel)
version_check:
	@echo "\n$(PACKAGE_NAME)[$(BRANCH)@$(HEAD)]: Checking installed package version (if it is installed)\n"
	python3 -c "import os; os.chdir('src'); from __version__ import __version__; print(__version__); os.chdir('../')"

version_extract:
	echo "$(PACKAGE_VERSION)"

# Running tests
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
			--doctest-modules \
			--tb=native \
			--verbosity=3 \
 		tests/units \
 	&& \
 	python -m coverage report --skip-empty --show-missing --omit="*/tests*" --precision=3

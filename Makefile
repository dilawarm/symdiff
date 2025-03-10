.PHONY: check clean-pycache distclean black isort test format fix
SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c
.DELETE_ON_ERROR:
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules
PROJECT_DIRS = symdiff tests

install:
	uv venv
	source .venv/bin/activate
	uv lock
	uv sync

check: black isort

black:
	@echo "============================== Black formatting check ==================="
	black --check $(PROJECT_DIRS)

isort:
	@echo "============================== Import sorting check ==================="
	isort --check $(PROJECT_DIRS)

fix: format

format:
	@echo "============================== Formatting code ========================="
	black $(PROJECT_DIRS)
	isort $(PROJECT_DIRS)

test:
	py.test -vv

coverage:
	@echo "============================== Tests =============================="
	py.test -vv --cov --junitxml=.out/test_results.xml --cov-report "xml:.out/coverage.xml"

requirements:
	uv export --no-hashes --no-dev > requirements.txt
	uv export --no-hashes > requirements-test.txt

clean-pycache:
	find . -type d -name '__pycache__' -print0 | xargs -0 -I {} /bin/rm -rf "{}"

distclean: clean-pycache
	rm -rf dist

badges:
	make coverage
	genbadge tests -i .out/test_results.xml -o .html/badges/tests-badge.svg
	genbadge coverage -i .out/coverage.xml -o .html/badges/coverage-badge.svg
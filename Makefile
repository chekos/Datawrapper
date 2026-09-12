.DEFAULT_GOAL := help

UV ?= uv
UV_PYTHON ?=
PYTHON ?= python3
PACKAGE ?= datawrapper
COVERAGE_FAIL_UNDER ?= 80
TEST_ARGS ?=
RUN = $(if $(UV_PYTHON),UV_PYTHON=$(UV_PYTHON)) $(UV) run

.PHONY: all help bootstrap install install-all install-dev install-test install-docs check verify diff-check lint format-check format fix type-check dependency-check workflow-check manifest-check test test-serial test-parallel coverage build package-check package-verify docs docs-check linkcheck build-docs serve-docs hooks clean

help: ## Show available commands
	@awk 'BEGIN {FS = ":.*## "}; /^[a-zA-Z0-9_-]+:.*## / {printf "%-18s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

bootstrap: ## Prepare this checkout and install locked dependencies
	$(PYTHON) scripts/worktree_bootstrap.py --uv "$(UV)"

install: install-all ## Install all development dependencies

install-all: ## Install every dependency group
	$(UV) sync --all-groups --locked

install-dev: ## Install dependencies for static checks
	$(UV) sync --group dev --locked

install-test: ## Install dependencies for tests
	$(UV) sync --group test --locked $(if $(UV_PYTHON),--python $(UV_PYTHON))

install-docs: ## Install dependencies for documentation
	$(UV) sync --group docs --locked

all: verify ## Run the complete verification suite

check: diff-check lint format-check type-check dependency-check workflow-check ## Run fast, non-mutating code checks

verify: check test manifest-check build docs-check ## Run all local CI checks

diff-check: ## Check the diff for whitespace errors
	git diff --check

lint: ## Check code with Ruff
	$(RUN) ruff check

format-check: ## Check formatting with Ruff
	$(RUN) ruff format --check

format: ## Format code with Ruff
	$(RUN) ruff format

fix: ## Apply Ruff lint fixes and formatting
	$(RUN) ruff check --fix
	$(RUN) ruff format

type-check: ## Check static types with ty
	$(RUN) ty check

dependency-check: ## Check dependency declarations with Deptry
	$(RUN) deptry .

workflow-check: ## Audit GitHub Actions workflows with Zizmor
	$(RUN) zizmor .github/workflows

manifest-check: ## Check source distribution contents
	$(RUN) check-manifest

test: ## Run tests serially
	$(RUN) pytest $(TEST_ARGS)

test-serial: test ## Run tests without parallel workers

test-parallel: ## Run tests with parallel workers
	$(RUN) pytest -n auto $(TEST_ARGS)

coverage: ## Enforce coverage for PACKAGE
	@test -n "$(PACKAGE)" || { echo "Set PACKAGE to the library import name."; exit 2; }
	$(RUN) pytest $(TEST_ARGS) --cov="$(PACKAGE)" --cov-branch --cov-report=term-missing:skip-covered --cov-fail-under="$(COVERAGE_FAIL_UNDER)"

build: ## Build source and wheel distributions
	rm -rf dist
	$(UV) build --sdist --wheel
	$(RUN) twine check dist/*

package-check: ## Build, install, and import PACKAGE in an isolated environment
	@test -n "$(PACKAGE)" || { echo "Set PACKAGE to the library import name."; exit 2; }
	@temp_dir=$$(mktemp -d); trap 'rm -rf "$$temp_dir"' EXIT; \
	$(UV) build --wheel --out-dir "$$temp_dir/dist"; \
	$(RUN) check-wheel-contents "$$temp_dir"/dist/*.whl; \
	$(UV) venv --no-project "$$temp_dir/venv"; \
	$(UV) pip install --python "$$temp_dir/venv/bin/python" "$$temp_dir"/dist/*.whl; \
	cd "$$temp_dir" && "$$temp_dir/venv/bin/python" -c 'import importlib; importlib.import_module("$(PACKAGE)")'

package-verify: package-check coverage ## Run package import and coverage checks

docs: ## Build HTML documentation
	$(RUN) sphinx-build -M html docs docs/_build

docs-check: ## Build documentation and fail on warnings
	$(RUN) sphinx-build -M html docs docs/_build -W --keep-going

linkcheck: ## Check documentation links and fail on warnings
	$(RUN) sphinx-build -M linkcheck docs docs/_build -W --keep-going

build-docs: docs ## Build HTML documentation

serve-docs: ## Serve documentation with live reload
	$(RUN) sphinx-autobuild -b html docs docs/_build/html

hooks: ## Run all pre-commit hooks (may modify files)
	$(RUN) pre-commit run --all-files

clean: ## Remove generated files and caches
	rm -rf build dist docs/_build docs/_build_html .coverage htmlcov .pytest_cache .ruff_cache .ty coverage.xml
	find . -maxdepth 1 -type d -name "*.egg-info" -prune -exec rm -rf {} +
	find . -path ./.venv -prune -o -type d -name __pycache__ -prune -exec rm -rf {} +

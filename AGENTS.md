# Agent guide for Datawrapper

This repository is friendly to AI-assisted edits, but agents should stay inside the same guardrails as human contributors.

## Start here

1. Read `README.md`, `CONTRIBUTING.md`, and this file before changing code.
2. Work from the latest `main` branch unless the maintainer tells you otherwise.
3. Keep pull requests focused. Do not mix dependency upgrades, broad refactors, generated artifacts, and product changes in one PR.
4. Prefer the object-oriented chart API (`BarChart`, `LineChart`, `get_chart`, etc.) for new work. Treat lower-level `Datawrapper` methods as legacy compatibility paths unless a task explicitly targets them.

## Canonical local commands

Install the locked dependencies:

```bash
uv sync --frozen --all-extras
```

Run the same deterministic checks expected before a PR:

```bash
uv run ruff check ./datawrapper ./tests
uv run ruff format --check ./datawrapper ./tests
uv run mypy ./datawrapper --ignore-missing-imports
uv run pytest
uv build --sdist --wheel
```

Before committing, run the hook suite against all files:

```bash
uv run pre-commit run --all-files
```

## Test strategy

- Put fast, isolated validation in `tests/unit/`.
- Put mocked multi-component behavior in `tests/integration/` or `tests/functional/`.
- Mark tests that require the real Datawrapper API with `@pytest.mark.api` and a `DATAWRAPPER_ACCESS_TOKEN` skip guard. The default local and CI test runs must pass without credentials.
- Prefer `responses`, `pytest-mock`, or `unittest.mock` over live HTTP calls for regression tests.
- When fixing a bug, add a regression test that would fail before the fix.

## Change boundaries

- Do not commit `.venv/`, `.ruff_cache/`, `.mypy_cache/`, `htmlcov/`, `coverage.xml`, `dist/`, or other generated outputs.
- Do not edit `uv.lock` or dependency constraints unless the task is explicitly about dependency maintenance.
- Do not add secrets, API tokens, recordings of API responses containing private data, or maintainer-specific local configuration.
- Do not publish releases, merge pull requests, or change repository settings.

## AI-specific safety checks

Agents commonly make mistakes in this codebase by using stale legacy examples, weakening CI to make failures disappear, or adding broad generated documentation. Avoid those shortcuts. If a check is too slow or flaky, document the evidence in the PR and choose the strongest practical alternative instead of disabling it silently.

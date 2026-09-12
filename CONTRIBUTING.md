# How to contribute

Thanks for helping improve `datawrapper`. Please keep changes focused and easy to review.

## Dependencies

Clone the repository and move into it on your terminal.

Install the locked development dependencies with `uv`:

```sh
make bootstrap
```

Install pre-commit to run quick local guardrails before each commit:

```sh
uv run pre-commit install
```

You can also run the full hook suite manually:

```sh
uv run pre-commit run --all-files
```

## Tests and checks

Run the full local validation suite before opening a pull request:

```bash
make check   # ruff lint/format, ty, deptry, zizmor
make test    # pytest
make build   # sdist and wheel
```

We enforce ruff for linting and formatting, and [ty](https://github.com/astral-sh/ty) for static
typing; both are handled via pre-commit (ty on push). You can run either manually:

```bash
uv run ruff check
uv run ty check
```

See `AGENTS.md` for the full set of `make` targets, including `make check` (fast, non-mutating
checks) and `make verify` (the full local CI suite).

For quicker iteration, run targeted tests first, then finish with the full suite:

```bash
uv run pytest tests/unit/test_flags.py
uv run pytest tests/functional/test_chart_factory.py -k unsupported
```

## Test strategy

- Add or update tests for behavior changes and bug fixes.
- Keep the default test suite deterministic and credential-free. Tests that call the live
  Datawrapper API must be marked `@pytest.mark.api` and skipped unless `DATAWRAPPER_ACCESS_TOKEN`
  is set.
- Prefer mocked HTTP tests with `responses`, `pytest-mock`, or `unittest.mock` for regression
  coverage.
- Put fast isolated tests in `tests/unit/`, mocked multi-component tests in `tests/integration/`
  or `tests/functional/`, and real API smoke tests behind the `api` marker.

## Before submitting

Before submitting your code please do the following steps:

1. Keep the change scoped to one purpose.
2. Add tests for the new or changed behavior.
3. Update documentation when user-facing behavior, setup, or commands change.
4. Run the full validation suite listed above.
5. Confirm you did not commit generated artifacts such as `.venv/`, `.ruff_cache/`, `.pytest_cache/`,
   `.ty/`, `htmlcov/`, `coverage.xml`, or `dist/`.

## Guidance for AI agents

AI-assisted pull requests are welcome when they follow the same contribution rules. Agents should
also read `AGENTS.md` before editing. Do not weaken linting, type checks, tests, or CI to hide
failures; if a check is impractical, explain the evidence and choose the strongest practical
alternative.

Now you're ready to submit your pull request.

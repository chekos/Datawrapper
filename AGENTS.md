# Agent Guide

This repository is a lightweight Python wrapper for the Datawrapper API. It
ships a single importable package, `datawrapper/`, with an object-oriented
chart API (`datawrapper.charts`) and a lower-level legacy client
(`datawrapper.Datawrapper`).

See `.clinerules` for the library's internal design conventions (the
object-oriented chart API, serialization/deserialization patterns, annotation
mixins, and other code-level guidance). This file covers repository structure
and the development/CI workflow instead.

## Repository Structure

- `datawrapper/`: The published package. `datawrapper/charts/` holds the
  chart classes; `datawrapper/__main__.py` is the CLI entry point.
- `tests/`: Unit, integration, and functional tests, organized under
  `tests/unit/`, `tests/integration/`, and `tests/functional/`.
- `docs/`: Sphinx documentation source, published to Read the Docs.
- `.github/workflows/`: Continuous integration, documentation, CodeQL, and
  Scorecard workflows.
- `Makefile`: Common development and verification commands.

## Development Workflow

Install dependencies with:

```sh
make bootstrap
```

The bootstrap uses Git metadata to identify the primary checkout. In a linked
worktree, it can share the primary checkout's ignored `.env` and creates an
ignored `.env.worktree` with a stable `WORKTREE_ID`.

Use these commands while making changes:

```sh
make check   # Fast, non-mutating lint, format, and type checks
make verify  # Full local CI suite: checks, tests, build, and docs
make test-serial  # Debug tests without parallel workers
make test-parallel  # Use for the full, independent test suite
```

Use `make fix` or `make format` only when changes to source files are
intended. `make hooks` may also modify files.

## Worktrees and Parallel Agents

- Edit only the current checkout. Never modify the primary checkout or sibling
  worktrees.
- Avoid broad clean, reset, or delete operations. Do not stop services that may
  be shared with another checkout or agent.
- Coordinate ownership of conflict-prone files such as lockfiles, schemas,
  and generated artifacts (`docs/_build*`, `htmlcov/`, `coverage.xml`).
- `pytest-xdist` runs tests in parallel, but it does not isolate external
  resources across worktrees. Give each worktree separate ports, caches, or
  containers when tests use them.

## Type Checking

Static types are checked with `ty` (`make type-check`), configured in
`[tool.ty]` in `pyproject.toml`. Prefer precise type hints over `Any`; add
`# ty: ignore[...]` comments only with a reason.

## Documentation

Document the package's public behavior in the Sphinx source under `docs/`.
Update it with every user-facing API or behavior change, and build it with
`make docs-check`. Documentation is published by Read the Docs from
`.readthedocs.yaml`, not by a GitHub Actions deploy step — a push to `main`
triggers a Read the Docs build automatically.

## Changelog

For user-facing behavior, compatibility, or security changes, add a concise
entry under the appropriate `Unreleased` category in `CHANGELOG.md`. Do not
add entries for internal-only changes. Maintainers move entries into versioned
release sections.

## Releases

Follow `RELEASING.md` for the full checklist. The routine order is: merge the
approved release PR, confirm the exact version tag resolves to its merge
commit, obtain explicit approval for the tag-triggered package publication,
then create a public GitHub Release from that existing tag with concise
changelog-based notes. Agents may prepare release notes and validate a
release, but must not create tags, releases, or package publications without
explicit human approval.

## Change Guidelines

- Keep production code, tests, package configuration, and documentation aligned.
- Add tests for new library behavior under `tests/`.
- Use the configured Ruff and ty checks; do not introduce duplicate tooling
  without a project need.
- Copy `.env.example` to `.env` or use `make bootstrap` in a linked worktree.
  Do not commit generated build output, virtual environments, `.env` files,
  `.env.worktree`, or credentials.

# Changelog

All notable changes to this project are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

- Adopt the `palewire/python-open-source-template` development and agentic
  tooling: `AGENTS.md`, an expanded `Makefile`, PEP 735 `dependency-groups`,
  `ty` type checking, `deptry`, `zizmor`, `check-manifest`, and expanded
  pre-commit hooks (secrets/spelling/workflow-lint checks).
- Add CodeQL and OpenSSF Scorecard security-scanning workflows, issue/PR
  templates, and `CODEOWNERS`.

### Changed

- Replace `mypy` with [`ty`](https://github.com/astral-sh/ty) as the static
  type checker.

### Fixed

- Read chart data separated by semicolons, tabs or pipes, not only commas.
  `Datawrapper.get()` parsed every CSV response with a comma, so charts with
  semicolon-separated data could not be fetched, and tab-separated data (what
  the editor stores when you paste from a spreadsheet) came back as a single
  column. `get()` and `BaseChart.deserialize_data()` now share a
  `read_csv()` helper that sniffs the delimiter from the first lines.
- Name columns with a blank header `X.1`, `X.2`, ... as Datawrapper does,
  instead of pandas' `Unnamed: 1`, so a chart's settings that refer to them
  (`axes`, `column-format`) still match after `update()`.

### Removed

- Remove the unused `rich` and `exceptiongroup` runtime dependencies.
- Remove the `mypy` optional dependency group (superseded by the `ty` entry
  in the `dev` dependency group).

### Security

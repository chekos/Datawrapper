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

- Send each column's `number-format` in `ColumnFormatList`. The serializer
  dropped it along with the default values, so a column's number or date
  format was lost on create, and on every `update()` of a fetched chart.

### Removed

- Remove the unused `rich` and `exceptiongroup` runtime dependencies.
- Remove the `mypy` optional dependency group (superseded by the `ty` entry
  in the `dev` dependency group).

### Security

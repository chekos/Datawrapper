# datawrapper

<div align="center">

[![PyPI Version](https://img.shields.io/pypi/v/datawrapper.svg)](https://pypi.python.org/pypi/datawrapper)
[![Monthly downloads](https://img.shields.io/pypi/dm/datawrapper)](https://img.shields.io/pypi/dm/datawrappe)
[![Build status](https://github.com/chekos/datawrapper/workflows/build/badge.svg?branch=master&event=push)](https://github.com/chekos/datawrapper/actions?query=workflow%3Abuild)
[![Python Version](https://img.shields.io/pypi/pyversions/datawrapper.svg)](https://pypi.org/project/datawrapper/)
[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/chekos/datawrapper/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/chekos/datawrapper/blob/master/.pre-commit-config.yaml)
[![Semantic Versions](https://img.shields.io/badge/%F0%9F%9A%80-semantic%20versions-informational.svg)](https://github.com/chekos/datawrapper/releases)
[![License](https://img.shields.io/github/license/chekos/datawrapper)](https://github.com/chekos/datawrapper/blob/master/LICENSE)

A light-weight python wrapper for the Datawrapper API (v3). While it is not developed by Datawrapper officially, you can use it with your API credentials from datawrapper.de

</div>

## 🚀 Features

* Retrieve your account information (including folders).
* Add data to charts, tables or maps.
* Create charts, tables or maps - and add data from a `pandas.DataFrame` in one call!
* Update chart descriptions.
* Publish charts, tables or maps.
* Retrieve chart properties, update its metadata, and other information.
* Display a chart (as output of notebook cell - it gets weird because interactivity ¯\\_(ツ)_/¯ )
* Retrieve a chart, table or map's iframe code to embed.
* Export chart as png (still working on the svg and pdf parts).
* Move charts across folders and organizations.
* Delete charts.
* Get a list of all your charts.

## Installation

```bash
pip install -U datawrapper
```

or install with `Poetry`

```bash
poetry add datawrapper
```

### Makefile usage

[`Makefile`](https://github.com/chekos/datawrapper/blob/master/Makefile) contains many functions for fast assembling and convenient work.

<details>
<summary>1. Download Poetry</summary>
<p>

```bash
make download-poetry
```

</p>
</details>

<details>
<summary>2. Install all dependencies and pre-commit hooks</summary>
<p>

```bash
make install
```

If you do not want to install pre-commit hooks, run the command with the NO_PRE_COMMIT flag:

```bash
make install NO_PRE_COMMIT=1
```

</p>
</details>

<details>
<summary>3. Check the security of your code</summary>
<p>

```bash
make check-safety
```

This command launches a `Poetry` and `Pip` integrity check as well as identifies security issues with `Safety` and `Bandit`. By default, the build will not crash if any of the items fail. But you can set `STRICT=1` for the entire build, or you can configure strictness for each item separately.

```bash
make check-safety STRICT=1
```

or only for `safety`:

```bash
make check-safety SAFETY_STRICT=1
```

multiple

```bash
make check-safety PIP_STRICT=1 SAFETY_STRICT=1
```

> List of flags for `check-safety` (can be set to `1` or `0`): `STRICT`, `POETRY_STRICT`, `PIP_STRICT`, `SAFETY_STRICT`, `BANDIT_STRICT`.

</p>
</details>

<details>
<summary>4. Check the codestyle</summary>
<p>

The command is similar to `check-safety` but to check the code style, obviously. It uses `Black`, `Darglint`, `Isort`, and `Mypy` inside.

```bash
make check-style
```

It may also contain the `STRICT` flag.

```bash
make check-style STRICT=1
```

> List of flags for `check-style` (can be set to `1` or `0`): `STRICT`, `BLACK_STRICT`, `DARGLINT_STRICT`, `ISORT_STRICT`, `MYPY_STRICT`.

</p>
</details>

<details>
<summary>5. Run all the codestyle formaters</summary>
<p>

Codestyle uses `pre-commit` hooks, so ensure you've run `make install` before.

```bash
make codestyle
```

</p>
</details>

<details>
<summary>6. Run tests</summary>
<p>

```bash
make test
```

</p>
</details>

<details>
<summary>7. Run all the linters</summary>
<p>

```bash
make lint
```

the same as:

```bash
make test && make check-safety && make check-style
```

> List of flags for `lint` (can be set to `1` or `0`): `STRICT`, `POETRY_STRICT`, `PIP_STRICT`, `SAFETY_STRICT`, `BANDIT_STRICT`, `BLACK_STRICT`, `DARGLINT_STRICT`, `ISORT_STRICT`, `MYPY_STRICT`.

</p>
</details>

<details>
<summary>8. Build docker</summary>
<p>

```bash
make docker
```

which is equivalent to:

```bash
make docker VERSION=latest
```

More information [here](https://github.com/chekos/datawrapper/tree/master/docker).

</p>
</details>

<details>
<summary>9. Cleanup docker</summary>
<p>

```bash
make clean_docker
```

or to remove all build

```bash
make clean
```

More information [here](https://github.com/chekos/datawrapper/tree/master/docker).

</p>
</details>

## 📈 Releases

You can see the list of available releases on the [GitHub Releases](https://github.com/chekos/datawrapper/releases) page.

We follow [Semantic Versions](https://semver.org/) specification.

We use [`Release Drafter`](https://github.com/marketplace/actions/release-drafter). As pull requests are merged, a draft release is kept up-to-date listing the changes, ready to publish when you’re ready. With the categories option, you can categorize pull requests in release notes using labels.

For Pull Request this labels are configured, by default:

|               **Label**               |  **Title in Releases**  |
| :-----------------------------------: | :---------------------: |
|       `enhancement`, `feature`        |       🚀 Features       |
| `bug`, `refactoring`, `bugfix`, `fix` | 🔧 Fixes & Refactoring  |
|       `build`, `ci`, `testing`        | 📦 Build System & CI/CD |
|              `breaking`               |   💥 Breaking Changes   |
|            `documentation`            |    📝 Documentation     |
|            `dependencies`             | ⬆️ Dependencies updates |

You can update it in [`release-drafter.yml`](https://github.com/chekos/datawrapper/blob/master/.github/release-drafter.yml).

GitHub creates the `bug`, `enhancement`, and `documentation` labels for you. Dependabot creates the `dependencies` label. Create the remaining labels on the Issues tab of your GitHub repository, when you need them.

## 🛡 License

[![License](https://img.shields.io/github/license/chekos/datawrapper)](https://github.com/chekos/datawrapper/blob/master/LICENSE)

This project is licensed under the terms of the `MIT` license. See [LICENSE](https://github.com/chekos/datawrapper/blob/master/LICENSE) for more details.

## 📃 Citation

```
@misc{datawrapper,
  author = {chekos},
  title = {A light-weight python wrapper for the Datawrapper API (v3). While it is not developed by Datawrapper officially, you can use it with your API credentials from datawrapper.de},
  year = {2021},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/chekos/datawrapper}}
}
```

## Credits

This project was generated with [`python-package-template`](https://github.com/TezRomacH/python-package-template).

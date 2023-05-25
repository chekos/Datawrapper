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

or `pipenv`

```bash
pipenv install datawrapper
```

or install with `Poetry`

```bash
poetry add datawrapper
```

### Contributing

Clone the repository. Move into the directory on your terminal.

Install dependencies for development.

```sh
pipenv install --dev
```

Install pre-commit to run a battery of automatic quick fixes against your work.

```sh
pipenv run pre-commit install
```

## 📈 Releases

You can see the list of available releases on the [GitHub Releases](https://github.com/chekos/datawrapper/releases) page.

We follow [Semantic Versions](https://semver.org/) specification. When you're ready to make a new release, visit the releases page and create a new entry. Set the tags and press publish. That will trigger a GitHub Action that automatically deploys the code to the Python Package Index.

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

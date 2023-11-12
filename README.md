# datawrapper

A lightweight Python wrapper for the Datawrapper API

[![PyPI Version](https://img.shields.io/pypi/v/datawrapper.svg)](https://pypi.python.org/pypi/datawrapper)
[![Monthly downloads](https://img.shields.io/pypi/dm/datawrapper)](https://img.shields.io/pypi/dm/datawrappe)
[![Python Version](https://img.shields.io/pypi/pyversions/datawrapper.svg)](https://pypi.org/project/datawrapper/)
[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/chekos/datawrapper/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/chekos/datawrapper/blob/master/.pre-commit-config.yaml)
[![Semantic Versions](https://img.shields.io/badge/%F0%9F%9A%80-semantic%20versions-informational.svg)](https://github.com/chekos/datawrapper/releases)
[![License](https://img.shields.io/github/license/chekos/datawrapper)](https://github.com/chekos/datawrapper/blob/master/LICENSE)

## Features

* Create, get, update, export and delete charts, tables and maps
* Add data from a `pandas.DataFrame` or a GeoJSON file with one simple call
* Get, update and delete folders, users and teams.
* Retrieve lists of recently edited and updated charts
* Access metadata about your account
* Get a list of all available themes

## Installation

```bash
pipenv install datawrapper
```

## Releases

You can see the list of available releases on the [GitHub Releases](https://github.com/chekos/datawrapper/releases) page.

We follow [Semantic Versions](https://semver.org/) specification. When you're ready to make a new release, visit the releases page and create a new entry. Set the tags and press publish. That will trigger a GitHub Action that automatically deploys the code to the Python Package Index.

## License

[![License](https://img.shields.io/github/license/chekos/datawrapper)](https://github.com/chekos/datawrapper/blob/master/LICENSE)

This project is licensed under the terms of the `MIT` license. See [LICENSE](https://github.com/chekos/datawrapper/blob/master/LICENSE) for more details.

## Citation

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

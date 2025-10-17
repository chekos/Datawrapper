# datawrapper

A lightweight Python wrapper for the Datawrapper API

## Features

* Create, get, update, export and delete charts, tables and maps
* Add data from a `pandas.DataFrame` or a GeoJSON file with one simple call
* Get, update and delete folders, users and teams.
* Retrieve lists of recently edited and updated charts
* Access metadata about your account
* Get a list of all available themes

## Installation

```bash
uv install datawrapper
```

### Contributing

Clone the repository. Move into the directory on your terminal.

Install dependencies for development.

```bash
uv install --all-extras
```

Install pre-commit to run a battery of automatic quick fixes against your work.

```bash
uv run pre-commit install
uv run pre-commit install
```

Run tests with

```bash
uv run pytest
```

## 📈 Releases

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

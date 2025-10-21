# datawrapper

A lightweight Python wrapper for the Datawrapper API

## Features

* Create, get, update, export and delete charts, tables and maps
* Add data from a `pandas.DataFrame` or a GeoJSON file with one simple call
* Get, update and delete folders, users and teams.
* Retrieve lists of recently edited and updated charts
* Access metadata about your account

## Installation

```bash
# With `uv` ...
uv add datawrapper

# or, if you prefer...
pip install datawrapper
```

## Quick Start

Create beautiful charts with type-safe, object-oriented Python:

```python
import pandas as pd
import datawrapper as dw

# Configure a bar chart
chart = dw.BarChart(
    title="Top Programming Languages 2024",
    data=pd.DataFrame({"Language": ["Python", "JavaScript", "Java"], "Users": [45.3, 38.2, 30.5]}),
    axis_label_format=NumberFormat.ONE_DECIMAL,
    value_label_format=NumberFormat.ABBREVIATED,
)

# Create and publish (uses DATAWRAPPER_ACCESS_TOKEN environment variable)
chart.create()
chart.publish()
```
See the [full documentation](https://datawrapper.readthedocs.io/) for comprehensive guides on all chart types.

### Contributing

Clone the repository. Move into the directory on your terminal.

Install dependencies for development.

```bash
uv install --all-extras
```

Install pre-commit to run a battery of automatic quick fixes against your work.

```bash
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

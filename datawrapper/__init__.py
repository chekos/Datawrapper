"""A light-weight python wrapper for the Datawrapper API (v3). While it is not developed by Datawrapper officially, you can use it with your API credentials from datawrapper.de"""

try:
    from importlib.metadata import PackageNotFoundError, version  # type: ignore
except ImportError:  # pragma: no cover
    from importlib_metadata import PackageNotFoundError, version  # type: ignore


try:
    __version__ = version(__name__)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"

from datawrapper.charts import (
    Annotate,
    BarChart,
    BarOverlay,
    BaseChart,
    ColumnFormat,
    ConnectorLine,
    Describe,
    RangeAnnotation,
    TextAnnotation,
    Transform,
)

from .__main__ import Datawrapper

__all__ = [
    "Datawrapper",
    "BaseChart",
    "Annotate",
    "ColumnFormat",
    "Transform",
    "Describe",
    "BarChart",
    "BarOverlay",
    "TextAnnotation",
    "RangeAnnotation",
    "ConnectorLine",
]

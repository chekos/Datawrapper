"""A light-weight python wrapper for the Datawrapper API (v3). While it is not developed by Datawrapper officially, you can use it with your API credentials from datawrapper.de"""

try:
    from importlib.metadata import PackageNotFoundError, version  # type: ignore
except ImportError:  # pragma: no cover
    from importlib_metadata import PackageNotFoundError, version  # type: ignore


try:
    __version__ = version(__name__)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"

from datawrapper.chart_factory import get_chart
from datawrapper.charts import (
    Annotate,
    AreaChart,
    AreaFill,
    ArrowChart,
    BarChart,
    BarOverlay,
    BaseChart,
    ColumnChart,
    ColumnFormat,
    ConnectorLine,
    Describe,
    Line,
    LineChart,
    LineSymbol,
    LineValueLabel,
    MultipleColumnChart,
    RangeAnnotation,
    ScatterPlot,
    StackedBarChart,
    TextAnnotation,
    Transform,
)
from datawrapper.charts.enums import (
    ArrowHead,
    ConnectorLineType,
    DateFormat,
    GridDisplay,
    GridLabelAlign,
    GridLabelPosition,
    LineDash,
    LineInterpolation,
    LineWidth,
    NumberDivisor,
    NumberFormat,
    PlotHeightMode,
    RegressionMethod,
    ReplaceFlagsType,
    ScatterAxisPosition,
    ScatterGridLines,
    ScatterShape,
    ScatterSize,
    StrokeWidth,
    SymbolDisplay,
    SymbolShape,
    SymbolStyle,
    ValueLabelAlignment,
    ValueLabelDisplay,
    ValueLabelMode,
    ValueLabelPlacement,
)
from datawrapper.exceptions import (
    FailedRequestError,
    InvalidRequestError,
    RateLimitError,
)
from datawrapper.flags import get_country_flag

from .__main__ import Datawrapper

__all__ = [
    "Datawrapper",
    "get_chart",
    "BaseChart",
    "Annotate",
    "ColumnFormat",
    "Transform",
    "Describe",
    "BarChart",
    "BarOverlay",
    "ColumnChart",
    "LineChart",
    "Line",
    "LineSymbol",
    "LineValueLabel",
    "AreaFill",
    "AreaChart",
    "ArrowChart",
    "MultipleColumnChart",
    "ScatterPlot",
    "StackedBarChart",
    "TextAnnotation",
    "RangeAnnotation",
    "ConnectorLine",
    "ArrowHead",
    "ConnectorLineType",
    "DateFormat",
    "GridDisplay",
    "GridLabelAlign",
    "GridLabelPosition",
    "LineDash",
    "LineInterpolation",
    "LineWidth",
    "NumberDivisor",
    "NumberFormat",
    "PlotHeightMode",
    "RegressionMethod",
    "ReplaceFlagsType",
    "ScatterAxisPosition",
    "ScatterGridLines",
    "ScatterShape",
    "ScatterSize",
    "StrokeWidth",
    "SymbolDisplay",
    "SymbolShape",
    "SymbolStyle",
    "ValueLabelAlignment",
    "ValueLabelDisplay",
    "ValueLabelMode",
    "ValueLabelPlacement",
    "get_country_flag",
    "FailedRequestError",
    "InvalidRequestError",
    "RateLimitError",
]

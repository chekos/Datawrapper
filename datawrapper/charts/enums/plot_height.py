"""Enum for plot height mode in charts."""

from enum import Enum


class PlotHeightMode(str, Enum):
    """Plot height mode options for charts.

    Controls how the chart's plot area height is determined.

    Attributes:
        FIXED: Fixed pixel height
        RATIO: Height as a ratio of width

    Examples:
        >>> from datawrapper.charts import LineChart, PlotHeightMode
        >>> chart = LineChart(
        ...     title="Temperature",
        ...     plot_height_mode=PlotHeightMode.RATIO,
        ...     plot_height_ratio=0.5,
        ... )
    """

    FIXED = "fixed"
    RATIO = "ratio"

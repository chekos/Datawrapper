"""Enum for grid display options in charts."""

from enum import Enum


class GridDisplay(str, Enum):
    """Grid display options for chart axes.

    Controls how grid lines are displayed on chart axes.

    Attributes:
        OFF: No grid lines displayed
        ON: Full grid lines displayed
        TICKS: Only tick marks displayed (no full lines)
        LINES: Full grid lines displayed (alternative to ON)

    Examples:
        >>> from datawrapper.charts import LineChart, GridDisplay
        >>> chart = LineChart(
        ...     title="Temperature", x_grid=GridDisplay.TICKS, y_grid=GridDisplay.ON
        ... )
    """

    OFF = "off"
    ON = "on"
    TICKS = "ticks"
    LINES = "lines"

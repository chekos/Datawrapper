"""Enums for grid label positioning in charts."""

from enum import Enum


class GridLabelPosition(str, Enum):
    """Position options for grid labels on chart axes.

    Controls where axis labels are displayed relative to the chart.

    Attributes:
        AUTO: Automatically determine label position
        INSIDE: Labels displayed inside the chart area
        OUTSIDE: Labels displayed outside the chart area
        OFF: No labels displayed
        ON: Labels displayed (for x-axis labels)

    Examples:
        >>> from datawrapper.charts import LineChart, GridLabelPosition
        >>> chart = LineChart(
        ...     title="Temperature", y_grid_labels=GridLabelPosition.OUTSIDE
        ... )
    """

    AUTO = "auto"
    INSIDE = "inside"
    OUTSIDE = "outside"
    OFF = "off"
    ON = "on"


class GridLabelAlign(str, Enum):
    """Alignment options for grid labels.

    Controls the horizontal alignment of axis labels.

    Attributes:
        LEFT: Labels aligned to the left
        RIGHT: Labels aligned to the right

    Examples:
        >>> from datawrapper.charts import LineChart, GridLabelAlign
        >>> chart = LineChart(
        ...     title="Temperature", y_grid_label_align=GridLabelAlign.RIGHT
        ... )
    """

    LEFT = "left"
    RIGHT = "right"

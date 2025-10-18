"""Enums for value label configuration in charts."""

from enum import Enum


class ValueLabelDisplay(str, Enum):
    """Display mode options for value labels.

    Controls when value labels are shown on chart elements.

    Attributes:
        HOVER: Labels shown only on hover
        ALWAYS: Labels always visible
        OFF: Labels not shown

    Examples:
        >>> from datawrapper.charts import ColumnChart, ValueLabelDisplay
        >>> chart = ColumnChart(
        ...     title="Sales", show_value_labels=ValueLabelDisplay.ALWAYS
        ... )
    """

    HOVER = "hover"
    ALWAYS = "always"
    OFF = "off"


class ValueLabelPlacement(str, Enum):
    """Placement options for value labels.

    Controls where value labels are positioned relative to chart elements.

    Attributes:
        INSIDE: Labels placed inside chart elements
        OUTSIDE: Labels placed outside chart elements
        BELOW: Labels placed below chart elements

    Examples:
        >>> from datawrapper.charts import ColumnChart, ValueLabelPlacement
        >>> chart = ColumnChart(
        ...     title="Sales", value_labels_placement=ValueLabelPlacement.OUTSIDE
        ... )
    """

    INSIDE = "inside"
    OUTSIDE = "outside"
    BELOW = "below"


class ValueLabelAlignment(str, Enum):
    """Alignment options for value labels.

    Controls the horizontal alignment of value labels.

    Attributes:
        LEFT: Labels aligned to the left
        RIGHT: Labels aligned to the right

    Examples:
        >>> from datawrapper.charts import BarChart, ValueLabelAlignment
        >>> chart = BarChart(
        ...     title="Sales", value_label_alignment=ValueLabelAlignment.RIGHT
        ... )
    """

    LEFT = "left"
    RIGHT = "right"


class ValueLabelMode(str, Enum):
    """Mode options for value labels in stacked bar charts.

    Controls how value labels are positioned in stacked bar charts.

    Attributes:
        LEFT: Labels aligned to the left
        DIVERGING: Labels positioned for diverging data

    Examples:
        >>> from datawrapper.charts import StackedBarChart, ValueLabelMode
        >>> chart = StackedBarChart(
        ...     title="Survey Results", value_label_mode=ValueLabelMode.DIVERGING
        ... )
    """

    LEFT = "left"
    DIVERGING = "diverging"

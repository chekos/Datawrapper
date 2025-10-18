"""Enum for flag replacement options in charts."""

from enum import Enum


class ReplaceFlagsType(str, Enum):
    """Flag replacement options for country codes in charts.

    Controls whether and how country codes are replaced with flag icons.

    Attributes:
        OFF: No flag replacement
        FOUR_BY_THREE: 4:3 aspect ratio flags
        ONE_BY_ONE: 1:1 (square) aspect ratio flags
        CIRCLE: Circular flags

    Examples:
        >>> from datawrapper.charts import BarChart, ReplaceFlagsType
        >>> chart = BarChart(
        ...     title="Country Data", replace_flags=ReplaceFlagsType.FOUR_BY_THREE
        ... )
    """

    OFF = "off"
    FOUR_BY_THREE = "4x3"
    ONE_BY_ONE = "1x1"
    CIRCLE = "circle"

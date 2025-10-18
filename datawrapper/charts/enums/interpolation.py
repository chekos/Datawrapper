"""Enum for line interpolation methods in charts."""

from enum import Enum


class LineInterpolation(str, Enum):
    """Interpolation methods for drawing lines in charts.

    Controls how lines are drawn between data points.

    Attributes:
        LINEAR: Straight lines between points
        STEP: Step function (horizontal then vertical)
        STEP_AFTER: Step function (vertical then horizontal)
        STEP_BEFORE: Step function (horizontal then vertical, alternative)
        CARDINAL: Smooth curved lines using cardinal splines
        MONOTONE: Smooth curved lines that preserve monotonicity

    Examples:
        >>> from datawrapper.charts import LineChart, LineInterpolation
        >>> chart = LineChart(
        ...     title="Temperature", interpolation=LineInterpolation.MONOTONE
        ... )
    """

    LINEAR = "linear"
    STEP = "step"
    STEP_AFTER = "step-after"
    STEP_BEFORE = "step-before"
    CARDINAL = "cardinal"
    MONOTONE = "monotone-x"
    MONOTONE_X = "monotone-x"
    CURVED = "monotone-x"  # Alias for MONOTONE_X
    NATURAL = "natural"

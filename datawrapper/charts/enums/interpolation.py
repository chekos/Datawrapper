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
    STEP_AFTER = "stepAfter"
    STEP_BEFORE = "stepBefore"
    CARDINAL = "cardinal"
    MONOTONE = "monotone"
    MONOTONE_X = "monotone-x"
    NATURAL = "natural"

"""Enums for scatter plot configuration."""

from enum import Enum


class ScatterShape(str, Enum):
    """Shape options for scatter plot points.

    Controls the shape of points in scatter plots.

    Attributes:
        CIRCLE: Circular points
        SQUARE: Square points
        DIAMOND: Diamond-shaped points
        TRIANGLE: Triangular points
        TRIANGLE_DOWN: Downward-pointing triangular points
        CROSS: Cross-shaped points
        STAR: Star-shaped points
        WYE: Y-shaped points

    Examples:
        >>> from datawrapper.charts import ScatterPlot, ScatterShape
        >>> chart = ScatterPlot(title="Data Points", fixed_shape=ScatterShape.STAR)
    """

    CIRCLE = "symbolCircle"
    SQUARE = "symbolSquare"
    DIAMOND = "symbolDiamond"
    TRIANGLE = "symbolTriangle"
    TRIANGLE_DOWN = "symbolTriangleDown"
    CROSS = "symbolCross"
    STAR = "symbolStar"
    WYE = "symbolWye"


class ScatterSize(str, Enum):
    """Size mode options for scatter plot points.

    Controls how point sizes are determined.

    Attributes:
        FIXED: All points have the same fixed size
        DYNAMIC: Point sizes vary based on data

    Examples:
        >>> from datawrapper.charts import ScatterPlot, ScatterSize
        >>> chart = ScatterPlot(title="Data Points", size=ScatterSize.DYNAMIC)
    """

    FIXED = "fixed"
    DYNAMIC = "dynamic"


class ScatterAxisPosition(str, Enum):
    """Axis position options for scatter plots.

    Controls where axis ticks and labels are positioned.

    Attributes:
        BOTTOM: Axis at bottom of chart
        TOP: Axis at top of chart
        LEFT: Axis at left of chart
        RIGHT: Axis at right of chart
        ZERO: Axis at zero value
        OFF: No axis displayed

    Examples:
        >>> from datawrapper.charts import ScatterPlot, ScatterAxisPosition
        >>> chart = ScatterPlot(
        ...     title="Data Points",
        ...     x_position=ScatterAxisPosition.ZERO,
        ...     y_position=ScatterAxisPosition.LEFT,
        ... )
    """

    BOTTOM = "bottom"
    TOP = "top"
    LEFT = "left"
    RIGHT = "right"
    ZERO = "zero"
    OFF = "off"


class ScatterGridLines(str, Enum):
    """Grid line display options for scatter plots.

    Controls how grid lines are displayed on scatter plot axes.

    Attributes:
        ON: Show grid lines with labels
        OFF: No grid lines or labels
        NO_LABELS: Show grid lines without labels
        JUST_LABELS: Show labels without grid lines

    Examples:
        >>> from datawrapper.charts import ScatterPlot, ScatterGridLines
        >>> chart = ScatterPlot(
        ...     title="Data Points", x_grid_lines=ScatterGridLines.NO_LABELS
        ... )
    """

    ON = "on"
    OFF = "off"
    NO_LABELS = "no-labels"
    JUST_LABELS = "just-labels"


class RegressionMethod(str, Enum):
    """Regression method options for scatter plots.

    Controls the type of regression line to display.

    Attributes:
        LINEAR: Linear regression
        QUADRATIC: Quadratic (polynomial degree 2) regression
        CUBIC: Cubic (polynomial degree 3) regression
        EXPONENTIAL: Exponential regression
        LOGARITHMIC: Logarithmic regression
        POWER: Power regression

    Examples:
        >>> from datawrapper.charts import ScatterPlot, RegressionMethod
        >>> chart = ScatterPlot(
        ...     title="Data Points", regression_method=RegressionMethod.LINEAR
        ... )
    """

    LINEAR = "linear"
    QUADRATIC = "quadratic"
    CUBIC = "cubic"
    EXPONENTIAL = "exponential"
    LOGARITHMIC = "logarithmic"
    POWER = "power"

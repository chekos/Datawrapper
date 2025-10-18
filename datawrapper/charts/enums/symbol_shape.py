"""Enums for symbol shapes in charts."""

from enum import Enum


class SymbolShape(str, Enum):
    """Symbol shape options for line charts.

    Controls the shape of symbols/markers on line charts.

    Attributes:
        CIRCLE: Circular symbols
        SQUARE: Square symbols
        DIAMOND: Diamond-shaped symbols
        TRIANGLE: Triangular symbols
        CROSS: Cross-shaped symbols

    Examples:
        >>> from datawrapper.charts.line import Line, LineSymbol, SymbolShape
        >>> line = Line(
        ...     column="temperature",
        ...     symbols=LineSymbol(shape=SymbolShape.DIAMOND, size=5),
        ... )
    """

    CIRCLE = "circle"
    SQUARE = "square"
    DIAMOND = "diamond"
    TRIANGLE = "triangle"
    CROSS = "cross"


class SymbolStyle(str, Enum):
    """Symbol style options for line charts.

    Controls whether symbols are filled or hollow.

    Attributes:
        HOLLOW: Hollow/outlined symbols
        FILL: Filled symbols

    Examples:
        >>> from datawrapper.charts.line import Line, LineSymbol, SymbolStyle
        >>> line = Line(
        ...     column="temperature",
        ...     symbols=LineSymbol(shape="circle", style=SymbolStyle.HOLLOW),
        ... )
    """

    HOLLOW = "hollow"
    FILL = "fill"


class SymbolDisplay(str, Enum):
    """Symbol display options for line charts.

    Controls when symbols are shown on line charts.

    Attributes:
        EVERY: Show symbols on every data point
        FIRST: Show symbol only on first data point
        LAST: Show symbol only on last data point
        BOTH: Show symbols on first and last data points

    Examples:
        >>> from datawrapper.charts.line import Line, LineSymbol, SymbolDisplay
        >>> line = Line(
        ...     column="temperature",
        ...     symbols=LineSymbol(shape="circle", on=SymbolDisplay.BOTH),
        ... )
    """

    EVERY = "every"
    FIRST = "first"
    LAST = "last"
    BOTH = "both"

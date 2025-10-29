"""Enums for connector line configuration in annotations."""

from enum import Enum


class ConnectorLineType(str, Enum):
    """Type options for connector lines in annotations.

    Controls the shape of connector lines between text and chart elements.

    Attributes:
        STRAIGHT: Straight line connector
        CURVE_RIGHT: Curved line bending to the right
        CURVE_LEFT: Curved line bending to the left

    Examples:
        >>> from datawrapper.charts import (
        ...     TextAnnotation,
        ...     ConnectorLine,
        ...     ConnectorLineType,
        ... )
        >>> anno = TextAnnotation(
        ...     text="Important point",
        ...     x=10,
        ...     y=20,
        ...     connector_line=ConnectorLine(type=ConnectorLineType.CURVE_RIGHT),
        ... )
    """

    STRAIGHT = "straight"
    CURVE_RIGHT = "curveRight"
    CURVE_LEFT = "curveLeft"


class StrokeWidth(int, Enum):
    """Stroke width options for lines and annotations.

    Controls the thickness of lines in pixels.

    Attributes:
        THIN: 1 pixel width
        MEDIUM: 2 pixel width
        THICK: 3 pixel width

    Examples:
        >>> from datawrapper.charts import ConnectorLine, StrokeWidth
        >>> connector = ConnectorLine(type="straight", stroke=StrokeWidth.THICK)
    """

    THIN = 1
    MEDIUM = 2
    THICK = 3


class StrokeType(str, Enum):
    """Stroke type options for line annotations.

    Controls the dash pattern of stroke lines in range annotations.

    Attributes:
        SOLID: Solid line (no dashes)
        DASHED: Dashed line pattern
        DOTTED: Dotted line pattern

    Examples:
        >>> from datawrapper.charts import RangeAnnotation, StrokeType
        >>> anno = RangeAnnotation(
        ...     type="x",
        ...     x0=0,
        ...     x1=10,
        ...     display="line",
        ...     stroke_type=StrokeType.DASHED,
        ... )
    """

    SOLID = "solid"
    DASHED = "dashed"
    DOTTED = "dotted"


class ArrowHead(str, Enum):
    """Arrow head options for connector lines.

    Controls the style of arrow head at the end of connector lines.

    Attributes:
        LINES: Arrow head made of lines
        TRIANGLE: Triangular arrow head
        NONE: No arrow head (False value)

    Examples:
        >>> from datawrapper.charts import ConnectorLine, ArrowHead
        >>> connector = ConnectorLine(type="straight", arrow_head=ArrowHead.TRIANGLE)
    """

    LINES = "lines"
    TRIANGLE = "triangle"
    NONE = False  # type: ignore

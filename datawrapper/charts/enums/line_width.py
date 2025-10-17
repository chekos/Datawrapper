from enum import Enum


class LineWidth(str, Enum):
    """Line width options for line charts.

    These values control the stroke width of lines in charts:
    - THINNEST (style3) = 1px stroke width
    - THIN (style0) = 2px stroke width (default)
    - MEDIUM (style1) = 3px stroke width
    - THICK (style2) = 4px stroke width
    - INVISIBLE = hidden line

    Examples:
        >>> # Using enum (recommended - more readable)
        >>> Line(column="sales", width=LineWidth.THICK)

        >>> # Using raw API values (also supported for backwards compatibility)
        >>> Line(column="sales", width="style3")
    """

    THINNEST = "style3"
    THIN = "style0"
    MEDIUM = "style1"
    THICK = "style2"
    INVISIBLE = "invisible"

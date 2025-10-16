from enum import Enum


class LineWidth(str, Enum):
    """Line width options for line charts.

    These values control the stroke width of lines in charts:
    - THINNEST (style0) = 1px stroke width
    - THIN (style1) = 2px stroke width (default)
    - MEDIUM (style2) = 3px stroke width
    - THICK (style3) = 4px stroke width
    - INVISIBLE = hidden line

    Examples:
        >>> # Using enum (recommended - more readable)
        >>> Line(column="sales", width=LineWidth.THICK)

        >>> # Using raw API values (also supported for backwards compatibility)
        >>> Line(column="sales", width="style3")
    """

    THINNEST = "style0"
    THIN = "style1"
    MEDIUM = "style2"
    THICK = "style3"
    INVISIBLE = "invisible"

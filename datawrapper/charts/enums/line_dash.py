from enum import Enum


class LineDash(str, Enum):
    """Line dash pattern options for line charts.

    These values control the dash pattern of lines in charts:
    - SOLID (style1) = No dashes (default)
    - SHORT_DASH (style2) = Short dashes (2.3,2 pattern)
    - MEDIUM_DASH (style3) = Medium dashes (5,3 pattern)
    - LONG_DASH (style4) = Long dashes (7.5,3 pattern)

    Examples:
        >>> # Using enum (recommended - more readable)
        >>> Line(column="sales", dash=LineDash.MEDIUM_DASH)

        >>> # Using raw API values (also supported for backwards compatibility)
        >>> Line(column="sales", dash="style3")
    """

    SOLID = "style1"
    SHORT_DASH = "style2"
    MEDIUM_DASH = "style3"
    LONG_DASH = "style4"

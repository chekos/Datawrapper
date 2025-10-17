from enum import Enum


class LineDash(str, Enum):
    """Line dash pattern options for line charts.

    These values control the dash pattern of lines in charts:
    - SOLID (style0) = No dashes (default)
    - SHORT_DASH (style1) = Short dashes (2.3,2 pattern)
    - MEDIUM_DASH (style2) = Medium dashes (5,3 pattern)
    - LONG_DASH (style3) = Long dashes (7.5,3 pattern)

    Examples:
        >>> # Using enum (recommended - more readable)
        >>> Line(column="sales", dash=LineDash.MEDIUM_DASH)

        >>> # Using raw API values (also supported for backwards compatibility)
        >>> Line(column="sales", dash="style3")
    """

    SOLID = "style0"
    SHORT_DASH = "style1"
    MEDIUM_DASH = "style2"
    LONG_DASH = "style3"

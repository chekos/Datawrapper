from enum import Enum


class LineWidth(str, Enum):
    """Line width options for line charts.

    These values control the stroke width of lines in charts.

    ⚠️ IMPORTANT: The style numbers DO NOT increase with thickness!

    Attributes:
        THINNEST (style3): 1px stroke width - thinnest line
        THIN (style0): 2px stroke width - default, despite being style0
        MEDIUM (style1): 3px stroke width
        THICK (style2): 4px stroke width - thickest line
        INVISIBLE: Hidden line

    Examples:
        >>> # Using enum (recommended - avoids confusion)
        >>> Line(column="sales", width=LineWidth.THICK)  # ✓ Clearly 4px
        >>> Line(column="sales", width=LineWidth.THINNEST)  # ✓ Clearly 1px

        >>> # Using raw API values (works but confusing)
        >>> Line(column="sales", width="style2")  # 4px (thick, not thin!)
        >>> Line(column="sales", width="style3")  # 1px (thinnest, not thickest!)
    """

    THINNEST = "style3"  # 1px - ⚠️ Highest number, thinnest line!
    THIN = "style0"  # 2px (default)
    MEDIUM = "style1"  # 3px
    THICK = "style2"  # 4px - ⚠️ Not style3!
    INVISIBLE = "invisible"

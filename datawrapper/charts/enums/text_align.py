"""Text alignment enums for annotations."""

from enum import Enum


class TextAlign(str, Enum):
    """Text alignment positions for annotations.

    Represents a 3x3 grid of alignment positions combining vertical and horizontal alignment.

    Examples:
        >>> from datawrapper.charts import TextAnnotation, TextAlign
        >>> anno = TextAnnotation(
        ...     text="Top left corner", x=10, y=20, align=TextAlign.TOP_LEFT
        ... )
        >>> anno.align
        <TextAlign.TOP_LEFT: 'tl'>

        >>> # Using raw string (backwards compatible)
        >>> anno = TextAnnotation(text="Center", x=50, y=50, align="mc")
        >>> anno.align
        'mc'
    """

    #: Top-left alignment
    TOP_LEFT = "tl"

    #: Top-center alignment
    TOP_CENTER = "tc"

    #: Top-right alignment
    TOP_RIGHT = "tr"

    #: Middle-left alignment
    MIDDLE_LEFT = "ml"

    #: Middle-center alignment
    MIDDLE_CENTER = "mc"

    #: Middle-right alignment
    MIDDLE_RIGHT = "mr"

    #: Bottom-left alignment
    BOTTOM_LEFT = "bl"

    #: Bottom-center alignment
    BOTTOM_CENTER = "bc"

    #: Bottom-right alignment
    BOTTOM_RIGHT = "br"

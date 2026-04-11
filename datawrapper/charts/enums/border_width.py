"""Enum for border thickness options in tables."""

from enum import Enum


class BorderWidth(str, Enum):
    """Border width options for rows and columns in tables.

    Attributes:
        NONE: No border
        THIN: 1px thickness
        MEDIUM: 2px thickness
        THICK: 3px thickness

    Examples:
        >>> from datawrapper.charts import Table, TableHeaderRow, BorderWidth
        >>> chart = Table(
        ...     title="Country Data",
        ...     header_style=TableHeaderRow(border_bottom=BorderWidth.THIN),
        ... )
    """

    NONE = "none"
    THIN = "1px"
    MEDIUM = "2px"
    THICK = "3px"

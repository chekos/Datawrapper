"""Enum for pagination options in charts."""

from enum import Enum


class PaginationType(str, Enum):
    """Pagination options in charts.

    Controls whether pagination is enabled and where the controls sit.

    Attributes:
        OFF: No pagination
        TOP: Pagination controls at top
        BOTTOM: Pagination controls at bottom
        BOTH: Pagination controls at top and bottom

    Examples:
        >>> from datawrapper.charts import Table, PaginationType
        >>> chart = Table(title="Country Data", pagination=PaginationType.TOP)
    """

    OFF = "off"
    TOP = "top"
    BOTTOM = "bottom"
    BOTH = "both"

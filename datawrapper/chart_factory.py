"""Factory function for retrieving typed chart instances from Datawrapper API."""

from __future__ import annotations

import os
from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    from datawrapper.charts.base import BaseChart


def get_chart(chart_id: str, access_token: str | None = None) -> BaseChart:
    """Retrieve a chart and return the appropriate typed chart instance.

    This function fetches a chart from the Datawrapper API and automatically
    returns an instance of the appropriate chart class (LineChart, BarChart,
    ColumnChart, etc.) based on the chart's type.

    Args:
        chart_id: The ID of the chart to retrieve
        access_token: Optional Datawrapper API access token. If not provided,
            will attempt to use the DATAWRAPPER_ACCESS_TOKEN environment variable.

    Returns:
        BaseChart: A typed chart instance (LineChart, BarChart, ColumnChart, etc.)

    Raises:
        ValueError: If the chart type is not supported
        FailedRequestError: If the API request fails
        InvalidRequestError: If the request is invalid

    Example:
        >>> from datawrapper import get_chart
        >>> chart = get_chart("abc123")
        >>> print(type(chart))
        <class 'datawrapper.charts.line.LineChart'>
        >>> chart.title = "Updated Title"
        >>> chart.update()
    """
    # Import here to avoid circular imports
    from datawrapper import Datawrapper
    from datawrapper.charts import (
        AreaChart,
        ArrowChart,
        BarChart,
        ColumnChart,
        LineChart,
        MultipleColumnChart,
        ScatterPlot,
        StackedBarChart,
    )

    # Type mapping from Datawrapper API chart types to Python chart classes
    chart_type_map = {
        "d3-lines": LineChart,
        "d3-bars": BarChart,
        "column-chart": ColumnChart,
        "d3-area": AreaChart,
        "d3-arrow-plot": ArrowChart,
        "d3-bars-split": MultipleColumnChart,
        "d3-scatter-plot": ScatterPlot,
        "d3-bars-stacked": StackedBarChart,
    }

    # Fetch chart metadata to determine type
    # Handle empty strings from environment variable by converting to None
    access_token = access_token or os.getenv("DATAWRAPPER_ACCESS_TOKEN") or None
    dw = Datawrapper(access_token=access_token)
    metadata = dw.get_chart(chart_id)
    chart_type = metadata.get("type")

    # Validate chart type exists
    if not chart_type:
        raise ValueError(f"Chart {chart_id} has no type field in metadata")

    # Get the appropriate chart class
    chart_class = chart_type_map.get(chart_type)
    if not chart_class:
        raise ValueError(
            f"Unsupported chart type: {chart_type}. "
            f"Supported types: {', '.join(chart_type_map.keys())}"
        )

    # Cast to satisfy type checkers while avoiding circular imports
    # Use string literal to avoid NameError at runtime
    chart_class_typed = cast("type[BaseChart]", chart_class)
    return chart_class_typed.get(chart_id=chart_id, access_token=access_token)

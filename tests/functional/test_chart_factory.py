"""Functional tests for the get_chart factory function with mocked API calls."""

from unittest.mock import MagicMock, patch

import pytest

from datawrapper import Datawrapper, get_chart
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


def test_get_chart_line_chart(clean_env):
    """Test get_chart returns LineChart for d3-lines type."""
    # Create a mock Datawrapper client
    mock_client = MagicMock(spec=Datawrapper)

    # Mock get_chart response with line chart metadata
    mock_metadata = {
        "id": "line123",
        "title": "Temperature Trends",
        "type": "d3-lines",
        "metadata": {"visualize": {}},
    }
    mock_client.get_chart.return_value = mock_metadata

    with (
        patch.dict("os.environ", {}, clear=True),  # Clear environment variables
        patch("datawrapper.Datawrapper", return_value=mock_client),
        patch.object(LineChart, "get") as mock_line_get,
    ):
        # Configure mock_line_get to return a LineChart instance
        mock_line_chart = LineChart(title="Temperature Trends")
        mock_line_chart.chart_id = "line123"
        mock_line_get.return_value = mock_line_chart

        # Call get_chart
        result = get_chart(chart_id="line123")

        # Verify Datawrapper client was created
        mock_client.get_chart.assert_called_once_with("line123")

        # Verify LineChart.get was called
        mock_line_get.assert_called_once_with(chart_id="line123", access_token=None)

        # Verify result is a LineChart instance
        assert isinstance(result, LineChart)
        assert result.chart_id == "line123"


def test_get_chart_bar_chart():
    """Test get_chart returns BarChart for d3-bars type."""
    # Create a mock Datawrapper client
    mock_client = MagicMock(spec=Datawrapper)

    # Mock get_chart response with bar chart metadata
    mock_metadata = {
        "id": "bar456",
        "title": "Sales by Region",
        "type": "d3-bars",
        "metadata": {"visualize": {}},
    }
    mock_client.get_chart.return_value = mock_metadata

    with (
        patch("datawrapper.Datawrapper", return_value=mock_client),
        patch.object(BarChart, "get") as mock_bar_get,
    ):
        # Configure mock_bar_get to return a BarChart instance
        mock_bar_chart = BarChart(title="Sales by Region")
        mock_bar_chart.chart_id = "bar456"
        mock_bar_get.return_value = mock_bar_chart

        # Call get_chart
        result = get_chart(chart_id="bar456")

        # Verify result is a BarChart instance
        assert isinstance(result, BarChart)
        assert result.chart_id == "bar456"


def test_get_chart_column_chart():
    """Test get_chart returns ColumnChart for column-chart type."""
    # Create a mock Datawrapper client
    mock_client = MagicMock(spec=Datawrapper)

    # Mock get_chart response with column chart metadata
    mock_metadata = {
        "id": "col789",
        "title": "Monthly Revenue",
        "type": "column-chart",
        "metadata": {"visualize": {}},
    }
    mock_client.get_chart.return_value = mock_metadata

    with (
        patch("datawrapper.Datawrapper", return_value=mock_client),
        patch.object(ColumnChart, "get") as mock_col_get,
    ):
        # Configure mock_col_get to return a ColumnChart instance
        mock_col_chart = ColumnChart(title="Monthly Revenue")
        mock_col_chart.chart_id = "col789"
        mock_col_get.return_value = mock_col_chart

        # Call get_chart
        result = get_chart(chart_id="col789")

        # Verify result is a ColumnChart instance
        assert isinstance(result, ColumnChart)
        assert result.chart_id == "col789"


def test_get_chart_area_chart():
    """Test get_chart returns AreaChart for d3-area type."""
    # Create a mock Datawrapper client
    mock_client = MagicMock(spec=Datawrapper)

    # Mock get_chart response with area chart metadata
    mock_metadata = {
        "id": "area111",
        "title": "Population Growth",
        "type": "d3-area",
        "metadata": {"visualize": {}},
    }
    mock_client.get_chart.return_value = mock_metadata

    with (
        patch("datawrapper.Datawrapper", return_value=mock_client),
        patch.object(AreaChart, "get") as mock_area_get,
    ):
        # Configure mock_area_get to return an AreaChart instance
        mock_area_chart = AreaChart(title="Population Growth")
        mock_area_chart.chart_id = "area111"
        mock_area_get.return_value = mock_area_chart

        # Call get_chart
        result = get_chart(chart_id="area111")

        # Verify result is an AreaChart instance
        assert isinstance(result, AreaChart)
        assert result.chart_id == "area111"


def test_get_chart_arrow_chart():
    """Test get_chart returns ArrowChart for d3-arrow-plot type."""
    # Create a mock Datawrapper client
    mock_client = MagicMock(spec=Datawrapper)

    # Mock get_chart response with arrow chart metadata
    mock_metadata = {
        "id": "arrow222",
        "title": "Change Over Time",
        "type": "d3-arrow-plot",
        "metadata": {"visualize": {}},
    }
    mock_client.get_chart.return_value = mock_metadata

    with (
        patch("datawrapper.Datawrapper", return_value=mock_client),
        patch.object(ArrowChart, "get") as mock_arrow_get,
    ):
        # Configure mock_arrow_get to return an ArrowChart instance
        mock_arrow_chart = ArrowChart(title="Change Over Time")
        mock_arrow_chart.chart_id = "arrow222"
        mock_arrow_get.return_value = mock_arrow_chart

        # Call get_chart
        result = get_chart(chart_id="arrow222")

        # Verify result is an ArrowChart instance
        assert isinstance(result, ArrowChart)
        assert result.chart_id == "arrow222"


def test_get_chart_multiple_column_chart():
    """Test get_chart returns MultipleColumnChart for d3-bars-split type."""
    # Create a mock Datawrapper client
    mock_client = MagicMock(spec=Datawrapper)

    # Mock get_chart response with multiple column chart metadata
    mock_metadata = {
        "id": "multi333",
        "title": "Grouped Data",
        "type": "d3-bars-split",
        "metadata": {"visualize": {}},
    }
    mock_client.get_chart.return_value = mock_metadata

    with (
        patch("datawrapper.Datawrapper", return_value=mock_client),
        patch.object(MultipleColumnChart, "get") as mock_multi_get,
    ):
        # Configure mock_multi_get to return a MultipleColumnChart instance
        mock_multi_chart = MultipleColumnChart(title="Grouped Data")
        mock_multi_chart.chart_id = "multi333"
        mock_multi_get.return_value = mock_multi_chart

        # Call get_chart
        result = get_chart(chart_id="multi333")

        # Verify result is a MultipleColumnChart instance
        assert isinstance(result, MultipleColumnChart)
        assert result.chart_id == "multi333"


def test_get_chart_scatter_plot():
    """Test get_chart returns ScatterPlot for d3-scatter-plot type."""
    # Create a mock Datawrapper client
    mock_client = MagicMock(spec=Datawrapper)

    # Mock get_chart response with scatter plot metadata
    mock_metadata = {
        "id": "scatter444",
        "title": "Correlation Analysis",
        "type": "d3-scatter-plot",
        "metadata": {"visualize": {}},
    }
    mock_client.get_chart.return_value = mock_metadata

    with (
        patch("datawrapper.Datawrapper", return_value=mock_client),
        patch.object(ScatterPlot, "get") as mock_scatter_get,
    ):
        # Configure mock_scatter_get to return a ScatterPlot instance
        mock_scatter_chart = ScatterPlot(title="Correlation Analysis")
        mock_scatter_chart.chart_id = "scatter444"
        mock_scatter_get.return_value = mock_scatter_chart

        # Call get_chart
        result = get_chart(chart_id="scatter444")

        # Verify result is a ScatterPlot instance
        assert isinstance(result, ScatterPlot)
        assert result.chart_id == "scatter444"


def test_get_chart_stacked_bar_chart():
    """Test get_chart returns StackedBarChart for d3-bars-stacked type."""
    # Create a mock Datawrapper client
    mock_client = MagicMock(spec=Datawrapper)

    # Mock get_chart response with stacked bar chart metadata
    mock_metadata = {
        "id": "stacked555",
        "title": "Market Share",
        "type": "d3-bars-stacked",
        "metadata": {"visualize": {}},
    }
    mock_client.get_chart.return_value = mock_metadata

    with (
        patch("datawrapper.Datawrapper", return_value=mock_client),
        patch.object(StackedBarChart, "get") as mock_stacked_get,
    ):
        # Configure mock_stacked_get to return a StackedBarChart instance
        mock_stacked_chart = StackedBarChart(title="Market Share")
        mock_stacked_chart.chart_id = "stacked555"
        mock_stacked_get.return_value = mock_stacked_chart

        # Call get_chart
        result = get_chart(chart_id="stacked555")

        # Verify result is a StackedBarChart instance
        assert isinstance(result, StackedBarChart)
        assert result.chart_id == "stacked555"


def test_get_chart_with_access_token():
    """Test get_chart passes access_token to both Datawrapper and chart class."""
    # Create a mock Datawrapper client
    mock_client = MagicMock(spec=Datawrapper)

    # Mock get_chart response
    mock_metadata = {
        "id": "token666",
        "title": "Test Chart",
        "type": "d3-lines",
        "metadata": {"visualize": {}},
    }
    mock_client.get_chart.return_value = mock_metadata

    with (
        patch("datawrapper.Datawrapper", return_value=mock_client) as mock_dw_class,
        patch.object(LineChart, "get") as mock_line_get,
    ):
        # Configure mock_line_get to return a LineChart instance
        mock_line_chart = LineChart(title="Test Chart")
        mock_line_chart.chart_id = "token666"
        mock_line_get.return_value = mock_line_chart

        # Call get_chart with custom access token
        result = get_chart(chart_id="token666", access_token="custom_token")

        # Verify Datawrapper was initialized with access token
        mock_dw_class.assert_called_once_with(access_token="custom_token")

        # Verify LineChart.get was called with access token
        mock_line_get.assert_called_once_with(
            chart_id="token666", access_token="custom_token"
        )

        # Verify result
        assert isinstance(result, LineChart)
        assert result.chart_id == "token666"


def test_get_chart_missing_type():
    """Test get_chart raises ValueError when chart has no type field."""
    # Create a mock Datawrapper client
    mock_client = MagicMock(spec=Datawrapper)

    # Mock get_chart response without type field
    mock_metadata = {
        "id": "notype777",
        "title": "Test Chart",
        "metadata": {"visualize": {}},
    }
    mock_client.get_chart.return_value = mock_metadata

    with patch("datawrapper.Datawrapper", return_value=mock_client):
        # Call get_chart should raise ValueError
        with pytest.raises(ValueError, match="has no type field in metadata"):
            get_chart(chart_id="notype777")


def test_get_chart_unsupported_type():
    """Test get_chart raises ValueError for unsupported chart types."""
    # Create a mock Datawrapper client
    mock_client = MagicMock(spec=Datawrapper)

    # Mock get_chart response with unsupported type
    mock_metadata = {
        "id": "unsupported888",
        "title": "Test Chart",
        "type": "d3-maps",  # Unsupported type
        "metadata": {"visualize": {}},
    }
    mock_client.get_chart.return_value = mock_metadata

    with patch("datawrapper.Datawrapper", return_value=mock_client):
        # Call get_chart should raise ValueError
        with pytest.raises(ValueError, match="Unsupported chart type: d3-maps"):
            get_chart(chart_id="unsupported888")


def test_get_chart_all_supported_types():
    """Test that all supported chart types are correctly mapped."""
    supported_types = {
        "d3-lines": LineChart,
        "d3-bars": BarChart,
        "column-chart": ColumnChart,
        "d3-area": AreaChart,
        "d3-arrow-plot": ArrowChart,
        "d3-bars-split": MultipleColumnChart,
        "d3-scatter-plot": ScatterPlot,
        "d3-bars-stacked": StackedBarChart,
    }

    for chart_type, expected_class in supported_types.items():
        # Create a mock Datawrapper client
        mock_client = MagicMock(spec=Datawrapper)

        # Mock get_chart response
        mock_metadata = {
            "id": f"test_{chart_type}",
            "title": f"Test {chart_type}",
            "type": chart_type,
            "metadata": {"visualize": {}},
        }
        mock_client.get_chart.return_value = mock_metadata

        with (
            patch("datawrapper.Datawrapper", return_value=mock_client),
            patch.object(expected_class, "get") as mock_get,
        ):
            # Configure mock_get to return an instance of the expected class
            mock_chart = expected_class(title=f"Test {chart_type}")
            mock_chart.chart_id = f"test_{chart_type}"
            mock_get.return_value = mock_chart

            # Call get_chart
            result = get_chart(chart_id=f"test_{chart_type}")

            # Verify result is an instance of the expected class
            assert isinstance(result, expected_class)
            assert result.chart_id == f"test_{chart_type}"

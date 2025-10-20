"""Test the display method on BaseChart."""

from unittest.mock import MagicMock, patch

import pytest
from IPython.display import IFrame

from datawrapper.charts.base import BaseChart


def test_base_chart_display_method_exists():
    """Test that the display method exists on BaseChart."""
    chart = BaseChart(chart_type="d3-lines", title="Test Chart")
    assert hasattr(chart, "display")
    assert callable(chart.display)


def test_base_chart_display_requires_chart_id():
    """Test that display raises ValueError when chart_id is not set."""
    chart = BaseChart(chart_type="d3-lines", title="Test Chart")

    with pytest.raises(ValueError, match="No chart_id set"):
        chart.display()


def test_base_chart_display_with_chart_id():
    """Test that display works when chart_id is set."""
    # Create a chart with a chart_id
    chart = BaseChart(
        chart_type="d3-lines",
        title="Test Display Chart",
        data=[{"x": 1, "y": 2}, {"x": 2, "y": 4}],
    )
    chart.chart_id = "test123"

    # Mock the client and its display_chart method
    mock_client = MagicMock()
    mock_iframe = IFrame("https://example.com", width=600, height=400)
    mock_client.display_chart.return_value = mock_iframe

    with patch.object(chart, "_get_client", return_value=mock_client):
        # Call the display method
        result = chart.display()

        # Verify the client method was called
        mock_client.display_chart.assert_called_once()

        # Verify the chart_id was passed
        call_kwargs = mock_client.display_chart.call_args.kwargs
        assert call_kwargs["chart_id"] == "test123"

        # Verify the result is an IFrame
        assert result == mock_iframe
        assert isinstance(result, IFrame)


def test_base_chart_display_with_access_token():
    """Test that display passes access_token to the client."""
    # Create a chart with a chart_id
    chart = BaseChart(
        chart_type="d3-lines",
        title="Test Display Chart with Token",
        data=[{"x": 1, "y": 2}, {"x": 2, "y": 4}],
    )
    chart.chart_id = "test123"

    # Mock the client and its display_chart method
    mock_client = MagicMock()
    mock_iframe = IFrame("https://example.com", width=600, height=400)
    mock_client.display_chart.return_value = mock_iframe

    with patch.object(
        chart, "_get_client", return_value=mock_client
    ) as mock_get_client:
        # Call the display method with an access token
        test_token = "test_access_token"
        result = chart.display(access_token=test_token)

        # Verify _get_client was called with the access token
        mock_get_client.assert_called_once_with(test_token)

        # Verify the client method was called
        mock_client.display_chart.assert_called_once()

        # Verify the chart_id was passed
        call_kwargs = mock_client.display_chart.call_args.kwargs
        assert call_kwargs["chart_id"] == "test123"

        # Verify the result is an IFrame
        assert result == mock_iframe
        assert isinstance(result, IFrame)

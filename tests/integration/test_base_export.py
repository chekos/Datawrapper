"""Test the export method on BaseChart."""

from unittest.mock import MagicMock, patch

import pytest

from datawrapper.charts.base import BaseChart


def test_base_chart_export_method_exists():
    """Test that the export method exists on BaseChart."""
    chart = BaseChart(chart_type="d3-lines", title="Test Chart")
    assert hasattr(chart, "export")
    assert callable(chart.export)


def test_base_chart_export_requires_chart_id():
    """Test that export raises ValueError when chart_id is not set."""
    chart = BaseChart(chart_type="d3-lines", title="Test Chart")

    with pytest.raises(ValueError, match="No chart_id set"):
        chart.export()


def test_base_chart_export_with_chart_id(tmp_path):
    """Test that export works when chart_id is set."""
    # Create a chart with a chart_id
    chart = BaseChart(
        chart_type="d3-lines",
        title="Test Export Chart",
        data=[{"x": 1, "y": 2}, {"x": 2, "y": 4}],
    )
    chart.chart_id = "test123"

    # Mock the client and its export_chart method
    mock_client = MagicMock()
    output_file = tmp_path / "test_export.png"
    mock_client.export_chart.return_value = output_file

    with patch.object(chart, "_get_client", return_value=mock_client):
        # Export to a temporary file
        result = chart.export(
            output="png",
            filepath=str(output_file),
            display=False,
        )

        # Verify the client method was called
        mock_client.export_chart.assert_called_once()

        # Verify the chart_id was passed
        call_kwargs = mock_client.export_chart.call_args.kwargs
        assert call_kwargs["chart_id"] == "test123"
        assert call_kwargs["output"] == "png"
        assert call_kwargs["filepath"] == str(output_file)
        assert call_kwargs["display"] is False

        # Verify the result
        assert result == output_file

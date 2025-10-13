"""Test the export method on BaseChart."""

import os
from pathlib import Path

import pytest

from datawrapper.charts.base import BaseChart


@pytest.mark.skipif(
    not os.getenv("DATAWRAPPER_ACCESS_TOKEN"),
    reason="DATAWRAPPER_ACCESS_TOKEN not set",
)
def test_base_chart_export_method_exists():
    """Test that the export method exists on BaseChart."""
    chart = BaseChart(chart_type="d3-lines", title="Test Chart")
    assert hasattr(chart, "export")
    assert callable(chart.export)


@pytest.mark.skipif(
    not os.getenv("DATAWRAPPER_ACCESS_TOKEN"),
    reason="DATAWRAPPER_ACCESS_TOKEN not set",
)
def test_base_chart_export_requires_chart_id():
    """Test that export raises ValueError when chart_id is not set."""
    chart = BaseChart(chart_type="d3-lines", title="Test Chart")
    
    with pytest.raises(ValueError, match="No chart_id set"):
        chart.export()


@pytest.mark.skipif(
    not os.getenv("DATAWRAPPER_ACCESS_TOKEN"),
    reason="DATAWRAPPER_ACCESS_TOKEN not set",
)
def test_base_chart_export_with_chart_id(tmp_path):
    """Test that export works when chart_id is set."""
    # Create a simple chart
    chart = BaseChart(
        chart_type="d3-lines",
        title="Test Export Chart",
        data=[{"x": 1, "y": 2}, {"x": 2, "y": 4}],
    )
    
    # Create the chart
    chart_id = chart.create()
    
    try:
        # Export to a temporary file
        output_file = tmp_path / "test_export.png"
        result = chart.export(
            output="png",
            filepath=str(output_file),
            display=False,
        )
        
        # Verify the file was created
        assert isinstance(result, Path)
        assert result.exists()
        assert result.suffix == ".png"
        
    finally:
        # Clean up: delete the chart
        if chart.chart_id:
            client = chart._get_client()
            client.delete_chart(chart.chart_id)

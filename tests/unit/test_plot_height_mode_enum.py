"""Test PlotHeightMode enum integration and backwards compatibility."""

import pytest
from pydantic import ValidationError

from datawrapper.charts import (
    AreaChart,
    ColumnChart,
    LineChart,
    MultipleColumnChart,
    ScatterPlot,
)
from datawrapper.charts.enums import PlotHeightMode


class TestPlotHeightModeEnum:
    """Test PlotHeightMode enum usage across chart types."""

    def test_area_chart_with_enum(self):
        """Test AreaChart accepts PlotHeightMode enum values."""
        chart = AreaChart(
            title="Test",
            plot_height_mode=PlotHeightMode.RATIO,
        )
        assert chart.plot_height_mode == "ratio"

    def test_area_chart_with_string(self):
        """Test AreaChart accepts raw string values for backwards compatibility."""
        chart = AreaChart(
            title="Test",
            plot_height_mode="fixed",
        )
        assert chart.plot_height_mode == "fixed"

    def test_column_chart_with_enum(self):
        """Test ColumnChart accepts PlotHeightMode enum values."""
        chart = ColumnChart(
            title="Test",
            plot_height_mode=PlotHeightMode.FIXED,
        )
        assert chart.plot_height_mode == "fixed"

    def test_column_chart_with_string(self):
        """Test ColumnChart accepts raw string values for backwards compatibility."""
        chart = ColumnChart(
            title="Test",
            plot_height_mode="ratio",
        )
        assert chart.plot_height_mode == "ratio"

    def test_line_chart_with_enum(self):
        """Test LineChart accepts PlotHeightMode enum values."""
        chart = LineChart(
            title="Test",
            plot_height_mode=PlotHeightMode.RATIO,
        )
        assert chart.plot_height_mode == "ratio"

    def test_line_chart_with_string(self):
        """Test LineChart accepts raw string values for backwards compatibility."""
        chart = LineChart(
            title="Test",
            plot_height_mode="fixed",
        )
        assert chart.plot_height_mode == "fixed"

    def test_multiple_column_chart_with_enum(self):
        """Test MultipleColumnChart accepts PlotHeightMode enum values."""
        chart = MultipleColumnChart(
            title="Test",
            plot_height_mode=PlotHeightMode.FIXED,
        )
        assert chart.plot_height_mode == "fixed"

    def test_multiple_column_chart_with_string(self):
        """Test MultipleColumnChart accepts raw string values for backwards compatibility."""
        chart = MultipleColumnChart(
            title="Test",
            plot_height_mode="ratio",
        )
        assert chart.plot_height_mode == "ratio"

    def test_scatter_plot_with_enum(self):
        """Test ScatterPlot accepts PlotHeightMode enum values."""
        chart = ScatterPlot(
            title="Test",
            plot_height_mode=PlotHeightMode.RATIO,
        )
        assert chart.plot_height_mode == "ratio"

    def test_scatter_plot_with_string(self):
        """Test ScatterPlot accepts raw string values for backwards compatibility."""
        chart = ScatterPlot(
            title="Test",
            plot_height_mode="fixed",
        )
        assert chart.plot_height_mode == "fixed"

    def test_invalid_value_raises_error(self):
        """Test that invalid values raise ValidationError."""
        with pytest.raises(ValidationError):
            AreaChart(
                title="Test",
                plot_height_mode="invalid",
            )

    def test_serialization_with_enum(self):
        """Test that enum values serialize correctly."""
        chart = AreaChart(
            title="Test",
            plot_height_mode=PlotHeightMode.RATIO,
            plot_height_ratio=0.75,
        )
        serialized = chart.serialize_model()
        assert serialized["metadata"]["visualize"]["plotHeightMode"] == "ratio"
        assert serialized["metadata"]["visualize"]["plotHeightRatio"] == 0.75

    def test_serialization_with_string(self):
        """Test that string values serialize correctly."""
        chart = ColumnChart(
            title="Test",
            plot_height_mode="fixed",
            plot_height_fixed=400,
        )
        serialized = chart.serialize_model()
        assert serialized["metadata"]["visualize"]["plotHeightMode"] == "fixed"
        assert serialized["metadata"]["visualize"]["plotHeightFixed"] == 400

    def test_deserialization_preserves_mode(self):
        """Test that deserialization preserves plot height mode."""
        api_response = {
            "id": "test123",
            "type": "d3-lines",
            "title": "Test",
            "metadata": {
                "visualize": {
                    "plotHeightMode": "ratio",
                    "plotHeightRatio": 0.6,
                }
            },
        }
        init_data = LineChart.deserialize_model(api_response)
        assert init_data["plot_height_mode"] == "ratio"
        assert init_data["plot_height_ratio"] == 0.6

    def test_enum_values(self):
        """Test that PlotHeightMode enum has correct values."""
        assert PlotHeightMode.FIXED == "fixed"
        assert PlotHeightMode.RATIO == "ratio"
        assert len(PlotHeightMode) == 2

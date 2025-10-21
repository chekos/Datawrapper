"""Test BarChart axes metadata structure."""

import pandas as pd

from datawrapper import BarChart


def test_bar_chart_axes_in_metadata():
    """Test that axes configuration is placed in metadata section."""
    # Create a simple bar chart
    chart = BarChart(
        **{
            "chart-type": "d3-bars",
            "title": "Test Chart",
            "label-column": "Country",
            "bar-column": "Value",
            "color-column": "Category",
            "groups-column": "Region",
            "data": pd.DataFrame(
                {
                    "Country": ["A", "B", "C"],
                    "Value": [10, 20, 30],
                    "Category": ["X", "Y", "Z"],
                    "Region": ["North", "South", "East"],
                }
            ),
        }
    )

    # Serialize the chart
    serialized = chart.serialize_model()

    # Verify axes is in metadata, not at root level
    assert "axes" not in serialized, "axes should not be at root level"
    assert "metadata" in serialized, "metadata section should exist"
    assert "axes" in serialized["metadata"], "axes should be in metadata section"

    # Verify axes structure
    axes = serialized["metadata"]["axes"]
    assert "colors" in axes
    assert "bars" in axes
    assert "labels" in axes
    assert "groups" in axes

    # Verify axes values
    assert axes["colors"] == "Category"
    assert axes["bars"] == "Value"
    assert axes["labels"] == "Country"
    assert axes["groups"] == "Region"


def test_bar_chart_axes_fallback_colors():
    """Test that colors axis falls back to label_column when color_column is empty."""
    chart = BarChart(
        **{
            "chart-type": "d3-bars",
            "title": "Test Chart",
            "label-column": "Country",
            "bar-column": "Value",
            "color-column": "",  # Empty color column
            "data": pd.DataFrame({"Country": ["A", "B", "C"], "Value": [10, 20, 30]}),
        }
    )

    serialized = chart.serialize_model()
    axes = serialized["metadata"]["axes"]

    # Should fall back to label_column for colors
    assert axes["colors"] == "Country"
    assert axes["labels"] == "Country"


def test_bar_chart_metadata_structure_order():
    """Test that metadata sections are in the correct order."""
    chart = BarChart(
        **{
            "chart-type": "d3-bars",
            "title": "Test Chart",
            "data": pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]}),
        }
    )

    serialized = chart.serialize_model()
    metadata = serialized["metadata"]

    # Check that all expected sections exist
    expected_sections = [
        "data",
        "describe",
        "visualize",
        "publish",
        "annotate",
        "custom",
        "axes",
    ]
    for section in expected_sections:
        assert section in metadata, f"Missing metadata section: {section}"

    # Verify axes is at the same level as other metadata sections
    assert isinstance(metadata["axes"], dict)
    assert isinstance(metadata["data"], dict)
    assert isinstance(metadata["visualize"], dict)


def test_bar_chart_empty_axes_values():
    """Test axes configuration with empty column values."""
    chart = BarChart(
        **{
            "chart-type": "d3-bars",
            "title": "Test Chart",
            "data": pd.DataFrame({"A": [1, 2, 3]}),
        }
    )

    serialized = chart.serialize_model()
    axes = serialized["metadata"]["axes"]

    # All should be empty strings when no columns are specified
    assert axes["colors"] == ""  # color_column is empty, label_column is empty
    assert axes["bars"] == ""
    assert axes["labels"] == ""
    # groups should not be present when groups_column is None
    assert "groups" not in axes

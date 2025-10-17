"""Tests for BaseChart serialization with root-level metadata."""

import pandas as pd

import datawrapper


def test_base_chart_serialization_includes_root_metadata():
    """Test that BaseChart serialization includes required root-level metadata."""
    # Create a simple BaseChart instance using model_validate to bypass field name issues
    chart = datawrapper.BaseChart.model_validate(
        {
            "chart-type": "d3-bars",
            "title": "Test Chart Title",
            "language": "en-US",
            "theme": "datawrapper",
        }
    )

    # Serialize the chart
    serialized = chart.model_dump()

    # Verify root-level metadata is present
    assert "type" in serialized
    assert "title" in serialized
    assert "language" in serialized
    assert "theme" in serialized

    # Verify the values are correct
    assert serialized["type"] == "d3-bars"
    assert serialized["title"] == "Test Chart Title"
    assert serialized["language"] == "en-US"
    assert serialized["theme"] == "datawrapper"


def test_base_chart_serialization_with_empty_theme():
    """Test that BaseChart handles empty theme correctly."""
    chart = datawrapper.BaseChart.model_validate(
        {
            "chart-type": "d3-lines",
            "title": "Test Chart",
            "theme": "",  # Empty theme
        }
    )

    serialized = chart.model_dump()

    # Empty theme should be omitted from serialization (our fix for Datawrapper API compatibility)
    assert "theme" not in serialized


def test_base_chart_serialization_with_default_values():
    """Test that BaseChart serialization works with default values."""
    chart = datawrapper.BaseChart.model_validate({"chart-type": "d3-area"})

    serialized = chart.model_dump()

    # Verify root-level metadata with defaults
    assert serialized["type"] == "d3-area"
    assert serialized["title"] == ""  # Default empty title
    assert serialized["language"] == "en-US"  # Default language
    # Default theme is "datawrapper"
    assert serialized["theme"] == "datawrapper"


def test_base_chart_serialization_structure():
    """Test that the serialized structure includes all expected sections."""
    chart = datawrapper.BaseChart.model_validate(
        {
            "chart-type": "d3-bars",
            "title": "Structure Test",
        }
    )

    serialized = chart.model_dump()

    # Verify all expected root-level sections are present
    expected_root_sections = [
        "type",
        "title",
        "language",
        "theme",
        "metadata",
    ]

    for section in expected_root_sections:
        assert section in serialized, f"Missing root section: {section}"

    # Default theme is "datawrapper"
    assert serialized["theme"] == "datawrapper"

    # Verify metadata subsections are present
    metadata = serialized["metadata"]
    expected_metadata_sections = [
        "visualize",
        "data",
        "describe",
        "annotate",
        "custom",
        "publish",
    ]

    for section in expected_metadata_sections:
        assert section in metadata, f"Missing metadata section: {section}"


def test_base_chart_field_name_is_type_not_chart_type():
    """Test that the serialized field is 'type', not 'chart-type' or 'chart_type'."""
    chart = datawrapper.BaseChart.model_validate({"chart-type": "d3-scatter-plot"})

    serialized = chart.model_dump()

    # Should use "type" as the field name in serialized output
    assert "type" in serialized
    assert "chart-type" not in serialized
    assert "chart_type" not in serialized

    # Value should match the chart_type
    assert serialized["type"] == "d3-scatter-plot"


def test_base_chart_serialization_with_data():
    """Test that BaseChart serialization works with actual data."""
    # Create test data
    test_data = pd.DataFrame({"category": ["A", "B", "C"], "value": [10, 20, 30]})

    chart = datawrapper.BaseChart.model_validate(
        {
            "chart-type": "d3-bars",
            "title": "Data Test Chart",
            "data": test_data,
        }
    )

    serialized = chart.model_dump()

    # Root metadata should still be present
    assert serialized["type"] == "d3-bars"
    assert serialized["title"] == "Data Test Chart"

    # Data section should be present in metadata
    assert "data" in serialized["metadata"]

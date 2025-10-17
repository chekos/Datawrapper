"""Test that BaseChart metadata sections are in the correct order."""

import pandas as pd

from datawrapper import BaseChart


def test_metadata_section_order():
    """Test that metadata sections appear in the correct Datawrapper API order."""
    # Create a simple chart
    data = pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})
    chart = BaseChart(
        **{
            "chart-type": "d3-bars",
            "title": "Test Chart",
            "data": data,
            "source-name": "Test Source",
            "notes": "Test notes",
        }
    )

    # Serialize the chart
    serialized = chart.model_dump()

    # Check that root-level fields are present
    assert "type" in serialized
    assert "title" in serialized
    assert "language" in serialized
    # Note: theme field is omitted when empty (our fix for Datawrapper API compatibility)

    # Check that metadata wrapper exists
    assert "metadata" in serialized
    metadata = serialized["metadata"]

    # Check that all expected sections are present in metadata
    expected_sections = [
        "data",
        "describe",
        "visualize",
        "publish",
        "annotate",
        "custom",
    ]
    for section in expected_sections:
        assert section in metadata, f"Missing section: {section}"

    # Check the order by converting to list of keys
    actual_order = list(metadata.keys())
    expected_order = ["data", "describe", "visualize", "publish", "annotate", "custom"]

    assert actual_order == expected_order, (
        f"Expected order {expected_order}, got {actual_order}"
    )


def test_metadata_content_structure():
    """Test that metadata sections contain expected content."""
    data = pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})
    chart = BaseChart(
        **{
            "chart-type": "d3-bars",
            "title": "Test Chart",
            "data": data,
            "source-name": "Test Source",
            "source-url": "https://example.com",
            "notes": "Test notes",
            "byline": "Test Author",
        }
    )

    serialized = chart.model_dump()
    metadata = serialized["metadata"]

    # Check data section structure
    assert "transpose" in metadata["data"]
    assert "vertical-header" in metadata["data"]

    # Check describe section structure
    assert "source-name" in metadata["describe"]
    assert "source-url" in metadata["describe"]
    assert "byline" in metadata["describe"]

    # Check visualize section structure
    assert "dark-mode-invert" in metadata["visualize"]
    assert "sharing" in metadata["visualize"]

    # Check publish section structure
    assert "blocks" in metadata["publish"]
    assert "logo" in metadata["publish"]["blocks"]

    # Check annotate section structure
    assert "notes" in metadata["annotate"]
    # Note: byline is in describe section, not annotate (per Datawrapper API)

    # Check custom section (should be a dict)
    assert isinstance(metadata["custom"], dict)


if __name__ == "__main__":
    test_metadata_section_order()
    test_metadata_content_structure()
    print("All metadata structure tests passed!")

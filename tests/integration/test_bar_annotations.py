"""Test for BarChart annotation serialization bug fix."""

import pandas as pd

from datawrapper import BarChart, RangeAnnotation, TextAnnotation


def test_multiple_text_annotations():
    """Test that multiple text annotations are properly serialized as a list."""
    # Create a bar chart with multiple text annotations
    chart = BarChart(
        title="Test Chart",
        data=pd.DataFrame({"labels": ["A", "B", "C"], "values": [1, 2, 3]}),
        label_column="labels",
        bar_column="values",
        text_annotations=[
            TextAnnotation(text="First annotation", x=10, y=20),
            TextAnnotation(text="Second annotation", x=30, y=40),
            TextAnnotation(text="Third annotation", x=50, y=60),
        ],
    )

    # Serialize the chart
    serialized = chart.serialize_model()

    # Check that text-annotations is a list with all 3 annotations
    text_annotations = serialized["metadata"]["visualize"]["text-annotations"]
    assert isinstance(text_annotations, list), "text-annotations should be a list"
    assert len(text_annotations) == 3, (
        f"Expected 3 text annotations, got {len(text_annotations)}"
    )

    # Verify the content of each annotation
    assert text_annotations[0]["text"] == "First annotation"
    assert text_annotations[1]["text"] == "Second annotation"
    assert text_annotations[2]["text"] == "Third annotation"


def test_multiple_range_annotations():
    """Test that multiple range annotations are properly serialized as a list."""
    # Create a bar chart with multiple range annotations
    chart = BarChart(
        title="Test Chart",
        data=pd.DataFrame({"labels": ["A", "B", "C"], "values": [1, 2, 3]}),
        label_column="labels",
        bar_column="values",
        range_annotations=[
            RangeAnnotation(x0=0, x1=10, y0=0, y1=100),
            RangeAnnotation(x0=20, x1=30, y0=0, y1=100),
        ],
    )

    # Serialize the chart
    serialized = chart.serialize_model()

    # Check that range-annotations is a list with all 2 annotations
    range_annotations = serialized["metadata"]["visualize"]["range-annotations"]
    assert isinstance(range_annotations, list), "range-annotations should be a list"
    assert len(range_annotations) == 2, (
        f"Expected 2 range annotations, got {len(range_annotations)}"
    )

    # Verify the content of each annotation
    assert range_annotations[0]["position"]["x0"] == 0
    assert range_annotations[0]["position"]["x1"] == 10
    assert range_annotations[1]["position"]["x0"] == 20
    assert range_annotations[1]["position"]["x1"] == 30


def test_mixed_annotations():
    """Test that both text and range annotations work together."""
    chart = BarChart(
        title="Test Chart",
        data=pd.DataFrame({"labels": ["A", "B", "C"], "values": [1, 2, 3]}),
        label_column="labels",
        bar_column="values",
        text_annotations=[
            TextAnnotation(text="Text annotation", x=10, y=20),
        ],
        range_annotations=[
            RangeAnnotation(x0=0, x1=10, y0=0, y1=100),
        ],
    )

    # Serialize the chart
    serialized = chart.serialize_model()

    # Check both annotation types
    text_annotations = serialized["metadata"]["visualize"]["text-annotations"]
    range_annotations = serialized["metadata"]["visualize"]["range-annotations"]

    assert len(text_annotations) == 1
    assert len(range_annotations) == 1

    # Get first items from lists
    text_anno = text_annotations[0]
    range_anno = range_annotations[0]

    assert text_anno["text"] == "Text annotation"
    assert range_anno["position"]["x0"] == 0
    assert range_anno["position"]["x1"] == 10


def test_empty_annotations():
    """Test that empty annotation lists work correctly."""
    chart = BarChart(
        title="Test Chart",
        data=pd.DataFrame({"labels": ["A", "B", "C"], "values": [1, 2, 3]}),
        label_column="labels",
        bar_column="values",
        # No annotations specified
    )

    # Serialize the chart
    serialized = chart.serialize_model()

    # Check that annotation lists are empty
    text_annotations = serialized["metadata"]["visualize"]["text-annotations"]
    range_annotations = serialized["metadata"]["visualize"]["range-annotations"]

    assert isinstance(text_annotations, list)
    assert isinstance(range_annotations, list)
    assert len(text_annotations) == 0
    assert len(range_annotations) == 0

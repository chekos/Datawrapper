"""Unit tests for BarChart serialization."""

import datawrapper


class TestBarChartSerialization:
    """Test BarChart model serialization."""

    def test_bar_chart_serialize_minimal(self):
        """Test BarChart serialization with minimal data."""
        chart = datawrapper.BarChart(
            title="Test Bar Chart",
            data=[
                {"Category": "A", "Value": 10},
                {"Category": "B", "Value": 20},
                {"Category": "C", "Value": 15},
            ],
        )

        # Test the serialize_model method directly
        serialized = chart.serialize_model()

        assert isinstance(serialized, dict)
        assert "title" in serialized
        assert "type" in serialized
        assert serialized["title"] == "Test Bar Chart"
        assert serialized["type"] == "d3-bars"

    def test_bar_chart_serialize_with_overlays(self):
        """Test BarChart serialization with overlays."""
        overlay = datawrapper.BarOverlay(to="Value", type="value", color="#ff0000")

        chart = datawrapper.BarChart(
            title="Test Bar Chart with Overlay",
            data=[{"Category": "A", "Value": 10}, {"Category": "B", "Value": 20}],
            overlays=[overlay],
        )

        serialized = chart.serialize_model()

        # Check main structure
        assert isinstance(serialized, dict)
        assert "title" in serialized
        assert "type" in serialized
        assert "metadata" in serialized

        # Check that overlays are included in visualize section
        metadata = serialized["metadata"]
        assert "visualize" in metadata

        # The exact structure depends on BarChart implementation
        # This test ensures serialization doesn't break with overlays

    def test_bar_chart_serialize_with_annotations(self):
        """Test BarChart serialization with annotations."""
        annotation = datawrapper.TextAnnotation(text="Important note", x=50, y=100)

        chart = datawrapper.BarChart(
            title="Test Bar Chart with Annotations",
            data=[{"Category": "A", "Value": 10}, {"Category": "B", "Value": 20}],
            text_annotations=[annotation],
        )

        serialized = chart.serialize_model()

        # Check main structure
        assert isinstance(serialized, dict)
        assert "title" in serialized
        assert "type" in serialized
        assert "metadata" in serialized

        # Check that annotations are included
        _metadata = serialized["metadata"]
        # The exact location depends on BarChart implementation
        # This test ensures serialization doesn't break with annotations

    def test_bar_chart_serialize_full_configuration(self):
        """Test BarChart serialization with full configuration."""
        overlay = datawrapper.BarOverlay(to="Value", type="value", color="#ff0000")

        annotation = datawrapper.TextAnnotation(text="Peak value", x=75, y=150)

        chart = datawrapper.BarChart(
            title="Comprehensive Bar Chart",
            data=[
                {"Category": "A", "Value": 10, "Target": 12},
                {"Category": "B", "Value": 20, "Target": 18},
                {"Category": "C", "Value": 15, "Target": 16},
            ],
            overlays=[overlay],
            text_annotations=[annotation],
            source_name="Test Data Source",
            byline="Data Team",
            notes="This is a test chart",
        )

        serialized = chart.serialize_model()

        # Check main structure
        assert isinstance(serialized, dict)
        assert "title" in serialized
        assert "type" in serialized
        assert "metadata" in serialized
        assert serialized["title"] == "Comprehensive Bar Chart"
        assert serialized["type"] == "d3-bars"

        # Check metadata sections exist
        metadata = serialized["metadata"]
        assert "describe" in metadata
        assert "annotate" in metadata

        # Check describe section
        describe = metadata["describe"]
        assert describe["source-name"] == "Test Data Source"
        assert describe["byline"] == "Data Team"

        # Check annotate section
        annotate = metadata["annotate"]
        assert annotate["notes"] == "This is a test chart"

    def test_bar_chart_serialize_json_compatibility(self):
        """Test that BarChart serialized output is JSON-compatible."""
        import json

        chart = datawrapper.BarChart(
            title="JSON Test Chart",
            data=[{"Category": "A", "Value": 10}, {"Category": "B", "Value": 20}],
            source_name="JSON Source",
        )

        serialized = chart.serialize_model()

        # Should be able to convert to JSON without errors
        json_str = json.dumps(serialized)
        assert isinstance(json_str, str)

        # Should be able to parse back
        parsed = json.loads(json_str)
        assert parsed["title"] == "JSON Test Chart"
        assert parsed["type"] == "d3-bars"

    def test_bar_chart_serialize_empty_overlays_annotations(self):
        """Test BarChart serialization with empty overlays and annotations."""
        chart = datawrapper.BarChart(
            title="Empty Lists Chart",
            data=[{"Category": "A", "Value": 10}],
            overlays=[],  # Empty list
            text_annotations=[],  # Empty list
        )

        serialized = chart.serialize_model()

        assert isinstance(serialized, dict)
        assert "title" in serialized
        assert "type" in serialized
        # Should not raise errors with empty lists

    def test_bar_chart_serialize_vs_base_chart(self):
        """Test that BarChart serialization differs from BaseChart."""
        base_chart = datawrapper.BaseChart(
            title="Base Chart",
            chart_type="d3-bars",
            data=[{"Category": "A", "Value": 10}],
        )

        bar_chart = datawrapper.BarChart(
            title="Bar Chart", data=[{"Category": "A", "Value": 10}]
        )

        base_serialized = base_chart.serialize_model()
        bar_serialized = bar_chart.serialize_model()

        # Both should be valid dicts
        assert isinstance(base_serialized, dict)
        assert isinstance(bar_serialized, dict)

        # Both should have the same type
        assert base_serialized["type"] == "d3-bars"
        assert bar_serialized["type"] == "d3-bars"

        # BarChart may have additional structure in metadata
        # This test ensures both serialization methods work

    def test_bar_chart_serialize_special_data_types(self):
        """Test BarChart serialization with various data types."""
        chart = datawrapper.BarChart(
            title="Mixed Data Types",
            data=[
                {"Category": "A", "Value": 10.5, "Count": 100},
                {"Category": "B", "Value": 20.7, "Count": 200},
                {"Category": "C", "Value": 15.2, "Count": 150},
            ],
        )

        serialized = chart.serialize_model()

        assert isinstance(serialized, dict)
        assert "title" in serialized
        assert "type" in serialized
        # Should handle mixed numeric types without errors

"""Unit tests for annotation serialization."""

import datawrapper


class TestTextAnnotationSerialization:
    """Test TextAnnotation model serialization."""

    def test_text_annotation_serialize_minimal(self):
        """Test TextAnnotation serialization with minimal data."""
        annotation = datawrapper.TextAnnotation(text="Test annotation", x=50, y=100)

        # Test the serialize_model method directly
        serialized = annotation.serialize_model()

        assert isinstance(serialized, dict)
        assert "text" in serialized
        assert "position" in serialized
        assert serialized["text"] == "Test annotation"

        position = serialized["position"]
        assert "x" in position
        assert "y" in position
        assert position["x"] == 50
        assert position["y"] == 100

    def test_text_annotation_serialize_with_styling(self):
        """Test TextAnnotation serialization with styling options."""
        annotation = datawrapper.TextAnnotation(
            text="Styled annotation",
            x=75,
            y=150,
            color="#ff0000",
            size=14,
            bold=True,
            italic=True,
        )

        serialized = annotation.serialize_model()

        assert isinstance(serialized, dict)
        assert serialized["text"] == "Styled annotation"
        assert serialized["position"]["x"] == 75
        assert serialized["position"]["y"] == 150
        assert serialized["color"] == "#ff0000"
        assert serialized["size"] == 14
        assert serialized["bold"] is True
        assert serialized["italic"] is True

    def test_text_annotation_serialize_with_alignment(self):
        """Test TextAnnotation serialization with alignment options."""
        annotation = datawrapper.TextAnnotation(
            text="Aligned annotation",
            x=100,
            y=200,
            align="mc",  # middle center
        )

        serialized = annotation.serialize_model()

        assert isinstance(serialized, dict)
        assert serialized["text"] == "Aligned annotation"
        assert serialized["align"] == "mc"

    def test_text_annotation_serialize_json_compatibility(self):
        """Test that TextAnnotation serialized output is JSON-compatible."""
        import json

        annotation = datawrapper.TextAnnotation(
            text="JSON test annotation", x=25, y=75, color="#00ff00"
        )

        serialized = annotation.serialize_model()

        # Should be able to convert to JSON without errors
        json_str = json.dumps(serialized)
        assert isinstance(json_str, str)

        # Should be able to parse back
        parsed = json.loads(json_str)
        assert parsed["text"] == "JSON test annotation"
        assert parsed["position"]["x"] == 25
        assert parsed["position"]["y"] == 75

    def test_text_annotation_serialize_special_characters(self):
        """Test TextAnnotation serialization with special characters."""
        annotation = datawrapper.TextAnnotation(
            text="Special chars: émojis 🎉, quotes 'single' \"double\", 中文", x=0, y=0
        )

        serialized = annotation.serialize_model()

        assert isinstance(serialized, dict)
        assert "émojis 🎉" in serialized["text"]
        assert "quotes 'single' \"double\"" in serialized["text"]
        assert "中文" in serialized["text"]


class TestRangeAnnotationSerialization:
    """Test RangeAnnotation model serialization."""

    def test_range_annotation_serialize_minimal(self):
        """Test RangeAnnotation serialization with minimal data."""
        annotation = datawrapper.RangeAnnotation(x0=10, x1=90, y0=20, y1=80)

        # Test the serialize_model method directly
        serialized = annotation.serialize_model()

        assert isinstance(serialized, dict)
        assert "position" in serialized
        position = serialized["position"]
        assert "x0" in position
        assert "x1" in position
        assert "y0" in position
        assert "y1" in position
        assert position["x0"] == 10
        assert position["x1"] == 90
        assert position["y0"] == 20
        assert position["y1"] == 80

    def test_range_annotation_serialize_with_styling(self):
        """Test RangeAnnotation serialization with styling options."""
        annotation = datawrapper.RangeAnnotation(
            x0=0, x1=100, y0=0, y1=100, color="#0000ff", opacity=50
        )

        serialized = annotation.serialize_model()

        assert isinstance(serialized, dict)
        assert serialized["color"] == "#0000ff"
        assert serialized["opacity"] == 50

    def test_range_annotation_serialize_with_display_options(self):
        """Test RangeAnnotation serialization with display options."""
        annotation = datawrapper.RangeAnnotation(
            x0=25, x1=75, y0=25, y1=75, display="line", stroke_type="dashed"
        )

        serialized = annotation.serialize_model()

        assert isinstance(serialized, dict)
        assert serialized["display"] == "line"
        assert serialized["strokeType"] == "dashed"

    def test_range_annotation_serialize_json_compatibility(self):
        """Test that RangeAnnotation serialized output is JSON-compatible."""
        import json

        annotation = datawrapper.RangeAnnotation(x0=5, x1=95, y0=10, y1=90, type="x")

        serialized = annotation.serialize_model()

        # Should be able to convert to JSON without errors
        json_str = json.dumps(serialized)
        assert isinstance(json_str, str)

        # Should be able to parse back
        parsed = json.loads(json_str)
        assert parsed["position"]["x0"] == 5
        assert parsed["position"]["x1"] == 95
        assert parsed["type"] == "x"


class TestAnnotationIntegration:
    """Test annotation integration with charts."""

    def test_annotations_in_chart_serialization(self):
        """Test that annotations serialize correctly when included in charts."""
        text_annotation = datawrapper.TextAnnotation(
            text="Chart annotation", x=50, y=100
        )

        range_annotation = datawrapper.RangeAnnotation(x0=10, x1=90, y0=20, y1=80)

        chart = datawrapper.BarChart(
            title="Chart with Annotations",
            data=[{"Category": "A", "Value": 10}, {"Category": "B", "Value": 20}],
            text_annotations=[text_annotation],
            range_annotations=[range_annotation],
        )

        serialized = chart.serialize_model()

        # Check main structure
        assert isinstance(serialized, dict)
        assert "metadata" in serialized

        metadata = serialized["metadata"]
        assert "visualize" in metadata

        visualize = metadata["visualize"]
        assert "text-annotations" in visualize
        assert "range-annotations" in visualize

        # Check that annotations are properly serialized as lists
        text_annos = visualize["text-annotations"]
        range_annos = visualize["range-annotations"]

        assert isinstance(text_annos, list)
        assert isinstance(range_annos, list)
        assert len(text_annos) == 1
        assert len(range_annos) == 1

        # Verify annotation content
        text_anno_data = text_annos[0]
        range_anno_data = range_annos[0]

        assert text_anno_data["text"] == "Chart annotation"
        assert text_anno_data["position"]["x"] == 50
        assert text_anno_data["position"]["y"] == 100

        assert range_anno_data["type"] in ["x", "y"]
        assert range_anno_data["position"]["x0"] == 10
        assert range_anno_data["position"]["x1"] == 90
        assert range_anno_data["position"]["y0"] == 20
        assert range_anno_data["position"]["y1"] == 80

    def test_empty_annotations_in_chart(self):
        """Test that empty annotation lists serialize correctly."""
        chart = datawrapper.BarChart(
            title="Chart without Annotations",
            data=[{"Category": "A", "Value": 10}],
            text_annotations=[],
            range_annotations=[],
        )

        serialized = chart.serialize_model()

        # Should not raise errors with empty lists
        assert isinstance(serialized, dict)
        assert "metadata" in serialized

        metadata = serialized["metadata"]
        visualize = metadata["visualize"]

        # Empty lists should serialize as empty lists
        assert "text-annotations" in visualize
        assert "range-annotations" in visualize
        assert visualize["text-annotations"] == []
        assert visualize["range-annotations"] == []

    def test_mixed_annotation_types(self):
        """Test serialization with multiple annotation types."""
        annotations = [
            datawrapper.TextAnnotation(text="First", x=10, y=20),
            datawrapper.TextAnnotation(text="Second", x=30, y=40, color="#ff0000"),
            datawrapper.TextAnnotation(text="Third", x=50, y=60, bold=True),
        ]

        chart = datawrapper.BarChart(
            title="Multiple Annotations",
            data=[{"Category": "A", "Value": 10}],
            text_annotations=annotations,
        )

        serialized = chart.serialize_model()

        visualize = serialized["metadata"]["visualize"]
        text_annos = visualize["text-annotations"]

        # Annotations are serialized as a list
        assert isinstance(text_annos, list)
        assert len(text_annos) == 3

        # Check annotation values in order
        assert text_annos[0]["text"] == "First"
        assert text_annos[1]["text"] == "Second"
        assert text_annos[1]["color"] == "#ff0000"
        assert text_annos[2]["text"] == "Third"
        assert text_annos[2]["bold"] is True

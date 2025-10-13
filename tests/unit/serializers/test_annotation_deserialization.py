"""Tests for annotation deserialization methods."""

from datawrapper.charts.annos import RangeAnnotation, TextAnnotation
from datawrapper.charts.base import BaseChart


class TestTextAnnotationDeserialization:
    """Test TextAnnotation.deserialize method."""

    def test_deserialize_basic_text_annotation(self):
        """Test deserializing a basic text annotation."""
        api_data = {
            "test-123": {
                "text": "Important note",
                "position": {"x": 100, "y": 200},
            }
        }

        result = TextAnnotation.deserialize_model(api_data)

        assert len(result) == 1
        assert result[0]["id"] == "test-123"
        assert result[0]["text"] == "Important note"

    def test_deserialize_with_all_fields(self):
        """Test deserializing with all possible fields."""
        api_data = {
            "anno-456": {
                "text": "Full annotation",
                "position": {"x": 50, "y": 75},
                "align": "center",
                "bold": True,
                "color": "#FF0000",
                "size": 14,
                "italic": True,
                "underline": True,
                "width": 200,
            }
        }

        result = TextAnnotation.deserialize_model(api_data)

        assert len(result) == 1
        assert result[0]["id"] == "anno-456"
        assert result[0]["text"] == "Full annotation"

    def test_deserialize_preserves_uuid(self):
        """Test that UUID is preserved during deserialization."""
        api_data = {
            "uuid-789": {
                "text": "Test",
                "position": {"x": 0, "y": 0},
            }
        }

        result = TextAnnotation.deserialize_model(api_data)

        assert len(result) == 1
        assert result[0]["id"] == "uuid-789"


class TestRangeAnnotationDeserialization:
    """Test RangeAnnotation.deserialize method."""

    def test_deserialize_basic_range_annotation(self):
        """Test deserializing a basic range annotation."""
        api_data = {
            "range-123": {
                "position": {"x0": 10, "x1": 20, "y0": 0, "y1": 0},
            }
        }

        result = RangeAnnotation.deserialize_model(api_data)

        assert len(result) == 1
        assert result[0]["id"] == "range-123"

    def test_deserialize_with_all_fields(self):
        """Test deserializing with all possible fields."""
        api_data = {
            "range-456": {
                "position": {"x0": 5, "x1": 15, "y0": 100, "y1": 200},
                "color": "#00FF00",
                "opacity": 50,
                "type": "x",
                "display": "range",
            }
        }

        result = RangeAnnotation.deserialize_model(api_data)

        assert len(result) == 1
        assert result[0]["id"] == "range-456"
        assert result[0]["color"] == "#00FF00"

    def test_deserialize_preserves_uuid(self):
        """Test that UUID is preserved during deserialization."""
        api_data = {
            "uuid-range-789": {
                "position": {"x0": 0, "x1": 100, "y0": 0, "y1": 0},
            }
        }

        result = RangeAnnotation.deserialize_model(api_data)

        assert len(result) == 1
        assert result[0]["id"] == "uuid-range-789"


class TestBaseChartDeserializeAnnotations:
    """Test BaseChart._deserialize_annotations helper method."""

    def test_deserialize_empty_dict(self):
        """Test deserializing an empty dict returns empty list."""
        result = BaseChart._deserialize_annotations({}, TextAnnotation)
        assert result == []

    def test_deserialize_none(self):
        """Test deserializing None returns empty list."""
        result = BaseChart._deserialize_annotations(None, TextAnnotation)
        assert result == []

    def test_deserialize_empty_list(self):
        """Test deserializing an empty list returns empty list."""
        result = BaseChart._deserialize_annotations([], TextAnnotation)
        assert result == []

    def test_deserialize_dict_with_text_annotations(self):
        """Test deserializing dict of text annotations."""
        api_data = {
            "anno-1": {"text": "First", "x": 10, "y": 20},
            "anno-2": {"text": "Second", "x": 30, "y": 40},
        }

        result = BaseChart._deserialize_annotations(api_data, TextAnnotation)

        assert len(result) == 2
        assert result[0]["id"] == "anno-1"
        assert result[0]["text"] == "First"
        assert result[1]["id"] == "anno-2"
        assert result[1]["text"] == "Second"

    def test_deserialize_dict_with_range_annotations(self):
        """Test deserializing dict of range annotations."""
        api_data = {
            "range-1": {"x0": 0, "x1": 10},
            "range-2": {"x0": 20, "x1": 30},
        }

        result = BaseChart._deserialize_annotations(api_data, RangeAnnotation)

        assert len(result) == 2
        assert result[0]["id"] == "range-1"
        assert result[0]["x0"] == 0
        assert result[1]["id"] == "range-2"
        assert result[1]["x0"] == 20

    def test_deserialize_list_of_annotations(self):
        """Test deserializing list of annotations (already deserialized)."""
        api_data = [
            {"id": "anno-1", "text": "First", "x": 10, "y": 20},
            {"id": "anno-2", "text": "Second", "x": 30, "y": 40},
        ]

        result = BaseChart._deserialize_annotations(api_data, TextAnnotation)

        # Should return the list as-is since it's already in the correct format
        assert result == api_data

    def test_deserialize_preserves_all_annotation_properties(self):
        """Test that all annotation properties are preserved."""
        api_data = {
            "complex-anno": {
                "text": "Complex",
                "x": 100,
                "y": 200,
                "align": "center",
                "bold": True,
                "color": "#FF0000",
                "fontSize": 16,
                "italic": True,
                "underline": True,
                "width": 300,
            }
        }

        result = BaseChart._deserialize_annotations(api_data, TextAnnotation)

        assert len(result) == 1
        anno = result[0]
        assert anno["id"] == "complex-anno"
        assert anno["text"] == "Complex"
        assert anno["x"] == 100
        assert anno["y"] == 200
        assert anno["align"] == "center"
        assert anno["bold"] is True
        assert anno["color"] == "#FF0000"
        assert anno["fontSize"] == 16
        assert anno["italic"] is True
        assert anno["underline"] is True
        assert anno["width"] == 300

    def test_deserialize_multiple_annotations_maintains_order(self):
        """Test that annotation order is maintained during deserialization."""
        # Note: dict order is preserved in Python 3.7+
        api_data = {
            "first": {"text": "1", "x": 1, "y": 1},
            "second": {"text": "2", "x": 2, "y": 2},
            "third": {"text": "3", "x": 3, "y": 3},
        }

        result = BaseChart._deserialize_annotations(api_data, TextAnnotation)

        assert len(result) == 3
        assert result[0]["text"] == "1"
        assert result[1]["text"] == "2"
        assert result[2]["text"] == "3"

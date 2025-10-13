"""Tests for annotation deserialization methods."""

from datawrapper.charts.annos import RangeAnnotation, TextAnnotation


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

"""Tests for permissive RangeAnnotation position handling."""

from datawrapper.charts.annos import RangeAnnotation


class TestRangeAnnotationPermissive:
    """Test that RangeAnnotation handles different position configurations."""

    def test_vertical_line(self):
        """Test creating a vertical line annotation (only x0 needed)."""
        anno = RangeAnnotation(
            type="x",
            display="line",
            x0="2020-01-01",
        )
        assert anno.x0 == "2020-01-01"
        assert anno.x1 is None
        assert anno.y0 is None
        assert anno.y1 is None

        # Verify serialization only includes x0
        serialized = anno.serialize_model()
        assert serialized["position"]["x0"] == "2020-01-01"
        assert "x1" not in serialized["position"]
        assert "y0" not in serialized["position"]
        assert "y1" not in serialized["position"]

    def test_vertical_range(self):
        """Test creating a vertical range annotation (x0 and x1 needed)."""
        anno = RangeAnnotation(
            type="x",
            display="range",
            x0="2020-01-01",
            x1="2021-01-01",
        )
        assert anno.x0 == "2020-01-01"
        assert anno.x1 == "2021-01-01"
        assert anno.y0 is None
        assert anno.y1 is None

        # Verify serialization only includes x0 and x1
        serialized = anno.serialize_model()
        assert serialized["position"]["x0"] == "2020-01-01"
        assert serialized["position"]["x1"] == "2021-01-01"
        assert "y0" not in serialized["position"]
        assert "y1" not in serialized["position"]

    def test_horizontal_line(self):
        """Test creating a horizontal line annotation (only y0 needed)."""
        anno = RangeAnnotation(
            type="y",
            display="line",
            y0=50,
        )
        assert anno.x0 is None
        assert anno.x1 is None
        assert anno.y0 == 50
        assert anno.y1 is None

        # Verify serialization only includes y0
        serialized = anno.serialize_model()
        assert "x0" not in serialized["position"]
        assert "x1" not in serialized["position"]
        assert serialized["position"]["y0"] == 50
        assert "y1" not in serialized["position"]

    def test_horizontal_range(self):
        """Test creating a horizontal range annotation (y0 and y1 needed)."""
        anno = RangeAnnotation(
            type="y",
            display="range",
            y0=50,
            y1=100,
        )
        assert anno.x0 is None
        assert anno.x1 is None
        assert anno.y0 == 50
        assert anno.y1 == 100

        # Verify serialization only includes y0 and y1
        serialized = anno.serialize_model()
        assert "x0" not in serialized["position"]
        assert "x1" not in serialized["position"]
        assert serialized["position"]["y0"] == 50
        assert serialized["position"]["y1"] == 100

    def test_api_format_with_duplicate_positions(self):
        """Test deserializing API format where positions are duplicated."""
        # This mimics the actual API response format where vertical ranges
        # have x0/x1 duplicated in y0/y1
        api_data = {
            "anno-id-1": {
                "type": "x",
                "color": "#333333",
                "display": "range",
                "opacity": "10",
                "position": {
                    "x0": "1939M09",
                    "x1": "1945M09",
                    "y0": "1939M09",  # Duplicate of x0
                    "y1": "1945M09",  # Duplicate of x1
                },
                "strokeType": "solid",
                "strokeWidth": 1,
            }
        }

        result = RangeAnnotation.deserialize_model(api_data)
        assert len(result) == 1
        assert result[0]["id"] == "anno-id-1"
        assert result[0]["position"]["x0"] == "1939M09"
        assert result[0]["position"]["x1"] == "1945M09"
        # The duplicates are preserved in deserialization
        assert result[0]["position"]["y0"] == "1939M09"
        assert result[0]["position"]["y1"] == "1945M09"

    def test_mixed_numeric_and_string_positions(self):
        """Test that both numeric and string positions work."""
        # Numeric positions (for y-axis values)
        anno1 = RangeAnnotation(
            type="y",
            display="range",
            y0=0,
            y1=100,
        )
        serialized1 = anno1.serialize_model()
        assert serialized1["position"]["y0"] == 0
        assert serialized1["position"]["y1"] == 100

        # String positions (for x-axis dates)
        anno2 = RangeAnnotation(
            type="x",
            display="range",
            x0="2020-01-01",
            x1="2021-01-01",
        )
        serialized2 = anno2.serialize_model()
        assert serialized2["position"]["x0"] == "2020-01-01"
        assert serialized2["position"]["x1"] == "2021-01-01"

    def test_empty_position_dict_when_all_none(self):
        """Test that position dict is empty when all positions are None."""
        anno = RangeAnnotation(type="x", display="line")
        serialized = anno.serialize_model()
        assert serialized["position"] == {}

    def test_partial_positions_preserved(self):
        """Test that any combination of positions can be set."""
        # Only x0 and y0
        anno = RangeAnnotation(
            type="x",
            display="range",
            x0="2020",
            y0=50,
        )
        serialized = anno.serialize_model()
        assert serialized["position"]["x0"] == "2020"
        assert serialized["position"]["y0"] == 50
        assert "x1" not in serialized["position"]
        assert "y1" not in serialized["position"]

"""Unit tests for ColorCategory utility class."""

from datawrapper.charts.serializers import ColorCategory


class TestColorCategorySerialize:
    """Test ColorCategory.serialize() method."""

    def test_serialize_empty_dict(self):
        """Test serializing an empty dictionary."""
        result = ColorCategory.serialize({})
        assert result == {"map": {}}

    def test_serialize_simple_mapping(self):
        """Test serializing a simple color mapping."""
        color_map = {
            "Category A": "#FF0000",
            "Category B": "#00FF00",
            "Category C": "#0000FF",
        }
        result = ColorCategory.serialize(color_map)
        assert result == {"map": color_map}

    def test_serialize_with_special_characters(self):
        """Test serializing with special characters in keys."""
        color_map = {
            "Category-1": "#FF0000",
            "Category 2": "#00FF00",
            "Category_3": "#0000FF",
        }
        result = ColorCategory.serialize(color_map)
        assert result == {"map": color_map}

    def test_serialize_preserves_color_formats(self):
        """Test that different color formats are preserved."""
        color_map = {
            "Hex": "#FF0000",
            "RGB": "rgb(255, 0, 0)",
            "Named": "red",
        }
        result = ColorCategory.serialize(color_map)
        assert result == {"map": color_map}


class TestColorCategoryDeserialize:
    """Test ColorCategory.deserialize() method."""

    def test_deserialize_none(self):
        """Test deserializing None returns empty dicts and lists."""
        result = ColorCategory.deserialize(None)
        assert result == {
            "color_category": {},
            "category_labels": {},
            "category_order": [],
            "exclude_from_color_key": [],
        }

    def test_deserialize_empty_dict(self):
        """Test deserializing an empty dictionary."""
        result = ColorCategory.deserialize({})
        assert result == {
            "color_category": {},
            "category_labels": {},
            "category_order": [],
            "exclude_from_color_key": [],
        }

    def test_deserialize_dict_with_map(self):
        """Test deserializing a dictionary with 'map' key."""
        color_data = {
            "map": {
                "Category A": "#FF0000",
                "Category B": "#00FF00",
            }
        }
        result = ColorCategory.deserialize(color_data)
        assert result == {
            "color_category": {
                "Category A": "#FF0000",
                "Category B": "#00FF00",
            },
            "category_labels": {},
            "category_order": [],
            "exclude_from_color_key": [],
        }

    def test_deserialize_dict_without_map(self):
        """Test deserializing a dictionary without 'map' key."""
        color_data = {
            "Category A": "#FF0000",
            "Category B": "#00FF00",
        }
        result = ColorCategory.deserialize(color_data)
        assert result == {
            "color_category": {},
            "category_labels": {},
            "category_order": [],
            "exclude_from_color_key": [],
        }

    def test_deserialize_dict_with_empty_map(self):
        """Test deserializing a dictionary with empty 'map'."""
        color_data = {"map": {}}
        result = ColorCategory.deserialize(color_data)
        assert result == {
            "color_category": {},
            "category_labels": {},
            "category_order": [],
            "exclude_from_color_key": [],
        }

    def test_deserialize_dict_with_map_and_other_keys(self):
        """Test deserializing a dictionary with 'map' and other keys."""
        color_data = {
            "map": {
                "Category A": "#FF0000",
            },
            "other_key": "other_value",
        }
        result = ColorCategory.deserialize(color_data)
        assert result == {
            "color_category": {
                "Category A": "#FF0000",
            },
            "category_labels": {},
            "category_order": [],
            "exclude_from_color_key": [],
        }

    def test_deserialize_preserves_color_formats(self):
        """Test that different color formats are preserved during deserialization."""
        color_data = {
            "map": {
                "Hex": "#FF0000",
                "RGB": "rgb(255, 0, 0)",
                "Named": "red",
            }
        }
        result = ColorCategory.deserialize(color_data)
        assert result == {
            "color_category": {
                "Hex": "#FF0000",
                "RGB": "rgb(255, 0, 0)",
                "Named": "red",
            },
            "category_labels": {},
            "category_order": [],
            "exclude_from_color_key": [],
        }

    def test_deserialize_with_all_fields(self):
        """Test deserializing with all optional fields present."""
        color_data = {
            "map": {
                "A": "#FF0000",
                "B": "#00FF00",
            },
            "categoryLabels": {
                "A": "Category A",
                "B": "Category B",
            },
            "categoryOrder": ["B", "A"],
            "excludeFromKey": ["A"],
        }
        result = ColorCategory.deserialize(color_data)
        assert result == {
            "color_category": {
                "A": "#FF0000",
                "B": "#00FF00",
            },
            "category_labels": {
                "A": "Category A",
                "B": "Category B",
            },
            "category_order": ["B", "A"],
            "exclude_from_color_key": ["A"],
        }


class TestColorCategoryRoundTrip:
    """Test round-trip serialization/deserialization."""

    def test_roundtrip_empty(self):
        """Test round-trip with empty dictionary."""
        original = {}
        serialized = ColorCategory.serialize(original)
        deserialized = ColorCategory.deserialize(serialized)
        assert deserialized["color_category"] == original

    def test_roundtrip_simple_mapping(self):
        """Test round-trip with simple color mapping."""
        original = {
            "Category A": "#FF0000",
            "Category B": "#00FF00",
            "Category C": "#0000FF",
        }
        serialized = ColorCategory.serialize(original)
        deserialized = ColorCategory.deserialize(serialized)
        assert deserialized["color_category"] == original

    def test_roundtrip_complex_mapping(self):
        """Test round-trip with complex color mapping."""
        original = {
            "Category-1": "#FF0000",
            "Category 2": "rgb(0, 255, 0)",
            "Category_3": "blue",
            "Category 4 (Special)": "#FFFF00",
        }
        serialized = ColorCategory.serialize(original)
        deserialized = ColorCategory.deserialize(serialized)
        assert deserialized["color_category"] == original

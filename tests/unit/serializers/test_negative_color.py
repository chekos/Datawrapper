"""Unit tests for NegativeColor serializer utility."""

from datawrapper.charts.serializers import NegativeColor


class TestNegativeColorSerialize:
    """Test NegativeColor.serialize() method."""

    def test_serialize_none(self):
        """Test serializing None (disabled)."""
        result = NegativeColor.serialize(None)
        assert result == {"enabled": False, "value": ""}

    def test_serialize_color_string(self):
        """Test serializing a color string (enabled)."""
        result = NegativeColor.serialize("#FF0000")
        assert result == {"enabled": True, "value": "#FF0000"}

    def test_serialize_different_colors(self):
        """Test serializing various color formats."""
        # Hex color
        result = NegativeColor.serialize("#de2d26")
        assert result == {"enabled": True, "value": "#de2d26"}

        # RGB color
        result = NegativeColor.serialize("rgb(255, 0, 0)")
        assert result == {"enabled": True, "value": "rgb(255, 0, 0)"}

        # Named color
        result = NegativeColor.serialize("red")
        assert result == {"enabled": True, "value": "red"}


class TestNegativeColorDeserialize:
    """Test NegativeColor.deserialize() method."""

    def test_deserialize_disabled(self):
        """Test deserializing disabled negative color."""
        api_obj = {"enabled": False, "value": ""}
        result = NegativeColor.deserialize(api_obj)
        assert result is None

    def test_deserialize_enabled(self):
        """Test deserializing enabled negative color."""
        api_obj = {"enabled": True, "value": "#FF0000"}
        result = NegativeColor.deserialize(api_obj)
        assert result == "#FF0000"

    def test_deserialize_enabled_with_empty_value(self):
        """Test deserializing enabled but with empty value."""
        api_obj = {"enabled": True, "value": ""}
        result = NegativeColor.deserialize(api_obj)
        assert result == ""

    def test_deserialize_disabled_with_value(self):
        """Test deserializing disabled but with a value (value should be ignored)."""
        api_obj = {"enabled": False, "value": "#FF0000"}
        result = NegativeColor.deserialize(api_obj)
        assert result is None

    def test_deserialize_none(self):
        """Test deserializing None input."""
        result = NegativeColor.deserialize(None)
        assert result is None

    def test_deserialize_empty_dict(self):
        """Test deserializing empty dict."""
        result = NegativeColor.deserialize({})
        assert result is None

    def test_deserialize_missing_enabled_key(self):
        """Test deserializing dict without 'enabled' key."""
        api_obj = {"value": "#FF0000"}
        result = NegativeColor.deserialize(api_obj)
        assert result is None

    def test_deserialize_missing_value_key(self):
        """Test deserializing dict without 'value' key."""
        api_obj = {"enabled": True}
        result = NegativeColor.deserialize(api_obj)
        assert result == ""


class TestNegativeColorRoundTrip:
    """Test round-trip serialization/deserialization."""

    def test_roundtrip_none(self):
        """Test round-trip with None."""
        original = None
        serialized = NegativeColor.serialize(original)
        deserialized = NegativeColor.deserialize(serialized)
        assert deserialized == original

    def test_roundtrip_color(self):
        """Test round-trip with a color."""
        original = "#de2d26"
        serialized = NegativeColor.serialize(original)
        deserialized = NegativeColor.deserialize(serialized)
        assert deserialized == original

    def test_roundtrip_various_colors(self):
        """Test round-trip with various color formats."""
        colors = ["#FF0000", "#de2d26", "rgb(255, 0, 0)", "red"]
        for color in colors:
            serialized = NegativeColor.serialize(color)
            deserialized = NegativeColor.deserialize(serialized)
            assert deserialized == color

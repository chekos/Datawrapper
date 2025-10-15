"""Unit tests for ReplaceFlags serializer utility."""

import pytest

from datawrapper.charts.serializers import ReplaceFlags


class TestReplaceFlagsSerialize:
    """Test ReplaceFlags.serialize() method."""

    def test_serialize_off(self):
        """Test serializing 'off' flag type."""
        result = ReplaceFlags.serialize("off")
        assert result == {"enabled": False, "type": ""}

    def test_serialize_4x3(self):
        """Test serializing '4x3' flag type."""
        result = ReplaceFlags.serialize("4x3")
        assert result == {"enabled": True, "type": "4x3"}

    def test_serialize_1x1(self):
        """Test serializing '1x1' flag type."""
        result = ReplaceFlags.serialize("1x1")
        assert result == {"enabled": True, "type": "1x1"}

    def test_serialize_circle(self):
        """Test serializing 'circle' flag type."""
        result = ReplaceFlags.serialize("circle")
        assert result == {"enabled": True, "type": "circle"}


class TestReplaceFlagsDeserialize:
    """Test ReplaceFlags.deserialize() method."""

    def test_deserialize_disabled(self):
        """Test deserializing disabled flags."""
        result = ReplaceFlags.deserialize({"enabled": False, "type": ""})
        assert result == "off"

    def test_deserialize_disabled_with_type(self):
        """Test deserializing disabled flags with a type value."""
        # When disabled, the type should be ignored
        result = ReplaceFlags.deserialize({"enabled": False, "type": "4x3"})
        assert result == "off"

    def test_deserialize_4x3(self):
        """Test deserializing '4x3' flag type."""
        result = ReplaceFlags.deserialize({"enabled": True, "type": "4x3"})
        assert result == "4x3"

    def test_deserialize_1x1(self):
        """Test deserializing '1x1' flag type."""
        result = ReplaceFlags.deserialize({"enabled": True, "type": "1x1"})
        assert result == "1x1"

    def test_deserialize_circle(self):
        """Test deserializing 'circle' flag type."""
        result = ReplaceFlags.deserialize({"enabled": True, "type": "circle"})
        assert result == "circle"

    def test_deserialize_enabled_empty_type(self):
        """Test deserializing enabled flags with empty type."""
        result = ReplaceFlags.deserialize({"enabled": True, "type": ""})
        assert result == ""

    def test_deserialize_none(self):
        """Test deserializing None returns 'off'."""
        result = ReplaceFlags.deserialize(None)
        assert result == "off"

    def test_deserialize_empty_dict(self):
        """Test deserializing empty dict returns 'off'."""
        result = ReplaceFlags.deserialize({})
        assert result == "off"

    def test_deserialize_missing_enabled(self):
        """Test deserializing dict without 'enabled' key."""
        result = ReplaceFlags.deserialize({"type": "4x3"})
        assert result == "off"

    def test_deserialize_missing_type(self):
        """Test deserializing dict without 'type' key."""
        result = ReplaceFlags.deserialize({"enabled": True})
        assert result == ""

    def test_deserialize_non_dict(self):
        """Test deserializing non-dict values returns 'off'."""
        assert ReplaceFlags.deserialize("invalid") == "off"
        assert ReplaceFlags.deserialize(123) == "off"
        assert ReplaceFlags.deserialize([]) == "off"


class TestReplaceFlagsRoundTrip:
    """Test round-trip serialization/deserialization."""

    @pytest.mark.parametrize(
        "flag_type",
        ["off", "4x3", "1x1", "circle"],
    )
    def test_roundtrip(self, flag_type):
        """Test that serialize -> deserialize returns original value."""
        serialized = ReplaceFlags.serialize(flag_type)
        deserialized = ReplaceFlags.deserialize(serialized)
        assert deserialized == flag_type

    def test_roundtrip_preserves_structure(self):
        """Test that serialized structure matches API expectations."""
        # Serialize from Python format
        serialized = ReplaceFlags.serialize("4x3")

        # Verify structure
        assert isinstance(serialized, dict)
        assert "enabled" in serialized
        assert "type" in serialized
        assert serialized["enabled"] is True
        assert serialized["type"] == "4x3"

        # Deserialize back to Python format
        deserialized = ReplaceFlags.deserialize(serialized)
        assert deserialized == "4x3"

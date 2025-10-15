"""Tests for the CustomRange utility class."""

from datawrapper.charts.serializers import CustomRange


class TestCustomRangeSerialize:
    """Test CustomRange.serialize() method."""

    def test_serialize_tuple_with_values(self):
        """Test serializing a tuple with actual values."""
        result = CustomRange.serialize((0, 100))
        assert result == [0, 100]

    def test_serialize_list_with_values(self):
        """Test serializing a list with actual values."""
        result = CustomRange.serialize([10, 50])
        assert result == [10, 50]

    def test_serialize_tuple_with_empty_strings(self):
        """Test serializing a tuple with empty strings."""
        result = CustomRange.serialize(("", ""))
        assert result == ["", ""]

    def test_serialize_list_with_empty_strings(self):
        """Test serializing a list with empty strings."""
        result = CustomRange.serialize(["", ""])
        assert result == ["", ""]

    def test_serialize_mixed_values(self):
        """Test serializing with one empty string and one value."""
        result = CustomRange.serialize(("", 100))
        assert result == ["", 100]

    def test_serialize_float_values(self):
        """Test serializing with float values."""
        result = CustomRange.serialize((0.5, 99.9))
        assert result == [0.5, 99.9]

    def test_serialize_negative_values(self):
        """Test serializing with negative values."""
        result = CustomRange.serialize((-50, 50))
        assert result == [-50, 50]

    def test_serialize_string_values(self):
        """Test serializing with string values (like dates)."""
        result = CustomRange.serialize(("2020-01-01", "2023-12-31"))
        assert result == ["2020-01-01", "2023-12-31"]


class TestCustomRangeDeserialize:
    """Test CustomRange.deserialize() method."""

    def test_deserialize_list_with_values(self):
        """Test deserializing a list with numeric values."""
        result = CustomRange.deserialize([0, 100])
        assert result == [0, 100]

    def test_deserialize_list_with_empty_strings(self):
        """Test deserializing a list with empty strings."""
        result = CustomRange.deserialize(["", ""])
        assert result == ["", ""]

    def test_deserialize_mixed_values(self):
        """Test deserializing a list with mixed values."""
        result = CustomRange.deserialize([0, ""])
        assert result == [0, ""]

    def test_deserialize_float_values(self):
        """Test deserializing a list with float values."""
        result = CustomRange.deserialize([0.5, 99.9])
        assert result == [0.5, 99.9]

    def test_deserialize_negative_values(self):
        """Test deserializing a list with negative values."""
        result = CustomRange.deserialize([-100, 100])
        assert result == [-100, 100]

    def test_deserialize_string_values(self):
        """Test deserializing a list with string values that should stay as strings."""
        result = CustomRange.deserialize(["2020-01-01", "2020-12-31"])
        assert result == ["2020-01-01", "2020-12-31"]

    def test_deserialize_none(self):
        """Test deserializing None returns default empty strings."""
        result = CustomRange.deserialize(None)
        assert result == ["", ""]

    def test_deserialize_empty_list(self):
        """Test deserializing an empty list returns default empty strings."""
        result = CustomRange.deserialize([])
        assert result == ["", ""]

    def test_deserialize_single_value_list(self):
        """Test deserializing a list with only one value pads with empty string."""
        result = CustomRange.deserialize([100])
        assert result == [100, ""]

    def test_deserialize_more_than_two_values(self):
        """Test deserializing a list with more than two values returns only first two."""
        result = CustomRange.deserialize([0, 50, 100])
        assert result == [0, 50]


class TestCustomRangeRoundTrip:
    """Test round-trip serialization/deserialization."""

    def test_roundtrip_with_values(self):
        """Test that serialize -> deserialize preserves values."""
        original = [0, 100]
        serialized = CustomRange.serialize(original)
        deserialized = CustomRange.deserialize(serialized)
        assert deserialized == original

    def test_roundtrip_with_empty_strings(self):
        """Test that serialize -> deserialize preserves empty strings."""
        original = ["", ""]
        serialized = CustomRange.serialize(original)
        deserialized = CustomRange.deserialize(serialized)
        assert deserialized == original

    def test_roundtrip_with_mixed_values(self):
        """Test that serialize -> deserialize preserves mixed values."""
        original = ["", 100]
        serialized = CustomRange.serialize(original)
        deserialized = CustomRange.deserialize(serialized)
        assert deserialized == original

    def test_roundtrip_with_dates(self):
        """Test that serialize -> deserialize preserves date strings."""
        original = ["2020-01-01", "2023-12-31"]
        serialized = CustomRange.serialize(original)
        deserialized = CustomRange.deserialize(serialized)
        assert deserialized == original

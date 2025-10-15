"""Unit tests for the CustomTicks serialization/deserialization helper."""

from datawrapper.charts.serializers import CustomTicks


class TestCustomTicksSerialization:
    """Test CustomTicks.serialize method."""

    def test_serialize_empty_list(self):
        """Test serializing an empty list."""
        result = CustomTicks.serialize([])
        assert result == ""

    def test_serialize_single_integer(self):
        """Test serializing a single integer."""
        result = CustomTicks.serialize([5])
        assert result == "5"

    def test_serialize_single_float(self):
        """Test serializing a single float."""
        result = CustomTicks.serialize([3.14])
        assert result == "3.14"

    def test_serialize_single_string(self):
        """Test serializing a single string."""
        result = CustomTicks.serialize(["2020"])
        assert result == "2020"

    def test_serialize_multiple_integers(self):
        """Test serializing multiple integers."""
        result = CustomTicks.serialize([0, 10, 20, 30])
        assert result == "0,10,20,30"

    def test_serialize_multiple_floats(self):
        """Test serializing multiple floats."""
        result = CustomTicks.serialize([0.0, 2.5, 5.0, 7.5])
        assert result == "0.0,2.5,5.0,7.5"

    def test_serialize_multiple_strings(self):
        """Test serializing multiple strings."""
        result = CustomTicks.serialize(["2020", "2021", "2022"])
        assert result == "2020,2021,2022"

    def test_serialize_mixed_types(self):
        """Test serializing mixed types."""
        result = CustomTicks.serialize([0, 2.5, "2020", 10])
        assert result == "0,2.5,2020,10"

    def test_serialize_negative_numbers(self):
        """Test serializing negative numbers."""
        result = CustomTicks.serialize([-10, -5, 0, 5, 10])
        assert result == "-10,-5,0,5,10"


class TestCustomTicksDeserialization:
    """Test CustomTicks.deserialize method."""

    def test_deserialize_empty_string(self):
        """Test deserializing an empty string."""
        result = CustomTicks.deserialize("")
        assert result == []

    def test_deserialize_single_integer(self):
        """Test deserializing a single integer."""
        result = CustomTicks.deserialize("5")
        assert result == [5]

    def test_deserialize_single_float(self):
        """Test deserializing a single float."""
        result = CustomTicks.deserialize("3.14")
        assert result == [3.14]

    def test_deserialize_single_string(self):
        """Test deserializing a single string that's not a number."""
        result = CustomTicks.deserialize("Jan")
        assert result == ["Jan"]

    def test_deserialize_multiple_integers(self):
        """Test deserializing multiple integers."""
        result = CustomTicks.deserialize("0,10,20,30")
        assert result == [0, 10, 20, 30]

    def test_deserialize_multiple_floats(self):
        """Test deserializing multiple floats."""
        result = CustomTicks.deserialize("0.0,2.5,5.0,7.5")
        assert result == [0.0, 2.5, 5.0, 7.5]

    def test_deserialize_multiple_strings(self):
        """Test deserializing multiple strings."""
        result = CustomTicks.deserialize("Jan,Feb,Mar")
        assert result == ["Jan", "Feb", "Mar"]

    def test_deserialize_mixed_types(self):
        """Test deserializing mixed types."""
        result = CustomTicks.deserialize("0,2.5,Jan,10")
        assert result == [0, 2.5, "Jan", 10]

    def test_deserialize_negative_numbers(self):
        """Test deserializing negative numbers."""
        result = CustomTicks.deserialize("-10,-5,0,5,10")
        assert result == [-10, -5, 0, 5, 10]

    def test_deserialize_with_whitespace(self):
        """Test deserializing with extra whitespace."""
        result = CustomTicks.deserialize(" 0 , 10 , 20 , 30 ")
        assert result == [0, 10, 20, 30]

    def test_deserialize_date_strings(self):
        """Test deserializing date-like strings."""
        result = CustomTicks.deserialize("2020,2021,2022")
        assert result == [2020, 2021, 2022]

    def test_deserialize_date_format_strings(self):
        """Test deserializing date format strings."""
        result = CustomTicks.deserialize("2020-01,2020-02,2020-03")
        assert result == ["2020-01", "2020-02", "2020-03"]


class TestCustomTicksRoundTrip:
    """Test round-trip serialization and deserialization."""

    def test_roundtrip_integers(self):
        """Test round-trip with integers."""
        original = [0, 10, 20, 30]
        serialized = CustomTicks.serialize(original)
        deserialized = CustomTicks.deserialize(serialized)
        assert deserialized == original

    def test_roundtrip_floats(self):
        """Test round-trip with floats."""
        original = [0.0, 2.5, 5.0, 7.5]
        serialized = CustomTicks.serialize(original)
        deserialized = CustomTicks.deserialize(serialized)
        assert deserialized == original

    def test_roundtrip_strings(self):
        """Test round-trip with strings."""
        original = ["Jan", "Feb", "Mar"]
        serialized = CustomTicks.serialize(original)
        deserialized = CustomTicks.deserialize(serialized)
        assert deserialized == original

    def test_roundtrip_mixed(self):
        """Test round-trip with mixed types."""
        original = [0, 2.5, "Jan", 10]
        serialized = CustomTicks.serialize(original)
        deserialized = CustomTicks.deserialize(serialized)
        assert deserialized == original

    def test_roundtrip_empty(self):
        """Test round-trip with empty list."""
        original = []
        serialized = CustomTicks.serialize(original)
        deserialized = CustomTicks.deserialize(serialized)
        assert deserialized == original

    def test_roundtrip_negative_numbers(self):
        """Test round-trip with negative numbers."""
        original = [-10, -5, 0, 5, 10]
        serialized = CustomTicks.serialize(original)
        deserialized = CustomTicks.deserialize(serialized)
        assert deserialized == original

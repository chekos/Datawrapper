"""Tests for NumberDivisor enum and ColumnFormat number_divisor field."""

import pytest
from pydantic import ValidationError

from datawrapper.charts import ColumnFormat, NumberDivisor


class TestNumberDivisorEnum:
    """Test the NumberDivisor enum values."""

    def test_enum_values(self):
        """Test that enum has all expected values."""
        assert NumberDivisor.NO_CHANGE.value == "0"
        assert NumberDivisor.AUTO_DETECT.value == "auto"
        assert NumberDivisor.DIVIDE_BY_THOUSAND.value == "3"
        assert NumberDivisor.DIVIDE_BY_MILLION.value == "6"
        assert NumberDivisor.DIVIDE_BY_BILLION.value == "9"
        assert NumberDivisor.MULTIPLY_BY_HUNDRED.value == "-2"
        assert NumberDivisor.MULTIPLY_BY_THOUSAND.value == "-3"
        assert NumberDivisor.MULTIPLY_BY_MILLION.value == "-6"
        assert NumberDivisor.MULTIPLY_BY_BILLION.value == "-9"
        assert NumberDivisor.MULTIPLY_BY_TRILLION.value == "-12"

    def test_enum_string_representation(self):
        """Test that enum values are strings."""
        assert isinstance(NumberDivisor.DIVIDE_BY_MILLION.value, str)
        assert isinstance(NumberDivisor.AUTO_DETECT.value, str)


class TestColumnFormatNumberDivisor:
    """Test ColumnFormat with number_divisor field."""

    def test_default_value(self):
        """Test that default value is 0."""
        col_format = ColumnFormat(column="sales")
        assert col_format.number_divisor == 0

    def test_enum_value(self):
        """Test setting number_divisor with enum value."""
        col_format = ColumnFormat(
            column="sales", number_divisor=NumberDivisor.DIVIDE_BY_MILLION
        )
        assert col_format.number_divisor == NumberDivisor.DIVIDE_BY_MILLION

    def test_raw_int_value(self):
        """Test setting number_divisor with raw integer."""
        col_format = ColumnFormat(column="sales", number_divisor=6)
        assert col_format.number_divisor == 6

    def test_raw_string_value(self):
        """Test setting number_divisor with raw string."""
        col_format = ColumnFormat(column="sales", number_divisor="auto")
        assert col_format.number_divisor == "auto"

    def test_string_number_value(self):
        """Test setting number_divisor with string representation of number."""
        col_format = ColumnFormat(column="sales", number_divisor="6")
        assert col_format.number_divisor == "6"

    def test_negative_int_value(self):
        """Test setting number_divisor with negative integer."""
        col_format = ColumnFormat(column="sales", number_divisor=-6)
        assert col_format.number_divisor == -6

    def test_negative_string_value(self):
        """Test setting number_divisor with negative string."""
        col_format = ColumnFormat(column="sales", number_divisor="-6")
        assert col_format.number_divisor == "-6"

    def test_invalid_value_raises_error(self):
        """Test that invalid values raise ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            ColumnFormat(column="sales", number_divisor=999)
        assert "Invalid number_divisor" in str(exc_info.value)

    def test_invalid_string_raises_error(self):
        """Test that invalid string values raise ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            ColumnFormat(column="sales", number_divisor="invalid")
        assert "Invalid number_divisor" in str(exc_info.value)

    def test_all_valid_int_values(self):
        """Test all valid integer values."""
        valid_ints = [0, 3, 6, 9, -2, -3, -6, -9, -12]
        for value in valid_ints:
            col_format = ColumnFormat(column="sales", number_divisor=value)
            assert col_format.number_divisor == value

    def test_all_valid_string_values(self):
        """Test all valid string values."""
        valid_strings = ["0", "auto", "3", "6", "9", "-2", "-3", "-6", "-9", "-12"]
        for value in valid_strings:
            col_format = ColumnFormat(column="sales", number_divisor=value)
            assert col_format.number_divisor == value

    def test_all_enum_values(self):
        """Test all enum values."""
        for divisor in NumberDivisor:
            col_format = ColumnFormat(column="sales", number_divisor=divisor)
            assert col_format.number_divisor == divisor


class TestColumnFormatSerialization:
    """Test ColumnFormat serialization with number_divisor."""

    def test_serialize_default_value_included(self):
        """Test that default value (0) is included in model_dump."""
        col_format = ColumnFormat(column="sales", number_divisor=0)
        serialized = col_format.model_dump(by_alias=True, exclude={"column"})
        # model_dump includes all fields, filtering happens in ColumnFormatList
        assert serialized["number-divisor"] == 0

    def test_serialize_enum_value(self):
        """Test serializing enum value."""
        col_format = ColumnFormat(
            column="sales", number_divisor=NumberDivisor.DIVIDE_BY_MILLION
        )
        serialized = col_format.model_dump(by_alias=True, exclude={"column"})
        # Enum should be serialized as its value
        assert serialized["number-divisor"] == NumberDivisor.DIVIDE_BY_MILLION

    def test_serialize_raw_int_value(self):
        """Test serializing raw integer value."""
        col_format = ColumnFormat(column="sales", number_divisor=6)
        serialized = col_format.model_dump(by_alias=True, exclude={"column"})
        assert serialized["number-divisor"] == 6

    def test_serialize_auto_value(self):
        """Test serializing 'auto' value."""
        col_format = ColumnFormat(column="sales", number_divisor="auto")
        serialized = col_format.model_dump(by_alias=True, exclude={"column"})
        assert serialized["number-divisor"] == "auto"

    def test_serialize_negative_value(self):
        """Test serializing negative value."""
        col_format = ColumnFormat(column="sales", number_divisor=-6)
        serialized = col_format.model_dump(by_alias=True, exclude={"column"})
        assert serialized["number-divisor"] == -6

    def test_deserialize_from_api(self):
        """Test deserializing from API format."""
        api_data = {
            "column": "sales",
            "type": "number",
            "number-divisor": 6,
        }
        col_format = ColumnFormat.model_validate(api_data)
        assert col_format.number_divisor == 6

    def test_deserialize_auto_from_api(self):
        """Test deserializing 'auto' from API format."""
        api_data = {
            "column": "sales",
            "type": "number",
            "number-divisor": "auto",
        }
        col_format = ColumnFormat.model_validate(api_data)
        assert col_format.number_divisor == "auto"

    def test_combined_with_other_fields(self):
        """Test number_divisor works with other formatting fields."""
        col_format = ColumnFormat(
            column="sales",
            type="number",
            number_divisor=NumberDivisor.DIVIDE_BY_MILLION,
            number_prepend="$",
            number_append="M",
        )
        assert col_format.number_divisor == NumberDivisor.DIVIDE_BY_MILLION
        assert col_format.number_prepend == "$"
        assert col_format.number_append == "M"

        serialized = col_format.model_dump(by_alias=True, exclude={"column"})
        assert serialized["number-divisor"] == NumberDivisor.DIVIDE_BY_MILLION
        assert serialized["number-prepend"] == "$"
        assert serialized["number-append"] == "M"

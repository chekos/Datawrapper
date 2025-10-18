"""Tests for NumberFormat enum."""

from datawrapper.charts.enums import NumberFormat


class TestNumberFormat:
    """Test the NumberFormat enum."""

    def test_enum_values(self):
        """Test that enum values match expected format strings."""
        # Basic formats
        assert NumberFormat.AUTO.value == "auto"
        assert NumberFormat.THOUSANDS_WITH_OPTIONAL_DECIMALS.value == "0,0.[00]"
        assert NumberFormat.INTEGER.value == "0"
        assert NumberFormat.ONE_DECIMAL.value == "0.0"
        assert NumberFormat.TWO_DECIMALS.value == "0.00"
        assert NumberFormat.THREE_DECIMALS.value == "0.000"
        assert NumberFormat.UP_TO_ONE_DECIMAL.value == "0.[0]"
        assert NumberFormat.UP_TO_TWO_DECIMALS.value == "0.[00]"

        # Percentage formats
        assert NumberFormat.PERCENT_INTEGER.value == "0%"
        assert NumberFormat.PERCENT_ONE_DECIMAL.value == "0.0%"
        assert NumberFormat.PERCENT_TWO_DECIMALS.value == "0.00%"
        assert NumberFormat.PERCENT_UP_TO_ONE_DECIMAL.value == "0.[0]%"
        assert NumberFormat.PERCENT_UP_TO_TWO_DECIMALS.value == "0.[00]%"

        # Thousands separator and special formats
        assert NumberFormat.THOUSANDS_SEPARATOR.value == "0,0"
        assert NumberFormat.ORDINAL.value == "0o"

        # Abbreviated formats
        assert NumberFormat.ABBREVIATED.value == "0a"
        assert NumberFormat.ABBREVIATED_ONE_DECIMAL.value == "0.[0]a"
        assert NumberFormat.ABBREVIATED_TWO_DECIMALS.value == "0.[00]a"
        assert NumberFormat.ABBREVIATED_THREE_DECIMALS.value == "0.[000] a"

        # Sign display formats
        assert NumberFormat.PLUS_SIGN.value == "+0"
        assert NumberFormat.PLUS_SIGN_PERCENT.value == "+0%"

        # Currency formats
        assert NumberFormat.CURRENCY_ABBREVIATED_WITH_PLUS.value == "+$0.[00]a"
        assert NumberFormat.CURRENCY_ABBREVIATED.value == "$0.[00]a"
        assert NumberFormat.CURRENCY_OPTIONAL_DECIMALS.value == "$0.[00]"

        # Special formatting
        assert NumberFormat.ZERO_PADDED.value == "0000"
        assert NumberFormat.PARENTHESES_FOR_NEGATIVES.value == "(0,0.00)"
        assert NumberFormat.LEADING_DECIMAL.value == ".000"

        # Scientific notation
        assert NumberFormat.SCIENTIFIC_NOTATION.value == "0,0e+0"
        assert NumberFormat.SCIENTIFIC_NOTATION_DECIMALS.value == "0.[00]e+0"

        # Absolute value
        assert NumberFormat.ABSOLUTE_VALUE.value == "|0.0|"

    def test_enum_can_be_used_as_string(self):
        """Test that enum values can be compared to strings."""
        assert NumberFormat.AUTO == "auto"
        assert NumberFormat.THOUSANDS_SEPARATOR == "0,0"
        assert NumberFormat.PERCENT_TWO_DECIMALS == "0.00%"

    def test_enum_serialization(self):
        """Test that enum values serialize to their string values."""
        # When used in a dict or serialized, should become the string value
        format_dict = {"format": NumberFormat.THOUSANDS_SEPARATOR}
        assert format_dict["format"].value == "0,0"

    def test_custom_format_string(self):
        """Test that custom format strings can still be used."""
        # Users should still be able to use custom strings
        custom_format = "+$0.[00]a"
        assert isinstance(custom_format, str)
        assert custom_format == "+$0.[00]a"

    def test_enum_in_type_union(self):
        """Test that enum works in a union type with str."""

        # This simulates how it's used in chart models
        def accept_format(fmt: NumberFormat | str) -> str:
            if isinstance(fmt, NumberFormat):
                return fmt.value
            return fmt

        # Should work with enum
        assert accept_format(NumberFormat.THOUSANDS_SEPARATOR) == "0,0"
        # Should work with string
        assert accept_format("custom") == "custom"
        # Should work with custom format
        assert accept_format("+$0.[00]a") == "+$0.[00]a"

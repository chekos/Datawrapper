"""Tests for the DateFormat enum."""

from datawrapper.charts import ColumnFormat, DateFormat


class TestDateFormatEnum:
    """Test the DateFormat enum values and usage."""

    def test_enum_values(self):
        """Test that all enum values have correct string representations."""
        # Basic/Auto
        assert DateFormat.AUTO.value == "auto"

        # Year formats
        assert DateFormat.YEAR_FULL.value == "YYYY"
        assert DateFormat.YEAR_TWO_DIGIT.value == "YY"
        assert DateFormat.YEAR_ABBREVIATED.value == "'YY"
        assert DateFormat.YEAR_ABBREVIATED_FIRST.value == "YYYY~~'YY"

        # Quarter formats
        assert DateFormat.QUARTER.value == "Q"
        assert DateFormat.YEAR_QUARTER.value == "YYYY [Q]Q"
        assert DateFormat.YEAR_QUARTER_MULTILINE.value == "YYYY|[Q]Q"

        # Month formats
        assert DateFormat.MONTH_FULL.value == "MMMM"
        assert DateFormat.MONTH_ABBREVIATED.value == "MMM"
        assert DateFormat.MONTH_NUMBER_PADDED.value == "MM"
        assert DateFormat.MONTH_NUMBER.value == "M"
        assert DateFormat.MONTH_ABBREVIATED_WITH_YEAR.value == "MMM 'YY"
        assert DateFormat.YEAR_MONTH_MULTILINE.value == "YYYY|MMM"

        # Week formats
        assert DateFormat.WEEK_OF_YEAR_PADDED.value == "ww"
        assert DateFormat.WEEK_OF_YEAR.value == "w"
        assert DateFormat.WEEK_OF_YEAR_ORDINAL.value == "wo"

        # Day of month formats
        assert DateFormat.DAY_PADDED.value == "DD"
        assert DateFormat.DAY.value == "D"
        assert DateFormat.DAY_ORDINAL.value == "Do"
        assert DateFormat.MONTH_DAY_MULTILINE.value == "MMM|DD"
        assert DateFormat.MONTH_DAY_YEAR_FULL.value == "MMMM D, YYYY"

        # Day of week formats
        assert DateFormat.DAY_OF_WEEK_FULL.value == "dddd"
        assert DateFormat.DAY_OF_WEEK_SHORT.value == "ddd"
        assert DateFormat.DAY_OF_WEEK_MIN.value == "dd"
        assert DateFormat.DAY_OF_WEEK_NUMBER.value == "d"

        # Sport season formats
        assert DateFormat.SPORT_SEASON_FULL.value == "BB"
        assert DateFormat.SPORT_SEASON_ABBREVIATED.value == "B"

        # Time formats
        assert DateFormat.HOUR_24_PADDED.value == "HH"
        assert DateFormat.HOUR_24.value == "H"
        assert DateFormat.HOUR_12_PADDED.value == "hh"
        assert DateFormat.HOUR_12.value == "h"
        assert DateFormat.HOUR_24_ALT_PADDED.value == "kk"
        assert DateFormat.HOUR_24_ALT.value == "k"
        assert DateFormat.MINUTE_PADDED.value == "mm"
        assert DateFormat.MINUTE.value == "m"
        assert DateFormat.SECOND_PADDED.value == "ss"
        assert DateFormat.SECOND.value == "s"
        assert DateFormat.MILLISECOND.value == "SSS"
        assert DateFormat.AM_PM_UPPER.value == "A"
        assert DateFormat.AM_PM_LOWER.value == "a"

        # Timezone formats
        assert DateFormat.TIMEZONE_OFFSET.value == "Z"
        assert DateFormat.TIMEZONE_OFFSET_NO_COLON.value == "ZZ"

        # Unix timestamp formats
        assert DateFormat.UNIX_TIMESTAMP_SECONDS.value == "X"
        assert DateFormat.UNIX_TIMESTAMP_MILLISECONDS.value == "x"

        # Localized formats
        assert DateFormat.LOCALE_DATE_SHORT.value == "L"
        assert DateFormat.LOCALE_DATE_LONG.value == "LL"
        assert DateFormat.LOCALE_DATETIME_SHORT.value == "LLL"
        assert DateFormat.LOCALE_DATETIME_LONG.value == "LLLL"
        assert DateFormat.LOCALE_TIME.value == "LT"

    def test_enum_in_column_format(self):
        """Test using DateFormat enum in ColumnFormat."""
        # Using enum value
        col_format = ColumnFormat(
            column="date_column", type="date", number_format=DateFormat.YEAR_FULL
        )
        assert col_format.number_format == "YYYY"

        # Using string directly (backwards compatibility)
        col_format = ColumnFormat(
            column="date_column", type="date", number_format="YYYY-MM-DD"
        )
        assert col_format.number_format == "YYYY-MM-DD"

    def test_enum_serialization(self):
        """Test that DateFormat enum serializes correctly."""
        col_format = ColumnFormat(
            column="date_column",
            type="date",
            number_format=DateFormat.MONTH_ABBREVIATED_WITH_YEAR,
        )

        # Serialize to dict
        data = col_format.model_dump(by_alias=True)
        assert data["number-format"] == "MMM 'YY"

    def test_backwards_compatibility_with_strings(self):
        """Test that raw format strings still work."""
        # Custom format string
        col_format = ColumnFormat(
            column="date_column", type="date", number_format="DD.MM.YYYY"
        )
        assert col_format.number_format == "DD.MM.YYYY"

        # Standard format as string
        col_format = ColumnFormat(
            column="date_column", type="date", number_format="YYYY-MM-DD"
        )
        assert col_format.number_format == "YYYY-MM-DD"

    def test_enum_comparison(self):
        """Test that enum values can be compared."""
        assert DateFormat.YEAR_FULL == DateFormat.YEAR_FULL
        assert DateFormat.YEAR_FULL != DateFormat.MONTH_ABBREVIATED
        assert DateFormat.YEAR_FULL.value == "YYYY"

    def test_enum_in_type_hints(self):
        """Test that DateFormat works in type hints with union types."""
        from typing import get_args

        # This is how it's used in chart classes
        format_type = DateFormat | str

        # Verify the union includes both types
        args = get_args(format_type)
        assert DateFormat in args
        assert str in args

    def test_all_enum_members_accessible(self):
        """Test that all enum members are accessible."""
        # Test a few key members from each category
        assert hasattr(DateFormat, "YEAR_FULL")
        assert hasattr(DateFormat, "MONTH_ABBREVIATED")
        assert hasattr(DateFormat, "YEAR_QUARTER")
        assert hasattr(DateFormat, "LOCALE_DATE_LONG")
        assert hasattr(DateFormat, "DAY_OF_WEEK_FULL")
        assert hasattr(DateFormat, "HOUR_24_PADDED")
        assert hasattr(DateFormat, "TIMEZONE_OFFSET")

        # Test that we can iterate over all members
        all_formats = list(DateFormat)
        assert len(all_formats) == 50  # We now have 50 date/time formats

    def test_enum_docstring(self):
        """Test that the enum has proper documentation."""
        assert DateFormat.__doc__ is not None
        assert "date" in DateFormat.__doc__.lower()
        assert "format" in DateFormat.__doc__.lower()

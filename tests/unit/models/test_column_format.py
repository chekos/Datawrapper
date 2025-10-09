"""Unit tests for ColumnFormat model."""

import pytest
from pydantic import ValidationError

import datawrapper
from tests.utils import _test_class


class TestColumnFormat:
    """Test ColumnFormat model validation and serialization."""

    def test_column_format_basic_validation(self):
        """Test basic ColumnFormat validation."""
        _test_class(datawrapper.ColumnFormat)

    def test_column_format_defaults(self):
        """Test ColumnFormat default values."""
        col_format = datawrapper.ColumnFormat(column="sales")

        # Check defaults
        assert col_format.column == "sales"
        assert col_format.type == "auto"
        assert col_format.ignore is False
        assert col_format.number_prepend == ""
        assert col_format.number_append == ""

    def test_column_format_with_valid_data(self):
        """Test ColumnFormat with valid data."""
        col_format = datawrapper.ColumnFormat(
            column="revenue",
            type="number",
            ignore=True,
            **{"number-prepend": "$"},  # Use alias
            **{"number-append": "M"},  # Use alias
        )

        assert col_format.column == "revenue"
        assert col_format.type == "number"
        assert col_format.ignore is True
        assert col_format.number_prepend == "$"
        assert col_format.number_append == "M"

    def test_column_format_all_types(self):
        """Test ColumnFormat with all valid types."""
        valid_types = ["auto", "text", "number", "date"]

        for col_type in valid_types:
            col_format = datawrapper.ColumnFormat(column="test", type=col_type)
            assert col_format.type == col_type

    def test_column_format_invalid_type(self):
        """Test ColumnFormat with invalid type."""
        with pytest.raises(ValidationError) as exc_info:
            datawrapper.ColumnFormat(column="sales", type="invalid")

        assert "type" in str(exc_info.value)

    def test_column_format_empty_column_string(self):
        """Test ColumnFormat with empty column string."""
        with pytest.raises(ValidationError):
            datawrapper.ColumnFormat(column="")

    def test_column_format_required_column(self):
        """Test ColumnFormat requires column."""
        with pytest.raises(ValidationError):
            datawrapper.ColumnFormat()

    def test_column_format_serialization(self):
        """Test ColumnFormat serialization."""
        col_format = datawrapper.ColumnFormat(
            column="sales",
            type="number",
            ignore=False,
            **{"number-prepend": "$"},
            **{"number-append": "K"},
        )

        # Test model_dump
        data = col_format.model_dump(by_alias=True)
        assert isinstance(data, dict)

        # Test JSON serialization
        json_str = col_format.model_dump_json(by_alias=True)
        assert isinstance(json_str, str)

        # Test round-trip
        reconstructed = datawrapper.ColumnFormat.model_validate_json(json_str)
        assert reconstructed == col_format

    def test_column_format_field_aliases(self):
        """Test ColumnFormat field aliases work correctly."""
        # Create with alias field names
        col_format = datawrapper.ColumnFormat(
            column="sales", **{"number-prepend": "$"}, **{"number-append": "M"}
        )

        # Serialize with aliases
        data = col_format.model_dump(by_alias=True)

        # Should contain API field names (aliases)
        assert "number-prepend" in data
        assert "number-append" in data
        assert data["number-prepend"] == "$"
        assert data["number-append"] == "M"

    def test_column_format_validation_edge_cases(self):
        """Test ColumnFormat validation edge cases."""
        # Test with whitespace-only strings for column (allowed by min_length=1)
        col_format = datawrapper.ColumnFormat(column="   ")
        assert col_format.column == "   "

        # Test with numeric values for column (should fail)
        with pytest.raises(ValidationError):
            datawrapper.ColumnFormat(column=123)

        # Test with boolean values for column (should fail)
        with pytest.raises(ValidationError):
            datawrapper.ColumnFormat(column=True)

    def test_column_format_boolean_ignore(self):
        """Test ColumnFormat ignore field validation."""
        # Valid boolean values should work
        col_format = datawrapper.ColumnFormat(column="sales", ignore=True)
        assert col_format.ignore is True

        col_format = datawrapper.ColumnFormat(column="sales", ignore=False)
        assert col_format.ignore is False

        # String values should fail
        with pytest.raises(ValidationError):
            datawrapper.ColumnFormat(column="sales", ignore="true")

    def test_column_format_prepend_append_strings(self):
        """Test ColumnFormat prepend and append string fields."""
        col_format = datawrapper.ColumnFormat(
            column="sales",
            **{"number-prepend": "USD "},
            **{"number-append": " million"},
        )

        assert col_format.number_prepend == "USD "
        assert col_format.number_append == " million"

        # Empty strings should work
        col_format = datawrapper.ColumnFormat(
            column="sales", **{"number-prepend": ""}, **{"number-append": ""}
        )

        assert col_format.number_prepend == ""
        assert col_format.number_append == ""

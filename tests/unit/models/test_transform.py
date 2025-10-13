"""Unit tests for Transform model."""

import pytest
from pydantic import ValidationError

import datawrapper
from tests.utils import _test_class


class TestTransform:
    """Test Transform model validation and serialization."""

    def test_transform_basic_validation(self):
        """Test basic Transform validation."""
        _test_class(datawrapper.Transform)

    def test_transform_defaults(self):
        """Test Transform default values."""
        transform = datawrapper.Transform()

        # Check defaults
        assert transform.transpose is False
        assert transform.vertical_header is True
        assert transform.horizontal_header is True
        assert transform.column_order == []
        assert len(transform.column_format) == 0
        assert transform.external_data == ""
        assert transform.use_datawrapper_cdn is True
        assert transform.upload_method == "copy"

    def test_transform_with_valid_data(self):
        """Test Transform with valid data."""
        transform = datawrapper.Transform(
            transpose=True,
            **{"vertical-header": False},  # Use alias
            **{"horizontal-header": False},  # Use alias
            **{"column-order": [2, 1, 0]},  # Use alias
            **{"external-data": "https://example.com/data.csv"},  # Use alias
            **{"use-datawrapper-cdn": False},  # Use alias
            **{"upload-method": "external-data"},  # Use alias
        )

        assert transform.transpose is True
        assert transform.vertical_header is False
        assert transform.horizontal_header is False
        assert transform.column_order == [2, 1, 0]
        assert transform.external_data == "https://example.com/data.csv"
        assert transform.use_datawrapper_cdn is False
        assert transform.upload_method == "external-data"

    def test_transform_upload_methods(self):
        """Test Transform with all valid upload methods."""
        valid_methods = ["copy", "upload", "google-spreadsheet", "external-data"]

        for method in valid_methods:
            transform = datawrapper.Transform(**{"upload-method": method})
            assert transform.upload_method == method

    def test_transform_invalid_upload_method(self):
        """Test Transform with invalid upload method."""
        with pytest.raises(ValidationError) as exc_info:
            datawrapper.Transform(**{"upload-method": "invalid"})

        assert "upload-method" in str(exc_info.value) or "upload_method" in str(
            exc_info.value
        )

    def test_transform_column_format_with_objects(self):
        """Test Transform with ColumnFormat objects."""
        col_format = datawrapper.ColumnFormat(column="sales", type="number")
        transform = datawrapper.Transform(**{"column-format": [col_format]})

        assert len(transform.column_format) == 1
        assert isinstance(transform.column_format[0], datawrapper.ColumnFormat)
        assert transform.column_format[0].column == "sales"

    def test_transform_column_format_with_dicts(self):
        """Test Transform with column format as dictionaries."""
        transform = datawrapper.Transform(
            **{"column-format": [{"column": "sales", "type": "number"}]}
        )

        assert len(transform.column_format) == 1
        assert isinstance(transform.column_format[0], datawrapper.ColumnFormat)
        assert transform.column_format[0].column == "sales"
        assert transform.column_format[0].type == "number"

    def test_transform_mixed_column_format(self):
        """Test Transform with mixed ColumnFormat objects and dicts."""
        col_format_obj = datawrapper.ColumnFormat(column="sales", type="number")
        col_format_dict = {"column": "date", "type": "date"}

        transform = datawrapper.Transform(
            **{"column-format": [col_format_obj, col_format_dict]}
        )

        assert len(transform.column_format) == 2
        assert isinstance(transform.column_format[0], datawrapper.ColumnFormat)
        assert isinstance(transform.column_format[1], datawrapper.ColumnFormat)
        assert transform.column_format[0].column == "sales"
        assert transform.column_format[1].column == "date"

    def test_transform_serialization(self):
        """Test Transform serialization."""
        transform = datawrapper.Transform(
            transpose=True,
            **{"vertical-header": False},
            **{"column-format": [{"column": "sales", "type": "number"}]},
        )

        # Test model_dump
        data = transform.model_dump(by_alias=True)
        assert isinstance(data, dict)

        # Test JSON serialization
        json_str = transform.model_dump_json(by_alias=True)
        assert isinstance(json_str, str)

        # Test round-trip
        reconstructed = datawrapper.Transform.model_validate_json(json_str)
        assert reconstructed.transpose == transform.transpose
        assert reconstructed.vertical_header == transform.vertical_header

    def test_transform_field_aliases(self):
        """Test Transform field aliases work correctly."""
        transform = datawrapper.Transform(
            **{"vertical-header": False},
            **{"horizontal-header": False},
            **{"column-order": [1, 2, 0]},
            **{"column-format": []},
            **{"external-data": "https://example.com"},
            **{"use-datawrapper-cdn": False},
            **{"upload-method": "external-data"},
        )

        # Serialize with aliases
        data = transform.model_dump(by_alias=True)

        # Should contain API field names (aliases)
        assert "vertical-header" in data
        assert "horizontal-header" in data
        assert "column-order" in data
        assert "column-format" in data
        assert "external-data" in data
        assert "use-datawrapper-cdn" in data
        assert "upload-method" in data

    def test_transform_column_order_validation(self):
        """Test Transform column_order validation."""
        # Valid integer lists should work
        transform = datawrapper.Transform(**{"column-order": [0, 1, 2]})
        assert transform.column_order == [0, 1, 2]

        # Empty list should work
        transform = datawrapper.Transform(**{"column-order": []})
        assert transform.column_order == []

        # Non-list values should fail
        with pytest.raises(ValidationError):
            datawrapper.Transform(**{"column-order": "not a list"})

    def test_transform_boolean_fields(self):
        """Test Transform boolean field validation."""
        # Valid boolean values should work
        transform = datawrapper.Transform(
            transpose=True,
            **{"vertical-header": False},
            **{"horizontal-header": True},
            **{"use-datawrapper-cdn": False},
        )

        assert transform.transpose is True
        assert transform.vertical_header is False
        assert transform.horizontal_header is True
        assert transform.use_datawrapper_cdn is False

        # Invalid type values should fail
        with pytest.raises(ValidationError):
            datawrapper.Transform(transpose=123)  # int instead of bool

    def test_transform_external_data_url(self):
        """Test Transform external_data field."""
        # Valid URL strings should work
        transform = datawrapper.Transform(
            **{"external-data": "https://example.com/data.csv"}
        )
        assert transform.external_data == "https://example.com/data.csv"

        # Empty string should work (default)
        transform = datawrapper.Transform(**{"external-data": ""})
        assert transform.external_data == ""

        # Non-string values should fail
        with pytest.raises(ValidationError):
            datawrapper.Transform(**{"external-data": 123})

    def test_transform_with_dict_column_format(self):
        """Test Transform handles dict column-format from API (auto-converts to list)."""
        # Simulate API response with dict-based column-format
        api_data = {
            "transpose": False,
            "vertical-header": True,
            "horizontal-header": True,
            "column-format": {
                "sales": {"type": "number", "number-prepend": "$"},
                "date": {"type": "date"},
            },
            "external-data": "",
            "use-datawrapper-cdn": True,
            "upload-method": "copy",
        }

        transform = datawrapper.Transform(**api_data)

        # Verify the transform was created successfully
        assert isinstance(transform, datawrapper.Transform)
        assert transform.transpose is False
        assert transform.vertical_header is True

        # Verify column-format was converted from dict to list
        assert len(transform.column_format) == 2
        assert all(
            isinstance(cf, datawrapper.ColumnFormat) for cf in transform.column_format
        )

        # Verify the column names and configs were preserved
        column_names = {cf.column for cf in transform.column_format}
        assert column_names == {"sales", "date"}

        # Find and verify the sales column
        sales_col = next(cf for cf in transform.column_format if cf.column == "sales")
        assert sales_col.type == "number"
        assert sales_col.number_prepend == "$"

        # Find and verify the date column
        date_col = next(cf for cf in transform.column_format if cf.column == "date")
        assert date_col.type == "date"

    def test_transform_with_empty_dict_column_format(self):
        """Test Transform handles empty dict column-format."""
        api_data = {
            "column-format": {},
        }

        transform = datawrapper.Transform(**api_data)

        # Verify empty dict was converted to empty list
        assert len(transform.column_format) == 0

    def test_transform_with_list_column_format(self):
        """Test Transform handles list column-format (no conversion needed)."""
        api_data = {
            "column-format": [
                {"column": "sales", "type": "number"},
                {"column": "date", "type": "date"},
            ],
        }

        transform = datawrapper.Transform(**api_data)

        # Verify list format was preserved
        assert len(transform.column_format) == 2
        assert transform.column_format[0].column == "sales"
        assert transform.column_format[1].column == "date"

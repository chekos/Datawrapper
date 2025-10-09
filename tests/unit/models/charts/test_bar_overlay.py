"""Unit tests for BarOverlay model."""

import pytest
from pydantic import ValidationError

import datawrapper
from tests.utils import _test_class


class TestBarOverlay:
    """Test BarOverlay model validation and serialization."""

    def test_bar_overlay_basic_validation(self):
        """Test basic BarOverlay validation."""
        _test_class(datawrapper.BarOverlay)

    def test_bar_overlay_defaults(self):
        """Test BarOverlay default values."""
        overlay = datawrapper.BarOverlay(to="sales")

        # Check defaults
        assert overlay.type == "value"
        assert overlay.title == ""
        assert overlay.to_column == "sales"
        assert overlay.from_column == "--zero-baseline--"
        assert overlay.color == "#4682b4"
        assert overlay.opacity == 0.6
        assert overlay.pattern == "solid"
        assert overlay.show_in_color_key is True
        assert overlay.label_directly is True

    def test_bar_overlay_with_valid_data(self):
        """Test BarOverlay with valid data."""
        overlay = datawrapper.BarOverlay(
            type="range",
            title="Sales Range",
            to="sales",
            **{"from": "min_sales"},  # 'from' is a Python keyword, use dict unpacking
            color="#ff0000",
            opacity=0.8,
            pattern="diagonal-up",
            showInColorKey=False,
            labelDirectly=False,
        )

        assert overlay.type == "range"
        assert overlay.title == "Sales Range"
        assert overlay.to_column == "sales"
        assert overlay.from_column == "min_sales"
        assert overlay.color == "#ff0000"
        assert overlay.opacity == 0.8
        assert overlay.pattern == "diagonal-up"
        assert overlay.show_in_color_key is False
        assert overlay.label_directly is False

    def test_bar_overlay_invalid_type(self):
        """Test BarOverlay with invalid type."""
        with pytest.raises(ValidationError) as exc_info:
            datawrapper.BarOverlay(to="sales", type="invalid")

        assert "type" in str(exc_info.value)

    def test_bar_overlay_empty_to_column_string(self):
        """Test BarOverlay with empty to_column string."""
        with pytest.raises(ValidationError):
            datawrapper.BarOverlay(to="")

    def test_bar_overlay_required_to_column(self):
        """Test BarOverlay requires to_column."""
        with pytest.raises(ValidationError):
            datawrapper.BarOverlay()

    def test_bar_overlay_serialization(self):
        """Test BarOverlay serialization."""
        overlay = datawrapper.BarOverlay(
            type="range",
            title="Sales Range",
            to="sales",
            **{"from": "min_sales"},
            color="#ff0000",
            opacity=0.8,
        )

        # Test model_dump
        data = overlay.model_dump(by_alias=True)
        assert isinstance(data, dict)

        # Test JSON serialization
        json_str = overlay.model_dump_json(by_alias=True)
        assert isinstance(json_str, str)

        # Test round-trip
        reconstructed = datawrapper.BarOverlay.model_validate_json(json_str)
        assert reconstructed == overlay

    def test_bar_overlay_field_aliases(self):
        """Test BarOverlay field aliases work correctly."""
        # Create with alias field names
        overlay = datawrapper.BarOverlay(
            to="sales",
            **{"from": "min_sales"},
            showInColorKey=False,
            labelDirectly=False,
        )

        # Serialize with aliases
        data = overlay.model_dump(by_alias=True)

        # Should contain API field names (aliases)
        assert "to" in data  # to_column -> to
        assert "from" in data  # from_column -> from
        assert "showInColorKey" in data  # show_in_color_key -> showInColorKey
        assert "labelDirectly" in data  # label_directly -> labelDirectly

    def test_bar_overlay_validation_edge_cases(self):
        """Test BarOverlay validation edge cases."""
        # Test with whitespace-only strings (allowed by min_length=1)
        overlay = datawrapper.BarOverlay(to="   ")
        assert overlay.to_column == "   "

        # Test with numeric values (should fail)
        with pytest.raises(ValidationError):
            datawrapper.BarOverlay(to=123)

        # Test with boolean values (should fail)
        with pytest.raises(ValidationError):
            datawrapper.BarOverlay(to=True)

    def test_bar_overlay_invalid_pattern(self):
        """Test BarOverlay with invalid pattern."""
        with pytest.raises(ValidationError):
            datawrapper.BarOverlay(to="sales", pattern="invalid")

    def test_bar_overlay_opacity_bounds(self):
        """Test BarOverlay opacity validation."""
        # Valid opacity values should work
        overlay = datawrapper.BarOverlay(to="sales", opacity=0.0)
        assert overlay.opacity == 0.0

        overlay = datawrapper.BarOverlay(to="sales", opacity=1.0)
        assert overlay.opacity == 1.0

        # Test with opacity outside typical bounds (Pydantic may or may not enforce this)
        overlay = datawrapper.BarOverlay(to="sales", opacity=1.5)
        assert overlay.opacity == 1.5  # Pydantic doesn't enforce 0-1 range by default

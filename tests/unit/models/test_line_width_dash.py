"""Unit tests for LineWidth and LineDash enums."""

import pytest
from pydantic import ValidationError

from datawrapper.charts.enums import LineDash, LineWidth
from datawrapper.charts.line import Line


class TestLineWidthEnum:
    """Test the LineWidth enum."""

    def test_enum_values(self):
        """Test that enum values are correct."""
        assert LineWidth.THINNEST.value == "style3"
        assert LineWidth.THIN.value == "style0"
        assert LineWidth.MEDIUM.value == "style1"
        assert LineWidth.THICK.value == "style2"
        assert LineWidth.INVISIBLE.value == "invisible"

    def test_line_with_enum_width(self):
        """Test creating a Line with LineWidth enum."""
        line = Line(column="sales", width=LineWidth.THICK)
        assert line.width == LineWidth.THICK
        assert line.width.value == "style2"

    def test_line_with_string_width(self):
        """Test creating a Line with raw string width (backwards compatibility)."""
        line = Line(column="sales", width="style2")
        assert line.width == "style2"

    def test_line_with_invalid_width(self):
        """Test that invalid width values raise ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            Line(column="sales", width="invalid")

        error_msg = str(exc_info.value)
        assert "Invalid width" in error_msg
        assert "style0, style1, style2, style3, invisible" in error_msg

    def test_line_width_serialization_enum(self):
        """Test that enum width values serialize correctly."""
        line = Line(column="sales", width=LineWidth.THICK)
        serialized = Line.serialize_model(line)
        assert serialized["width"] == "style2"

    def test_line_width_serialization_string(self):
        """Test that string width values serialize correctly."""
        line = Line(column="sales", width="style2")
        serialized = Line.serialize_model(line)
        assert serialized["width"] == "style2"

    def test_line_width_deserialization(self):
        """Test that width values deserialize correctly."""
        api_data = {
            "title": "Sales",
            "width": "style2",
            "interpolation": "linear",
        }
        line_dict = Line.deserialize_model("sales", api_data)
        assert line_dict["width"] == "style2"

        # Can create Line from deserialized data
        line = Line(**line_dict)
        assert line.width == "style2"

    def test_all_width_values_valid(self):
        """Test that all enum values are valid."""
        for width_enum in LineWidth:
            line = Line(column="test", width=width_enum)
            assert line.width == width_enum

            # Test serialization
            serialized = Line.serialize_model(line)
            assert serialized["width"] == width_enum.value


class TestLineDashEnum:
    """Test the LineDash enum."""

    def test_enum_values(self):
        """Test that enum values are correct."""
        assert LineDash.SOLID.value == "style0"
        assert LineDash.SHORT_DASH.value == "style1"
        assert LineDash.MEDIUM_DASH.value == "style2"
        assert LineDash.LONG_DASH.value == "style3"

    def test_line_with_enum_dash(self):
        """Test creating a Line with LineDash enum."""
        line = Line(column="sales", dash=LineDash.MEDIUM_DASH)
        assert line.dash == LineDash.MEDIUM_DASH
        assert line.dash.value == "style2"

    def test_line_with_string_dash(self):
        """Test creating a Line with raw string dash (backwards compatibility)."""
        line = Line(column="sales", dash="style2")
        assert line.dash == "style2"

    def test_line_with_none_dash(self):
        """Test creating a Line with None dash (no dashing)."""
        line = Line(column="sales", dash=None)
        assert line.dash is None

    def test_line_with_invalid_dash(self):
        """Test that invalid dash values raise ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            Line(column="sales", dash="invalid")

        error_msg = str(exc_info.value)
        assert "Invalid dash" in error_msg
        assert "style0, style1, style2, style3" in error_msg

    def test_line_dash_serialization_enum(self):
        """Test that enum dash values serialize correctly."""
        line = Line(column="sales", dash=LineDash.LONG_DASH)
        serialized = Line.serialize_model(line)
        assert serialized["dash"] == "style3"

    def test_line_dash_serialization_string(self):
        """Test that string dash values serialize correctly."""
        line = Line(column="sales", dash="style2")
        serialized = Line.serialize_model(line)
        assert serialized["dash"] == "style2"

    def test_line_dash_serialization_none(self):
        """Test that None dash values serialize correctly (excluded from output)."""
        line = Line(column="sales", dash=None)
        serialized = Line.serialize_model(line)
        assert "dash" not in serialized

    def test_line_dash_deserialization(self):
        """Test that dash values deserialize correctly."""
        api_data = {
            "title": "Sales",
            "dash": "style2",
            "interpolation": "linear",
        }
        line_dict = Line.deserialize_model("sales", api_data)
        assert line_dict["dash"] == "style2"

        # Can create Line from deserialized data
        line = Line(**line_dict)
        assert line.dash == "style2"

    def test_line_dash_deserialization_none(self):
        """Test that missing dash deserializes to None."""
        api_data = {
            "title": "Sales",
            "interpolation": "linear",
        }
        line_dict = Line.deserialize_model("sales", api_data)
        assert line_dict["dash"] is None

        # Can create Line from deserialized data
        line = Line(**line_dict)
        assert line.dash is None

    def test_all_dash_values_valid(self):
        """Test that all enum values are valid."""
        for dash_enum in LineDash:
            line = Line(column="test", dash=dash_enum)
            assert line.dash == dash_enum

            # Test serialization
            serialized = Line.serialize_model(line)
            assert serialized["dash"] == dash_enum.value


class TestLineWidthAndDashTogether:
    """Test using both LineWidth and LineDash together."""

    def test_line_with_both_enums(self):
        """Test creating a Line with both enums."""
        line = Line(
            column="sales",
            width=LineWidth.THICK,
            dash=LineDash.MEDIUM_DASH,
        )
        assert line.width == LineWidth.THICK
        assert line.dash == LineDash.MEDIUM_DASH

    def test_line_with_both_strings(self):
        """Test creating a Line with both raw strings."""
        line = Line(
            column="sales",
            width="style3",
            dash="style2",
        )
        assert line.width == "style3"
        assert line.dash == "style2"

    def test_line_with_mixed_types(self):
        """Test creating a Line with mixed enum and string."""
        line = Line(
            column="sales",
            width=LineWidth.THICK,
            dash="style2",
        )
        assert line.width == LineWidth.THICK
        assert line.dash == "style2"

    def test_serialization_with_both(self):
        """Test serialization with both width and dash."""
        line = Line(
            column="sales",
            width=LineWidth.THICK,
            dash=LineDash.LONG_DASH,
        )
        serialized = Line.serialize_model(line)
        assert serialized["width"] == "style2"
        assert serialized["dash"] == "style3"

    def test_deserialization_with_both(self):
        """Test deserialization with both width and dash."""
        api_data = {
            "title": "Sales",
            "width": "style2",
            "dash": "style3",
            "interpolation": "linear",
        }
        line_dict = Line.deserialize_model("sales", api_data)
        assert line_dict["width"] == "style2"
        assert line_dict["dash"] == "style3"

        # Can create Line from deserialized data
        line = Line(**line_dict)
        assert line.width == "style2"
        assert line.dash == "style3"

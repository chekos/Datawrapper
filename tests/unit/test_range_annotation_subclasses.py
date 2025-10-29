"""Test RangeAnnotation subclasses and validators."""

import pytest
from pydantic import ValidationError

from datawrapper.charts import (
    RangeAnnotation,
    XLineAnnotation,
    XRangeAnnotation,
    YLineAnnotation,
    YRangeAnnotation,
)
from datawrapper.charts.enums import StrokeType, StrokeWidth


class TestRangeAnnotationValidators:
    """Test validators on the base RangeAnnotation class."""

    def test_type_validator_accepts_valid_values(self):
        """Test that type validator accepts 'x' and 'y'."""
        anno_x = RangeAnnotation(type="x", x0=0, x1=10)
        assert anno_x.type == "x"

        anno_y = RangeAnnotation(type="y", y0=0, y1=10)
        assert anno_y.type == "y"

    def test_type_validator_rejects_invalid_values(self):
        """Test that type validator rejects invalid values."""
        with pytest.raises(ValidationError) as exc_info:
            RangeAnnotation(type="z", x0=0, x1=10)
        # Pydantic's Literal validation happens before custom validator
        assert "Input should be 'x' or 'y'" in str(exc_info.value)

    def test_display_validator_accepts_valid_values(self):
        """Test that display validator accepts 'line' and 'range'."""
        anno_line = RangeAnnotation(display="line", x0=0)
        assert anno_line.display == "line"

        anno_range = RangeAnnotation(display="range", x0=0, x1=10)
        assert anno_range.display == "range"

    def test_display_validator_rejects_invalid_values(self):
        """Test that display validator rejects invalid values."""
        with pytest.raises(ValidationError) as exc_info:
            RangeAnnotation(display="invalid", x0=0)
        # Pydantic's Literal validation happens before custom validator
        assert "Input should be 'line' or 'range'" in str(exc_info.value)

    def test_opacity_validator_accepts_valid_range(self):
        """Test that opacity validator accepts values 0-100."""
        # Test boundary values
        anno_0 = RangeAnnotation(opacity=0, x0=0)
        assert anno_0.opacity == 0

        anno_100 = RangeAnnotation(opacity=100, x0=0)
        assert anno_100.opacity == 100

        # Test middle value
        anno_50 = RangeAnnotation(opacity=50, x0=0)
        assert anno_50.opacity == 50

    def test_opacity_validator_rejects_out_of_range(self):
        """Test that opacity validator rejects values outside 0-100."""
        with pytest.raises(ValidationError) as exc_info:
            RangeAnnotation(opacity=-1, x0=0)
        assert "Invalid opacity: -1" in str(exc_info.value)
        assert "Must be between 0 and 100" in str(exc_info.value)

        with pytest.raises(ValidationError) as exc_info:
            RangeAnnotation(opacity=101, x0=0)
        assert "Invalid opacity: 101" in str(exc_info.value)
        assert "Must be between 0 and 100" in str(exc_info.value)

    def test_stroke_type_validator_accepts_enum_values(self):
        """Test that stroke_type validator accepts StrokeType enum values."""
        anno = RangeAnnotation(stroke_type=StrokeType.DASHED, x0=0)
        assert anno.stroke_type == "dashed"

    def test_stroke_type_validator_accepts_valid_strings(self):
        """Test that stroke_type validator accepts valid string values."""
        anno = RangeAnnotation(stroke_type="dotted", x0=0)
        assert anno.stroke_type == "dotted"

    def test_stroke_type_validator_rejects_invalid_strings(self):
        """Test that stroke_type validator rejects invalid string values."""
        with pytest.raises(ValidationError) as exc_info:
            RangeAnnotation(stroke_type="invalid", x0=0)
        assert "Invalid stroke type: invalid" in str(exc_info.value)

    def test_stroke_width_validator_accepts_enum_values(self):
        """Test that stroke_width validator accepts StrokeWidth enum values."""
        anno = RangeAnnotation(stroke_width=StrokeWidth.THICK, x0=0)
        assert anno.stroke_width == 3

    def test_stroke_width_validator_accepts_valid_ints(self):
        """Test that stroke_width validator accepts valid int values."""
        anno = RangeAnnotation(stroke_width=2, x0=0)
        assert anno.stroke_width == 2

    def test_stroke_width_validator_rejects_invalid_ints(self):
        """Test that stroke_width validator rejects invalid int values."""
        with pytest.raises(ValidationError) as exc_info:
            RangeAnnotation(stroke_width=99, x0=0)
        assert "Invalid stroke width: 99" in str(exc_info.value)


class TestXRangeAnnotation:
    """Test XRangeAnnotation subclass."""

    def test_automatic_field_setting(self):
        """Test that type and display are automatically set."""
        anno = XRangeAnnotation(x0=0, x1=10)
        assert anno.type == "x"
        assert anno.display == "range"

    def test_requires_both_x_positions(self):
        """Test that both x0 and x1 are required."""
        # Should work with both positions
        anno = XRangeAnnotation(x0=0, x1=10)
        assert anno.x0 == 0
        assert anno.x1 == 10

        # Should fail without x0
        with pytest.raises(ValidationError) as exc_info:
            XRangeAnnotation(x1=10)
        assert "requires both x0 and x1" in str(exc_info.value)

        # Should fail without x1
        with pytest.raises(ValidationError) as exc_info:
            XRangeAnnotation(x0=0)
        assert "requires both x0 and x1" in str(exc_info.value)

        # Should fail without both
        with pytest.raises(ValidationError) as exc_info:
            XRangeAnnotation()
        assert "requires both x0 and x1" in str(exc_info.value)

    def test_accepts_custom_color_and_opacity(self):
        """Test that custom color and opacity can be set."""
        anno = XRangeAnnotation(x0=0, x1=10, color="#ff0000", opacity=75)
        assert anno.color == "#ff0000"
        assert anno.opacity == 75

    def test_serialization(self):
        """Test that serialization works correctly."""
        anno = XRangeAnnotation(x0=0, x1=10, color="#ff0000")
        serialized = anno.serialize_model()
        assert serialized["type"] == "x"
        assert serialized["display"] == "range"
        assert serialized["position"]["x0"] == 0
        assert serialized["position"]["x1"] == 10
        assert serialized["color"] == "#ff0000"

    def test_cannot_override_type_or_display(self):
        """Test that type and display cannot be overridden to invalid values."""
        # Type is automatically set to "x", so trying to set it to "y" should still result in "x"
        anno = XRangeAnnotation(x0=0, x1=10, type="x")
        assert anno.type == "x"

        # Display is automatically set to "range"
        anno = XRangeAnnotation(x0=0, x1=10, display="range")
        assert anno.display == "range"


class TestYRangeAnnotation:
    """Test YRangeAnnotation subclass."""

    def test_automatic_field_setting(self):
        """Test that type and display are automatically set."""
        anno = YRangeAnnotation(y0=0, y1=10)
        assert anno.type == "y"
        assert anno.display == "range"

    def test_requires_both_y_positions(self):
        """Test that both y0 and y1 are required."""
        # Should work with both positions
        anno = YRangeAnnotation(y0=0, y1=10)
        assert anno.y0 == 0
        assert anno.y1 == 10

        # Should fail without y0
        with pytest.raises(ValidationError) as exc_info:
            YRangeAnnotation(y1=10)
        assert "requires both y0 and y1" in str(exc_info.value)

        # Should fail without y1
        with pytest.raises(ValidationError) as exc_info:
            YRangeAnnotation(y0=0)
        assert "requires both y0 and y1" in str(exc_info.value)

        # Should fail without both
        with pytest.raises(ValidationError) as exc_info:
            YRangeAnnotation()
        assert "requires both y0 and y1" in str(exc_info.value)

    def test_accepts_custom_color_and_opacity(self):
        """Test that custom color and opacity can be set."""
        anno = YRangeAnnotation(y0=0, y1=10, color="#00ff00", opacity=25)
        assert anno.color == "#00ff00"
        assert anno.opacity == 25

    def test_serialization(self):
        """Test that serialization works correctly."""
        anno = YRangeAnnotation(y0=0, y1=10, color="#00ff00")
        serialized = anno.serialize_model()
        assert serialized["type"] == "y"
        assert serialized["display"] == "range"
        assert serialized["position"]["y0"] == 0
        assert serialized["position"]["y1"] == 10
        assert serialized["color"] == "#00ff00"


class TestXLineAnnotation:
    """Test XLineAnnotation subclass."""

    def test_automatic_field_setting(self):
        """Test that type and display are automatically set."""
        anno = XLineAnnotation(x0=5)
        assert anno.type == "x"
        assert anno.display == "line"

    def test_requires_x0_position(self):
        """Test that x0 is required."""
        # Should work with x0
        anno = XLineAnnotation(x0=5)
        assert anno.x0 == 5

        # Should fail without x0
        with pytest.raises(ValidationError) as exc_info:
            XLineAnnotation()
        assert "requires x0 to be set" in str(exc_info.value)

    def test_x1_is_optional(self):
        """Test that x1 is optional for line annotations."""
        anno = XLineAnnotation(x0=5)
        assert anno.x1 is None

        # Can also provide x1 if desired (though not typical for line)
        anno_with_x1 = XLineAnnotation(x0=5, x1=10)
        assert anno_with_x1.x0 == 5
        assert anno_with_x1.x1 == 10

    def test_accepts_stroke_customization(self):
        """Test that stroke type and width can be customized."""
        anno = XLineAnnotation(
            x0=5, stroke_type=StrokeType.DASHED, stroke_width=StrokeWidth.THICK
        )
        assert anno.stroke_type == "dashed"
        assert anno.stroke_width == 3

    def test_serialization(self):
        """Test that serialization works correctly."""
        anno = XLineAnnotation(x0=5, color="#0000ff", stroke_type="dotted")
        serialized = anno.serialize_model()
        assert serialized["type"] == "x"
        assert serialized["display"] == "line"
        assert serialized["position"]["x0"] == 5
        assert "x1" not in serialized["position"]  # x1 should not be included if None
        assert serialized["color"] == "#0000ff"
        assert serialized["strokeType"] == "dotted"


class TestYLineAnnotation:
    """Test YLineAnnotation subclass."""

    def test_automatic_field_setting(self):
        """Test that type and display are automatically set."""
        anno = YLineAnnotation(y0=5)
        assert anno.type == "y"
        assert anno.display == "line"

    def test_requires_y0_position(self):
        """Test that y0 is required."""
        # Should work with y0
        anno = YLineAnnotation(y0=5)
        assert anno.y0 == 5

        # Should fail without y0
        with pytest.raises(ValidationError) as exc_info:
            YLineAnnotation()
        assert "requires y0 to be set" in str(exc_info.value)

    def test_y1_is_optional(self):
        """Test that y1 is optional for line annotations."""
        anno = YLineAnnotation(y0=5)
        assert anno.y1 is None

        # Can also provide y1 if desired (though not typical for line)
        anno_with_y1 = YLineAnnotation(y0=5, y1=10)
        assert anno_with_y1.y0 == 5
        assert anno_with_y1.y1 == 10

    def test_accepts_stroke_customization(self):
        """Test that stroke type and width can be customized."""
        anno = YLineAnnotation(
            y0=5, stroke_type=StrokeType.DOTTED, stroke_width=StrokeWidth.MEDIUM
        )
        assert anno.stroke_type == "dotted"
        assert anno.stroke_width == 2

    def test_serialization(self):
        """Test that serialization works correctly."""
        anno = YLineAnnotation(y0=5, color="#ff00ff", stroke_width=3)
        serialized = anno.serialize_model()
        assert serialized["type"] == "y"
        assert serialized["display"] == "line"
        assert serialized["position"]["y0"] == 5
        assert "y1" not in serialized["position"]  # y1 should not be included if None
        assert serialized["color"] == "#ff00ff"
        assert serialized["strokeWidth"] == 3


class TestSubclassInheritance:
    """Test that subclasses properly inherit validators from parent."""

    def test_xrange_inherits_opacity_validator(self):
        """Test that XRangeAnnotation inherits opacity validator."""
        with pytest.raises(ValidationError) as exc_info:
            XRangeAnnotation(x0=0, x1=10, opacity=150)
        assert "Invalid opacity: 150" in str(exc_info.value)

    def test_yrange_inherits_type_validator(self):
        """Test that YRangeAnnotation inherits type validator."""
        # Type is auto-set to "y", but validator should still work
        anno = YRangeAnnotation(y0=0, y1=10)
        assert anno.type == "y"

    def test_xline_inherits_stroke_validators(self):
        """Test that XLineAnnotation inherits stroke validators."""
        with pytest.raises(ValidationError) as exc_info:
            XLineAnnotation(x0=5, stroke_type="invalid")
        assert "Invalid stroke type: invalid" in str(exc_info.value)

        with pytest.raises(ValidationError) as exc_info:
            XLineAnnotation(x0=5, stroke_width=99)
        assert "Invalid stroke width: 99" in str(exc_info.value)

    def test_yline_inherits_all_validators(self):
        """Test that YLineAnnotation inherits all validators from parent."""
        # Test opacity validator
        with pytest.raises(ValidationError) as exc_info:
            YLineAnnotation(y0=5, opacity=200)
        assert "Invalid opacity: 200" in str(exc_info.value)

        # Test stroke validators
        with pytest.raises(ValidationError) as exc_info:
            YLineAnnotation(y0=5, stroke_type="bad")
        assert "Invalid stroke type: bad" in str(exc_info.value)

        with pytest.raises(ValidationError) as exc_info:
            YLineAnnotation(y0=5, stroke_width=100)
        assert "Invalid stroke width: 100" in str(exc_info.value)

"""Test MultipleColumn RangeAnnotation subclasses and validators."""

import pytest
from pydantic import ValidationError

from datawrapper.charts.multiple_column import (
    MultipleColumnRangeAnnotation,
    MultipleColumnXLineAnnotation,
    MultipleColumnXRangeAnnotation,
    MultipleColumnYLineAnnotation,
    MultipleColumnYRangeAnnotation,
)


class TestMultipleColumnRangeAnnotationValidators:
    """Test validators on the base MultipleColumnRangeAnnotation class."""

    def test_inherits_base_validators(self):
        """Test that MultipleColumnRangeAnnotation inherits validators from RangeAnnotation."""
        # Test opacity validator
        with pytest.raises(ValidationError) as exc_info:
            MultipleColumnRangeAnnotation(x0=0, opacity=150)
        assert "Invalid opacity: 150" in str(exc_info.value)

    def test_plot_field_accepts_str(self):
        """Test that plot field accepts string values."""
        anno = MultipleColumnRangeAnnotation(x0=0, plot="2")
        assert anno.plot == "2"

    def test_plot_field_optional(self):
        """Test that plot field is optional."""
        anno = MultipleColumnRangeAnnotation(x0=0)
        assert anno.plot is None

    def test_serialization_includes_plot_field(self):
        """Test that serialization includes plot field in position object."""
        anno = MultipleColumnRangeAnnotation(x0=0, x1=10, plot="1")
        serialized = anno.serialize_model()
        assert serialized["position"]["plot"] == "1"

    def test_serialization_excludes_none_plot(self):
        """Test that serialization excludes plot field when None."""
        anno = MultipleColumnRangeAnnotation(x0=0, x1=10)
        serialized = anno.serialize_model()
        assert "plot" not in serialized["position"]


class TestMultipleColumnXRangeAnnotation:
    """Test MultipleColumnXRangeAnnotation subclass."""

    def test_automatic_field_setting(self):
        """Test that type and display are automatically set."""
        anno = MultipleColumnXRangeAnnotation(x0=0, x1=10)
        assert anno.type == "x"
        assert anno.display == "range"

    def test_requires_both_x_positions(self):
        """Test that both x0 and x1 are required."""
        # Should work with both positions
        anno = MultipleColumnXRangeAnnotation(x0=0, x1=10)
        assert anno.x0 == 0
        assert anno.x1 == 10

        # Should fail without x0
        with pytest.raises(ValidationError) as exc_info:
            MultipleColumnXRangeAnnotation(x1=10)
        assert "requires both x0 and x1" in str(exc_info.value)

        # Should fail without x1
        with pytest.raises(ValidationError) as exc_info:
            MultipleColumnXRangeAnnotation(x0=0)
        assert "requires both x0 and x1" in str(exc_info.value)

        # Should fail without both
        with pytest.raises(ValidationError) as exc_info:
            MultipleColumnXRangeAnnotation()
        assert "requires both x0 and x1" in str(exc_info.value)

    def test_accepts_custom_color_and_opacity(self):
        """Test that custom color and opacity can be set."""
        anno = MultipleColumnXRangeAnnotation(x0=0, x1=10, color="#ff0000", opacity=75)
        assert anno.color == "#ff0000"
        assert anno.opacity == 75

    def test_accepts_plot_field(self):
        """Test that plot field can be set."""
        anno = MultipleColumnXRangeAnnotation(x0=0, x1=10, plot="2")
        assert anno.plot == "2"

    def test_serialization(self):
        """Test that serialization works correctly."""
        anno = MultipleColumnXRangeAnnotation(x0=0, x1=10, color="#ff0000", plot="1")
        serialized = anno.serialize_model()
        assert serialized["type"] == "x"
        assert serialized["display"] == "range"
        assert serialized["position"]["x0"] == 0
        assert serialized["position"]["x1"] == 10
        assert serialized["position"]["plot"] == "1"
        assert serialized["color"] == "#ff0000"

    def test_cannot_override_type_or_display(self):
        """Test that type and display cannot be overridden to invalid values."""
        # Type is automatically set to "x"
        anno = MultipleColumnXRangeAnnotation(x0=0, x1=10, type="x")
        assert anno.type == "x"

        # Display is automatically set to "range"
        anno = MultipleColumnXRangeAnnotation(x0=0, x1=10, display="range")
        assert anno.display == "range"


class TestMultipleColumnYRangeAnnotation:
    """Test MultipleColumnYRangeAnnotation subclass."""

    def test_automatic_field_setting(self):
        """Test that type and display are automatically set."""
        anno = MultipleColumnYRangeAnnotation(y0=0, y1=10)
        assert anno.type == "y"
        assert anno.display == "range"

    def test_requires_both_y_positions(self):
        """Test that both y0 and y1 are required."""
        # Should work with both positions
        anno = MultipleColumnYRangeAnnotation(y0=0, y1=10)
        assert anno.y0 == 0
        assert anno.y1 == 10

        # Should fail without y0
        with pytest.raises(ValidationError) as exc_info:
            MultipleColumnYRangeAnnotation(y1=10)
        assert "requires both y0 and y1" in str(exc_info.value)

        # Should fail without y1
        with pytest.raises(ValidationError) as exc_info:
            MultipleColumnYRangeAnnotation(y0=0)
        assert "requires both y0 and y1" in str(exc_info.value)

        # Should fail without both
        with pytest.raises(ValidationError) as exc_info:
            MultipleColumnYRangeAnnotation()
        assert "requires both y0 and y1" in str(exc_info.value)

    def test_accepts_custom_color_and_opacity(self):
        """Test that custom color and opacity can be set."""
        anno = MultipleColumnYRangeAnnotation(y0=0, y1=10, color="#00ff00", opacity=25)
        assert anno.color == "#00ff00"
        assert anno.opacity == 25

    def test_accepts_plot_field(self):
        """Test that plot field can be set."""
        anno = MultipleColumnYRangeAnnotation(y0=0, y1=10, plot="3")
        assert anno.plot == "3"

    def test_serialization(self):
        """Test that serialization works correctly."""
        anno = MultipleColumnYRangeAnnotation(y0=0, y1=10, color="#00ff00", plot="2")
        serialized = anno.serialize_model()
        assert serialized["type"] == "y"
        assert serialized["display"] == "range"
        assert serialized["position"]["y0"] == 0
        assert serialized["position"]["y1"] == 10
        assert serialized["position"]["plot"] == "2"
        assert serialized["color"] == "#00ff00"


class TestMultipleColumnXLineAnnotation:
    """Test MultipleColumnXLineAnnotation subclass."""

    def test_automatic_field_setting(self):
        """Test that type and display are automatically set."""
        anno = MultipleColumnXLineAnnotation(x0=5)
        assert anno.type == "x"
        assert anno.display == "line"

    def test_requires_x0_position(self):
        """Test that x0 is required."""
        # Should work with x0
        anno = MultipleColumnXLineAnnotation(x0=5)
        assert anno.x0 == 5

        # Should fail without x0
        with pytest.raises(ValidationError) as exc_info:
            MultipleColumnXLineAnnotation()
        assert "requires x0 to be set" in str(exc_info.value)

    def test_x1_is_optional(self):
        """Test that x1 is optional for line annotations."""
        anno = MultipleColumnXLineAnnotation(x0=5)
        assert anno.x1 is None

        # Can also provide x1 if desired (though not typical for line)
        anno_with_x1 = MultipleColumnXLineAnnotation(x0=5, x1=10)
        assert anno_with_x1.x0 == 5
        assert anno_with_x1.x1 == 10

    def test_accepts_plot_field(self):
        """Test that plot field can be set."""
        anno = MultipleColumnXLineAnnotation(x0=5, plot="1")
        assert anno.plot == "1"

    def test_serialization(self):
        """Test that serialization works correctly."""
        anno = MultipleColumnXLineAnnotation(x0=5, color="#0000ff", plot="0")
        serialized = anno.serialize_model()
        assert serialized["type"] == "x"
        assert serialized["display"] == "line"
        assert serialized["position"]["x0"] == 5
        assert "x1" not in serialized["position"]  # x1 should not be included if None
        assert serialized["position"]["plot"] == "0"
        assert serialized["color"] == "#0000ff"


class TestMultipleColumnYLineAnnotation:
    """Test MultipleColumnYLineAnnotation subclass."""

    def test_automatic_field_setting(self):
        """Test that type and display are automatically set."""
        anno = MultipleColumnYLineAnnotation(y0=5)
        assert anno.type == "y"
        assert anno.display == "line"

    def test_requires_y0_position(self):
        """Test that y0 is required."""
        # Should work with y0
        anno = MultipleColumnYLineAnnotation(y0=5)
        assert anno.y0 == 5

        # Should fail without y0
        with pytest.raises(ValidationError) as exc_info:
            MultipleColumnYLineAnnotation()
        assert "requires y0 to be set" in str(exc_info.value)

    def test_y1_is_optional(self):
        """Test that y1 is optional for line annotations."""
        anno = MultipleColumnYLineAnnotation(y0=5)
        assert anno.y1 is None

        # Can also provide y1 if desired (though not typical for line)
        anno_with_y1 = MultipleColumnYLineAnnotation(y0=5, y1=10)
        assert anno_with_y1.y0 == 5
        assert anno_with_y1.y1 == 10

    def test_accepts_plot_field(self):
        """Test that plot field can be set."""
        anno = MultipleColumnYLineAnnotation(y0=5, plot="4")
        assert anno.plot == "4"

    def test_serialization(self):
        """Test that serialization works correctly."""
        anno = MultipleColumnYLineAnnotation(y0=5, color="#ff00ff", plot="2")
        serialized = anno.serialize_model()
        assert serialized["type"] == "y"
        assert serialized["display"] == "line"
        assert serialized["position"]["y0"] == 5
        assert "y1" not in serialized["position"]  # y1 should not be included if None
        assert serialized["position"]["plot"] == "2"
        assert serialized["color"] == "#ff00ff"


class TestSubclassInheritance:
    """Test that subclasses properly inherit validators from parent."""

    def test_xrange_inherits_opacity_validator(self):
        """Test that MultipleColumnXRangeAnnotation inherits opacity validator."""
        with pytest.raises(ValidationError) as exc_info:
            MultipleColumnXRangeAnnotation(x0=0, x1=10, opacity=150)
        assert "Invalid opacity: 150" in str(exc_info.value)

    def test_yrange_inherits_type_validator(self):
        """Test that MultipleColumnYRangeAnnotation inherits type validator."""
        # Type is auto-set to "y", but validator should still work
        anno = MultipleColumnYRangeAnnotation(y0=0, y1=10)
        assert anno.type == "y"

    def test_xline_inherits_validators(self):
        """Test that MultipleColumnXLineAnnotation inherits validators."""
        with pytest.raises(ValidationError) as exc_info:
            MultipleColumnXLineAnnotation(x0=5, opacity=200)
        assert "Invalid opacity: 200" in str(exc_info.value)

    def test_yline_inherits_all_validators(self):
        """Test that MultipleColumnYLineAnnotation inherits all validators from parent."""
        # Test opacity validator
        with pytest.raises(ValidationError) as exc_info:
            MultipleColumnYLineAnnotation(y0=5, opacity=200)
        assert "Invalid opacity: 200" in str(exc_info.value)

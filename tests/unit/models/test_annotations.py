"""Unit tests for annotation models."""

import pytest
from pydantic import ValidationError

from datawrapper import ConnectorLine, RangeAnnotation, TextAnnotation


class TestConnectorLine:
    """Test ConnectorLine model."""

    @pytest.mark.unit
    def test_connector_line_defaults(self):
        """Test ConnectorLine with default values."""
        connector = ConnectorLine()

        assert connector.type == "straight"
        assert connector.circle is False
        assert connector.stroke == 1
        assert (
            connector.enabled is True
        )  # Always True with "enabled by presence" pattern
        assert connector.arrow_head == "lines"
        assert connector.circle_style == "solid"
        assert connector.circle_radius == 15
        assert connector.inherit_color is False
        assert connector.target_padding == 4

    @pytest.mark.unit
    def test_connector_line_custom_values(self):
        """Test ConnectorLine with custom values."""
        connector = ConnectorLine(
            type="curveRight",
            circle=True,
            stroke=3,
            arrowHead="triangle",
            circleStyle="dashed",
            circleRadius=20,
            inheritColor=True,
            targetPadding=8,
        )

        assert connector.type == "curveRight"
        assert connector.circle is True
        assert connector.stroke == 3
        assert connector.enabled is True  # Always True
        assert connector.arrow_head == "triangle"
        assert connector.circle_style == "dashed"
        assert connector.circle_radius == 20
        assert connector.inherit_color is True
        assert connector.target_padding == 8

    @pytest.mark.unit
    def test_connector_line_invalid_type(self):
        """Test ConnectorLine with invalid type."""
        with pytest.raises(ValidationError):
            ConnectorLine(type="invalid")

    @pytest.mark.unit
    def test_connector_line_invalid_stroke(self):
        """Test ConnectorLine with invalid stroke."""
        with pytest.raises(ValidationError):
            ConnectorLine(stroke=5)

    @pytest.mark.unit
    def test_connector_line_serialization(self, assert_valid_serialization):
        """Test ConnectorLine serialization."""
        connector = ConnectorLine(type="curveLeft", stroke=2)
        assert_valid_serialization(connector)


class TestTextAnnotation:
    """Test TextAnnotation model."""

    @pytest.mark.unit
    def test_text_annotation_minimal(self):
        """Test TextAnnotation with minimal required fields."""
        annotation = TextAnnotation(text="Test", x=10, y=20)

        assert annotation.text == "Test"
        assert annotation.x == 10
        assert annotation.y == 20
        assert annotation.outline is True
        assert annotation.dx == 0
        assert annotation.dy == 0
        assert annotation.bold is False
        assert annotation.size == 14
        assert annotation.align == "tl"
        assert annotation.color is False
        assert annotation.width == 33.3
        assert annotation.italic is False
        assert annotation.underline is False
        assert annotation.show_mobile is True
        assert annotation.show_desktop is True
        assert annotation.mobile_fallback is False

    @pytest.mark.unit
    def test_text_annotation_full(self):
        """Test TextAnnotation with all fields."""
        connector = ConnectorLine()
        annotation = TextAnnotation(
            text="Full Test",
            x=50,
            y=75,
            outline=False,
            dx=5,
            dy=-5,
            bold=True,
            size=18,
            align="mc",
            color="#FF0000",
            width=50.0,
            italic=True,
            underline=True,
            showMobile=False,
            showDesktop=True,
            connectorLine=connector,
            mobileFallback=True,
        )

        assert annotation.text == "Full Test"
        assert annotation.x == 50
        assert annotation.y == 75
        assert annotation.outline is False
        assert annotation.dx == 5
        assert annotation.dy == -5
        assert annotation.bold is True
        assert annotation.size == 18
        assert annotation.align == "mc"
        assert annotation.color == "#FF0000"
        assert annotation.width == 50.0
        assert annotation.italic is True
        assert annotation.underline is True
        assert annotation.show_mobile is False
        assert annotation.show_desktop is True
        assert isinstance(annotation.connector_line, ConnectorLine)
        assert annotation.mobile_fallback is True

    @pytest.mark.unit
    def test_text_annotation_empty_text(self):
        """Test TextAnnotation with empty text."""
        with pytest.raises(ValidationError):
            TextAnnotation(text="", x=10, y=20)

    @pytest.mark.unit
    def test_text_annotation_invalid_align(self):
        """Test TextAnnotation with invalid alignment."""
        with pytest.raises(ValidationError):
            TextAnnotation(text="Test", x=10, y=20, align="invalid")

    @pytest.mark.unit
    def test_text_annotation_serialization(self):
        """Test TextAnnotation serialization."""
        annotation = TextAnnotation(
            text="Serialize Test", x=30, y=40, bold=True, color="#00FF00"
        )

        serialized = annotation.serialize_model()

        assert isinstance(serialized, dict)
        assert serialized["text"] == "Serialize Test"
        assert serialized["position"]["x"] == 30
        assert serialized["position"]["y"] == 40
        assert serialized["bold"] is True
        assert serialized["color"] == "#00FF00"
        assert "connectorLine" in serialized

    @pytest.mark.unit
    def test_text_annotation_connector_line_dict(self):
        """Test TextAnnotation with connector line as dict."""
        connector_dict = {"type": "curveRight", "stroke": 2}

        annotation = TextAnnotation(
            text="Test", x=10, y=20, connectorLine=connector_dict
        )

        serialized = annotation.serialize_model()
        assert serialized["connectorLine"]["type"] == "curveRight"
        assert (
            serialized["connectorLine"]["enabled"] is True
        )  # Always True when present
        assert serialized["connectorLine"]["stroke"] == 2

    @pytest.mark.unit
    def test_text_annotation_with_fixture(self, text_annotation):
        """Test TextAnnotation using fixture."""
        assert isinstance(text_annotation, TextAnnotation)
        assert len(text_annotation.text) > 0

        # Test standard Pydantic serialization (not API serialization)
        python_dict = text_annotation.model_dump()
        assert isinstance(python_dict, dict)

        json_str = text_annotation.model_dump_json()
        assert isinstance(json_str, str)

        # Test round-trip with standard Pydantic serialization
        reconstructed = TextAnnotation.model_validate_json(json_str)
        assert reconstructed == text_annotation

        # Test API serialization separately (this is different format)
        api_serialized = text_annotation.serialize_model()
        assert isinstance(api_serialized, dict)
        assert "position" in api_serialized
        assert "x" in api_serialized["position"]
        assert "y" in api_serialized["position"]


class TestRangeAnnotation:
    """Test RangeAnnotation model."""

    @pytest.mark.unit
    def test_range_annotation_minimal(self):
        """Test RangeAnnotation with minimal required fields."""
        annotation = RangeAnnotation(x0=0, x1=10, y0=0, y1=10)

        assert annotation.type == "x"
        assert annotation.color == "#989898"
        assert annotation.display == "range"
        assert annotation.opacity == 50
        assert annotation.x0 == 0
        assert annotation.x1 == 10
        assert annotation.y0 == 0
        assert annotation.y1 == 10
        assert annotation.stroke_type == "solid"
        assert annotation.stroke_width == 2

    @pytest.mark.unit
    def test_range_annotation_full(self):
        """Test RangeAnnotation with all fields."""
        annotation = RangeAnnotation(
            type="y",
            color="#FF0000",
            display="line",
            opacity=75,
            x0=5,
            x1=15,
            y0=10,
            y1=20,
            strokeType="dashed",
            strokeWidth=3,
        )

        assert annotation.type == "y"
        assert annotation.color == "#FF0000"
        assert annotation.display == "line"
        assert annotation.opacity == 75
        assert annotation.x0 == 5
        assert annotation.x1 == 15
        assert annotation.y0 == 10
        assert annotation.y1 == 20
        assert annotation.stroke_type == "dashed"
        assert annotation.stroke_width == 3

    @pytest.mark.unit
    def test_range_annotation_invalid_type(self):
        """Test RangeAnnotation with invalid type."""
        with pytest.raises(ValidationError):
            RangeAnnotation(type="z", x0=0, x1=10, y0=0, y1=10)

    @pytest.mark.unit
    def test_range_annotation_invalid_display(self):
        """Test RangeAnnotation with invalid display."""
        with pytest.raises(ValidationError):
            RangeAnnotation(display="invalid", x0=0, x1=10, y0=0, y1=10)

    @pytest.mark.unit
    def test_range_annotation_invalid_stroke_type(self):
        """Test RangeAnnotation with invalid stroke type."""
        with pytest.raises(ValidationError):
            RangeAnnotation(strokeType="invalid", x0=0, x1=10, y0=0, y1=10)

    @pytest.mark.unit
    def test_range_annotation_invalid_stroke_width(self):
        """Test RangeAnnotation with invalid stroke width."""
        with pytest.raises(ValidationError):
            RangeAnnotation(strokeWidth=5, x0=0, x1=10, y0=0, y1=10)

    @pytest.mark.unit
    def test_range_annotation_serialization(self):
        """Test RangeAnnotation serialization."""
        annotation = RangeAnnotation(
            type="y",
            color="#00FF00",
            display="line",
            x0=10,
            x1=20,
            y0=30,
            y1=40,
            strokeType="dotted",
        )

        serialized = annotation.serialize_model()

        assert isinstance(serialized, dict)
        assert serialized["type"] == "y"
        assert serialized["color"] == "#00FF00"
        assert serialized["display"] == "line"
        assert serialized["position"]["x0"] == 10
        assert serialized["position"]["x1"] == 20
        assert serialized["position"]["y0"] == 30
        assert serialized["position"]["y1"] == 40
        assert serialized["strokeType"] == "dotted"

    @pytest.mark.unit
    def test_range_annotation_with_fixture(
        self, range_annotation, assert_valid_serialization
    ):
        """Test RangeAnnotation using fixture."""
        assert isinstance(range_annotation, RangeAnnotation)
        assert range_annotation.x0 is not None
        assert range_annotation.x1 is not None
        assert range_annotation.y0 is not None
        assert range_annotation.y1 is not None
        assert_valid_serialization(range_annotation)

    @pytest.mark.unit
    def test_range_annotation_string_positions(self):
        """Test RangeAnnotation with string positions (for data values)."""
        annotation = RangeAnnotation(x0="Category A", x1="Category C", y0=0, y1=100)

        assert annotation.x0 == "Category A"
        assert annotation.x1 == "Category C"
        assert annotation.y0 == 0
        assert annotation.y1 == 100

    @pytest.mark.unit
    @pytest.mark.parametrize(
        "annotation_type,expected",
        [
            ("x", "x"),
            ("y", "y"),
        ],
    )
    def test_range_annotation_types(self, annotation_type, expected):
        """Test different range annotation types."""
        annotation = RangeAnnotation(type=annotation_type, x0=0, x1=10, y0=0, y1=10)
        assert annotation.type == expected

    @pytest.mark.unit
    @pytest.mark.parametrize(
        "display_type,expected",
        [
            ("line", "line"),
            ("range", "range"),
        ],
    )
    def test_range_annotation_display_types(self, display_type, expected):
        """Test different range annotation display types."""
        annotation = RangeAnnotation(display=display_type, x0=0, x1=10, y0=0, y1=10)
        assert annotation.display == expected

"""Test ConnectorLine enabled by presence pattern."""

import pytest
from pydantic import ValidationError

from datawrapper.charts.annos import ConnectorLine, TextAnnotation


class TestConnectorLineEnabledByPresence:
    """Test the enabled by presence pattern for ConnectorLine."""

    def test_connector_line_enabled_defaults_to_true(self):
        """Test that enabled defaults to True when ConnectorLine is created."""
        connector = ConnectorLine()
        assert connector.enabled is True

    def test_connector_line_enabled_can_be_true(self):
        """Test that enabled can be explicitly set to True."""
        connector = ConnectorLine(enabled=True, type="curveRight")
        assert connector.enabled is True
        assert connector.type == "curveRight"

    def test_connector_line_enabled_cannot_be_false(self):
        """Test that enabled cannot be set to False."""
        with pytest.raises(ValidationError) as exc_info:
            ConnectorLine(enabled=False)

        error = exc_info.value.errors()[0]
        assert "enabled cannot be False" in error["msg"]
        assert "omit the connector_line field" in error["msg"]

    def test_text_annotation_with_connector_line(self):
        """Test TextAnnotation with connector line enabled."""
        anno = TextAnnotation(
            text="Test",
            x=10,
            y=20,
            connector_line=ConnectorLine(type="curveRight", stroke=2),
        )

        assert anno.connector_line is not None
        assert anno.connector_line.enabled is True
        assert anno.connector_line.type == "curveRight"
        assert anno.connector_line.stroke == 2

    def test_text_annotation_without_connector_line(self):
        """Test TextAnnotation with connector line disabled (None)."""
        anno = TextAnnotation(text="Test", x=10, y=20)

        assert anno.connector_line is None

    def test_text_annotation_serialization_with_connector_line(self):
        """Test serialization when connector line is enabled."""
        anno = TextAnnotation(
            text="Test",
            x=10,
            y=20,
            connector_line=ConnectorLine(type="curveRight", stroke=2, circle=True),
        )

        serialized = anno.serialize_model()

        assert "connectorLine" in serialized
        assert serialized["connectorLine"]["enabled"] is True
        assert serialized["connectorLine"]["type"] == "curveRight"
        assert serialized["connectorLine"]["stroke"] == 2
        assert serialized["connectorLine"]["circle"] is True

    def test_text_annotation_serialization_without_connector_line(self):
        """Test serialization when connector line is disabled (None)."""
        anno = TextAnnotation(text="Test", x=10, y=20, connector_line=None)

        serialized = anno.serialize_model()

        assert "connectorLine" in serialized
        assert serialized["connectorLine"] == {"enabled": False}

    def test_text_annotation_deserialization_with_enabled_connector_line(self):
        """Test deserialization when API has enabled connector line."""
        api_data = {
            "anno-1": {
                "text": "Test",
                "position": {"x": 10, "y": 20},
                "connectorLine": {
                    "enabled": True,
                    "type": "curveRight",
                    "stroke": 2,
                    "circle": True,
                },
            }
        }

        result = TextAnnotation.deserialize_model(api_data)

        assert len(result) == 1
        assert result[0]["id"] == "anno-1"
        assert result[0]["connectorLine"]["enabled"] is True
        assert result[0]["connectorLine"]["type"] == "curveRight"

    def test_text_annotation_deserialization_with_disabled_connector_line(self):
        """Test deserialization when API has disabled connector line."""
        api_data = {
            "anno-1": {
                "text": "Test",
                "position": {"x": 10, "y": 20},
                "connectorLine": {"enabled": False},
            }
        }

        result = TextAnnotation.deserialize_model(api_data)

        assert len(result) == 1
        assert result[0]["id"] == "anno-1"
        assert result[0]["connectorLine"] is None

    def test_text_annotation_deserialization_without_connector_line(self):
        """Test deserialization when API has no connector line field."""
        api_data = {
            "anno-1": {
                "text": "Test",
                "position": {"x": 10, "y": 20},
            }
        }

        result = TextAnnotation.deserialize_model(api_data)

        assert len(result) == 1
        assert result[0]["id"] == "anno-1"
        # connectorLine key should not be present in result
        assert "connectorLine" not in result[0]

    def test_connector_line_with_dict_input(self):
        """Test TextAnnotation with connector line as dict."""
        anno = TextAnnotation(
            text="Test",
            x=10,
            y=20,
            connector_line={"type": "curveLeft", "stroke": 3, "enabled": True},
        )

        serialized = anno.serialize_model()

        assert serialized["connectorLine"]["enabled"] is True
        assert serialized["connectorLine"]["type"] == "curveLeft"
        assert serialized["connectorLine"]["stroke"] == 3

    def test_connector_line_dict_with_enabled_false_raises_error(self):
        """Test that dict with enabled=False raises validation error during serialization."""
        anno = TextAnnotation(
            text="Test",
            x=10,
            y=20,
            connector_line={"enabled": False},
        )

        # The validation happens during serialization when the dict is converted to ConnectorLine
        with pytest.raises(ValidationError) as exc_info:
            anno.serialize_model()

        error = exc_info.value.errors()[0]
        assert "enabled cannot be False" in error["msg"]

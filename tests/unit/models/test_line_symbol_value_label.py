"""Test LineSymbol and LineValueLabel validation."""

import pytest
from pydantic import ValidationError

from datawrapper.charts.line import Line, LineSymbol, LineValueLabel


class TestLineSymbolValidation:
    """Test LineSymbol validation."""

    def test_line_symbol_enabled_defaults_to_true(self):
        """Test that LineSymbol.enabled defaults to True."""
        symbol = LineSymbol()
        assert symbol.enabled is True

    def test_line_symbol_enabled_true_is_valid(self):
        """Test that explicitly setting enabled=True is valid."""
        symbol = LineSymbol(enabled=True, shape="square")
        assert symbol.enabled is True
        assert symbol.shape == "square"

    def test_line_symbol_enabled_false_raises_error(self):
        """Test that setting enabled=False raises a validation error."""
        with pytest.raises(ValidationError) as exc_info:
            LineSymbol(enabled=False)

        error = exc_info.value.errors()[0]
        assert error["type"] == "value_error"
        assert "cannot be False" in str(error["ctx"]["error"])

    def test_line_symbol_from_dict_enabled_false_raises_error(self):
        """Test that creating from dict with enabled=False raises error."""
        with pytest.raises(ValidationError) as exc_info:
            LineSymbol.model_validate({"enabled": False, "shape": "circle"})

        error = exc_info.value.errors()[0]
        assert error["type"] == "value_error"
        assert "cannot be False" in str(error["ctx"]["error"])


class TestLineValueLabelValidation:
    """Test LineValueLabel validation."""

    def test_line_value_label_enabled_defaults_to_true(self):
        """Test that LineValueLabel.enabled defaults to True."""
        label = LineValueLabel()
        assert label.enabled is True

    def test_line_value_label_enabled_true_is_valid(self):
        """Test that explicitly setting enabled=True is valid."""
        label = LineValueLabel(enabled=True, last=True)
        assert label.enabled is True
        assert label.last is True

    def test_line_value_label_enabled_false_raises_error(self):
        """Test that setting enabled=False raises a validation error."""
        with pytest.raises(ValidationError) as exc_info:
            LineValueLabel(enabled=False)

        error = exc_info.value.errors()[0]
        assert error["type"] == "value_error"
        assert "cannot be False" in str(error["ctx"]["error"])

    def test_line_value_label_from_dict_enabled_false_raises_error(self):
        """Test that creating from dict with enabled=False raises error."""
        with pytest.raises(ValidationError) as exc_info:
            LineValueLabel.model_validate({"enabled": False, "last": True})

        error = exc_info.value.errors()[0]
        assert error["type"] == "value_error"
        assert "cannot be False" in str(error["ctx"]["error"])


class TestLineOptionalFields:
    """Test Line model with optional symbols and value_labels."""

    def test_line_symbols_defaults_to_none(self):
        """Test that Line.symbols defaults to None."""
        line = Line(column="sales")
        assert line.symbols is None

    def test_line_value_labels_defaults_to_none(self):
        """Test that Line.value_labels defaults to None."""
        line = Line(column="sales")
        assert line.value_labels is None

    def test_line_with_symbols_object(self):
        """Test creating Line with symbols object."""
        line = Line(column="sales", symbols={"shape": "square", "on": "last"})
        assert line.symbols is not None
        assert line.symbols.enabled is True
        assert line.symbols.shape == "square"

    def test_line_with_value_labels_object(self):
        """Test creating Line with value_labels object."""
        line = Line(column="sales", value_labels={"last": True, "first": False})
        assert line.value_labels is not None
        assert line.value_labels.enabled is True
        assert line.value_labels.last is True

    def test_line_serialize_with_none_symbols(self):
        """Test serializing Line with symbols=None outputs enabled=False."""
        line = Line(column="sales")
        serialized = Line.serialize_model(line)
        assert serialized["symbols"]["enabled"] is False

    def test_line_serialize_with_symbols_object(self):
        """Test serializing Line with symbols object outputs enabled=True."""
        line = Line(column="sales", symbols={"shape": "square"})
        serialized = Line.serialize_model(line)
        assert serialized["symbols"]["enabled"] is True
        assert serialized["symbols"]["shape"] == "square"

    def test_line_serialize_with_none_value_labels(self):
        """Test serializing Line with value_labels=None outputs enabled=False."""
        line = Line(column="sales")
        serialized = Line.serialize_model(line)
        assert serialized["valueLabels"]["enabled"] is False

    def test_line_serialize_with_value_labels_object(self):
        """Test serializing Line with value_labels object outputs enabled=True."""
        line = Line(column="sales", value_labels={"last": True})
        serialized = Line.serialize_model(line)
        assert serialized["valueLabels"]["enabled"] is True
        assert serialized["valueLabels"]["last"] is True

    def test_line_deserialize_with_disabled_symbols(self):
        """Test deserializing Line with symbols.enabled=False returns None."""
        api_config = {"symbols": {"enabled": False}}
        init_dict = Line.deserialize_model("sales", api_config)
        assert init_dict["symbols"] is None

    def test_line_deserialize_with_enabled_symbols(self):
        """Test deserializing Line with symbols.enabled=True creates object."""
        api_config = {"symbols": {"enabled": True, "shape": "square"}}
        init_dict = Line.deserialize_model("sales", api_config)
        assert init_dict["symbols"] is not None
        assert init_dict["symbols"].shape == "square"

    def test_line_deserialize_with_disabled_value_labels(self):
        """Test deserializing Line with valueLabels.enabled=False returns None."""
        api_config = {"valueLabels": {"enabled": False}}
        init_dict = Line.deserialize_model("sales", api_config)
        assert init_dict["value_labels"] is None

    def test_line_deserialize_with_enabled_value_labels(self):
        """Test deserializing Line with valueLabels.enabled=True creates object."""
        api_config = {"valueLabels": {"enabled": True, "last": True}}
        init_dict = Line.deserialize_model("sales", api_config)
        assert init_dict["value_labels"] is not None
        assert init_dict["value_labels"].last is True

    def test_round_trip_with_symbols(self):
        """Test round-trip serialization/deserialization with symbols."""
        # Create line with symbols
        line1 = Line(column="sales", symbols={"shape": "diamond", "on": "both"})

        # Serialize
        serialized = Line.serialize_model(line1)

        # Deserialize
        init_dict = Line.deserialize_model("sales", serialized)
        line2 = Line.model_validate(init_dict)

        # Verify
        assert line2.symbols is not None
        assert line2.symbols.shape == "diamond"
        assert line2.symbols.on == "both"

    def test_round_trip_without_symbols(self):
        """Test round-trip serialization/deserialization without symbols."""
        # Create line without symbols
        line1 = Line(column="sales")

        # Serialize
        serialized = Line.serialize_model(line1)

        # Deserialize
        init_dict = Line.deserialize_model("sales", serialized)
        line2 = Line.model_validate(init_dict)

        # Verify
        assert line2.symbols is None

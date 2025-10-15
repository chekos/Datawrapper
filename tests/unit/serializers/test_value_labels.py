"""Tests for the ValueLabels serializer utility."""

from datawrapper.charts.serializers import ValueLabels


class TestValueLabelsSerialize:
    """Test ValueLabels.serialize() method."""

    def test_serialize_hover_default(self):
        """Test serializing hover mode (default)."""
        result = ValueLabels.serialize(
            show="hover",
            format_str="",
            placement="outside",
            always=False,
            chart_type="column",
        )
        assert result == {
            "valueLabels": {
                "show": "hover",
                "enabled": True,
                "format": "",
                "placement": "outside",
            }
        }

    def test_serialize_always_mode(self):
        """Test serializing always mode."""
        result = ValueLabels.serialize(
            show="always",
            format_str="0,0",
            placement="inside",
            always=True,
            chart_type="column",
        )
        assert result == {
            "valueLabels": {
                "show": "always",
                "enabled": True,
                "format": "0,0",
                "placement": "inside",
            },
            "value-label-format": "0,0",
            "value-labels-always": True,
        }

    def test_serialize_off_mode(self):
        """Test serializing off mode."""
        result = ValueLabels.serialize(
            show="off",
            format_str="",
            placement="outside",
            always=False,
            chart_type="column",
        )
        assert result == {
            "valueLabels": {
                "show": "",
                "enabled": False,
                "format": "",
                "placement": "outside",
            }
        }

    def test_serialize_multiple_column_chart(self):
        """Test serializing for multiple-column chart type."""
        result = ValueLabels.serialize(
            show="always",
            format_str="0.0a",
            placement="below",
            always=True,
            chart_type="multiple-column",
        )
        assert result == {
            "valueLabels": {
                "show": "always",
                "enabled": True,
                "format": "0.0a",
                "placement": "below",
            },
            "value-label-format": "0.0a",
            "value-labels-always": True,
        }

    def test_serialize_with_custom_format(self):
        """Test serializing with custom number format."""
        result = ValueLabels.serialize(
            show="hover",
            format_str="$0,0.00",
            placement="outside",
            always=False,
            chart_type="column",
        )
        assert result == {
            "valueLabels": {
                "show": "hover",
                "enabled": True,
                "format": "$0,0.00",
                "placement": "outside",
            },
            "value-label-format": "$0,0.00",
        }


class TestValueLabelsDeserialize:
    """Test ValueLabels.deserialize() method."""

    def test_deserialize_hover_mode(self):
        """Test deserializing hover mode."""
        visualize = {
            "valueLabels": {
                "enabled": True,
                "format": "",
                "placement": "outside",
            }
        }
        result = ValueLabels.deserialize(visualize, chart_type="column")
        assert result == {
            "show_value_labels": "hover",
            "value_labels_format": "",
            "value_labels_placement": "outside",
            "value_labels_always": False,
        }

    def test_deserialize_always_mode(self):
        """Test deserializing always mode."""
        visualize = {
            "valueLabels": {
                "enabled": True,
                "format": "0,0",
                "placement": "inside",
            },
            "value-labels-always": True,
        }
        result = ValueLabels.deserialize(visualize, chart_type="column")
        assert result == {
            "show_value_labels": "always",
            "value_labels_format": "0,0",
            "value_labels_placement": "inside",
            "value_labels_always": True,
        }

    def test_deserialize_off_mode(self):
        """Test deserializing off mode."""
        visualize = {
            "valueLabels": {
                "enabled": False,
                "format": "",
                "placement": "outside",
            }
        }
        result = ValueLabels.deserialize(visualize, chart_type="column")
        assert result == {
            "show_value_labels": "off",
            "value_labels_format": "",
            "value_labels_placement": "outside",
            "value_labels_always": False,
        }

    def test_deserialize_multiple_column_chart(self):
        """Test deserializing for multiple-column chart type."""
        visualize = {
            "valueLabels": {
                "enabled": True,
                "format": "0.0a",
                "placement": "below",
            },
            "value-labels-always": True,
        }
        result = ValueLabels.deserialize(visualize, chart_type="multiple-column")
        assert result == {
            "show_value_labels": "always",
            "value_labels_format": "0.0a",
            "value_labels_placement": "below",
            "value_labels_always": True,
        }

    def test_deserialize_missing_value_labels_object(self):
        """Test deserializing when valueLabels object is missing."""
        visualize = {}
        result = ValueLabels.deserialize(visualize, chart_type="column")
        assert result == {
            "show_value_labels": "hover",
            "value_labels_format": "",
            "value_labels_placement": "outside",
            "value_labels_always": False,
        }

    def test_deserialize_with_custom_format(self):
        """Test deserializing with custom number format."""
        visualize = {
            "valueLabels": {
                "enabled": True,
                "format": "$0,0.00",
                "placement": "outside",
            }
        }
        result = ValueLabels.deserialize(visualize, chart_type="column")
        assert result == {
            "show_value_labels": "hover",
            "value_labels_format": "$0,0.00",
            "value_labels_placement": "outside",
            "value_labels_always": False,
        }


class TestValueLabelsRoundTrip:
    """Test round-trip serialization/deserialization."""

    def test_round_trip_hover_mode(self):
        """Test round-trip for hover mode."""
        original = {
            "show": "hover",
            "format_str": "0,0",
            "placement": "outside",
            "always": False,
        }
        serialized = ValueLabels.serialize(
            show=original["show"],
            format_str=original["format_str"],
            placement=original["placement"],
            always=original["always"],
            chart_type="column",
        )
        deserialized = ValueLabels.deserialize(serialized, chart_type="column")

        assert deserialized["show_value_labels"] == original["show"]
        assert deserialized["value_labels_format"] == original["format_str"]
        assert deserialized["value_labels_placement"] == original["placement"]
        assert deserialized["value_labels_always"] == original["always"]

    def test_round_trip_always_mode(self):
        """Test round-trip for always mode."""
        original = {
            "show": "always",
            "format_str": "$0.00",
            "placement": "inside",
            "always": True,
        }
        serialized = ValueLabels.serialize(
            show=original["show"],
            format_str=original["format_str"],
            placement=original["placement"],
            always=original["always"],
            chart_type="column",
        )
        deserialized = ValueLabels.deserialize(serialized, chart_type="column")

        assert deserialized["show_value_labels"] == original["show"]
        assert deserialized["value_labels_format"] == original["format_str"]
        assert deserialized["value_labels_placement"] == original["placement"]
        assert deserialized["value_labels_always"] == original["always"]

    def test_round_trip_off_mode(self):
        """Test round-trip for off mode."""
        original = {
            "show": "off",
            "format_str": "",
            "placement": "outside",
            "always": False,
        }
        serialized = ValueLabels.serialize(
            show=original["show"],
            format_str=original["format_str"],
            placement=original["placement"],
            always=original["always"],
            chart_type="column",
        )
        deserialized = ValueLabels.deserialize(serialized, chart_type="column")

        assert deserialized["show_value_labels"] == original["show"]
        assert deserialized["value_labels_format"] == original["format_str"]
        assert deserialized["value_labels_placement"] == original["placement"]
        assert deserialized["value_labels_always"] == original["always"]

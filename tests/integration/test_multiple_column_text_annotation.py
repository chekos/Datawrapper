"""Integration tests for MultipleColumnTextAnnotation class."""

import pytest
from pydantic import ValidationError

from datawrapper.charts.multiple_column import (
    MultipleColumnChart,
    MultipleColumnTextAnnotation,
)


class TestMultipleColumnTextAnnotationSerialization:
    """Test serialization of MultipleColumnTextAnnotation."""

    def test_serialize_with_plot_field(self):
        """Test that plot field is serialized inside position object."""
        anno = MultipleColumnTextAnnotation(
            text="Test annotation",
            x="2020-01-01",
            y=100,
            plot="Mumbai (Bombay)",
        )

        result = anno.serialize_model()

        assert "position" in result
        assert result["position"]["x"] == "2020-01-01"
        assert result["position"]["y"] == 100
        assert result["position"]["plot"] == "Mumbai (Bombay)"

    def test_serialize_without_plot_field(self):
        """Test that plot field is omitted when None."""
        anno = MultipleColumnTextAnnotation(
            text="Test annotation",
            x="2020-01-01",
            y=100,
        )

        result = anno.serialize_model()

        assert "position" in result
        assert result["position"]["x"] == "2020-01-01"
        assert result["position"]["y"] == 100
        assert "plot" not in result["position"]

    def test_serialize_show_in_all_plots_true(self):
        """Test that showInAllPlots is serialized at top level when True."""
        anno = MultipleColumnTextAnnotation(
            text="Test annotation",
            x="2020-01-01",
            y=100,
            show_in_all_plots=True,
        )

        result = anno.serialize_model()

        assert result["showInAllPlots"] is True

    def test_serialize_show_in_all_plots_false(self):
        """Test that showInAllPlots is serialized at top level when False."""
        anno = MultipleColumnTextAnnotation(
            text="Test annotation",
            x="2020-01-01",
            y=100,
            show_in_all_plots=False,
        )

        result = anno.serialize_model()

        assert result["showInAllPlots"] is False

    def test_serialize_show_in_all_plots_default(self):
        """Test that showInAllPlots defaults to False."""
        anno = MultipleColumnTextAnnotation(
            text="Test annotation",
            x="2020-01-01",
            y=100,
        )

        result = anno.serialize_model()

        assert result["showInAllPlots"] is False

    def test_serialize_with_all_multi_panel_fields(self):
        """Test serialization with both plot and showInAllPlots."""
        anno = MultipleColumnTextAnnotation(
            text="Test annotation",
            x="2020-01-01",
            y=100,
            plot="Delhi",
            show_in_all_plots=True,
        )

        result = anno.serialize_model()

        assert result["position"]["plot"] == "Delhi"
        assert result["showInAllPlots"] is True

    def test_serialize_inherits_base_fields(self):
        """Test that base TextAnnotation fields are still serialized."""
        anno = MultipleColumnTextAnnotation(
            text="Test annotation",
            x="2020-01-01",
            y=100,
            plot="Paris",
            bold=True,
            size=16,
            color="#FF0000",
        )

        result = anno.serialize_model()

        assert result["text"] == "Test annotation"
        assert result["bold"] is True
        assert result["size"] == 16
        assert result["color"] == "#FF0000"
        assert result["position"]["plot"] == "Paris"


class TestMultipleColumnTextAnnotationDeserialization:
    """Test deserialization of MultipleColumnTextAnnotation."""

    def test_deserialize_with_plot_field(self):
        """Test deserialization extracts plot from position object."""
        api_data = {
            "anno123": {
                "text": "Test annotation",
                "position": {
                    "x": "2020-01-01",
                    "y": 100,
                    "plot": "Mumbai (Bombay)",
                },
                "showInAllPlots": False,
            }
        }

        result = MultipleColumnTextAnnotation.deserialize_model(api_data)

        assert len(result) == 1
        assert result[0]["id"] == "anno123"
        assert result[0]["plot"] == "Mumbai (Bombay)"
        assert result[0]["show_in_all_plots"] is False

    def test_deserialize_without_plot_field(self):
        """Test deserialization when plot field is missing."""
        api_data = {
            "anno123": {
                "text": "Test annotation",
                "position": {"x": "2020-01-01", "y": 100},
                "showInAllPlots": False,
            }
        }

        result = MultipleColumnTextAnnotation.deserialize_model(api_data)

        assert len(result) == 1
        assert result[0]["id"] == "anno123"
        assert "plot" not in result[0]
        assert result[0]["show_in_all_plots"] is False

    def test_deserialize_show_in_all_plots_true(self):
        """Test deserialization of showInAllPlots when True."""
        api_data = {
            "anno123": {
                "text": "Test annotation",
                "position": {"x": "2020-01-01", "y": 100},
                "showInAllPlots": True,
            }
        }

        result = MultipleColumnTextAnnotation.deserialize_model(api_data)

        assert len(result) == 1
        assert result[0]["show_in_all_plots"] is True

    def test_deserialize_show_in_all_plots_false(self):
        """Test deserialization of showInAllPlots when False."""
        api_data = {
            "anno123": {
                "text": "Test annotation",
                "position": {"x": "2020-01-01", "y": 100},
                "showInAllPlots": False,
            }
        }

        result = MultipleColumnTextAnnotation.deserialize_model(api_data)

        assert len(result) == 1
        assert result[0]["show_in_all_plots"] is False

    def test_deserialize_show_in_all_plots_default(self):
        """Test that showInAllPlots defaults to False when missing."""
        api_data = {
            "anno123": {
                "text": "Test annotation",
                "position": {"x": "2020-01-01", "y": 100},
            }
        }

        result = MultipleColumnTextAnnotation.deserialize_model(api_data)

        assert len(result) == 1
        assert result[0]["show_in_all_plots"] is False

    def test_deserialize_multiple_annotations(self):
        """Test deserialization of multiple annotations."""
        api_data = {
            "anno1": {
                "text": "First annotation",
                "position": {"x": "2020-01-01", "y": 100, "plot": "Delhi"},
                "showInAllPlots": False,
            },
            "anno2": {
                "text": "Second annotation",
                "position": {"x": "2021-01-01", "y": 200, "plot": "Paris"},
                "showInAllPlots": True,
            },
        }

        result = MultipleColumnTextAnnotation.deserialize_model(api_data)

        assert len(result) == 2
        assert result[0]["id"] == "anno1"
        assert result[0]["plot"] == "Delhi"
        assert result[0]["show_in_all_plots"] is False
        assert result[1]["id"] == "anno2"
        assert result[1]["plot"] == "Paris"
        assert result[1]["show_in_all_plots"] is True

    def test_deserialize_empty_data(self):
        """Test deserialization with None or empty dict."""
        assert MultipleColumnTextAnnotation.deserialize_model(None) == []
        assert MultipleColumnTextAnnotation.deserialize_model({}) == []

    def test_deserialize_preserves_base_fields(self):
        """Test that base TextAnnotation fields are preserved."""
        api_data = {
            "anno123": {
                "text": "Test annotation",
                "position": {"x": "2020-01-01", "y": 100, "plot": "Paris"},
                "showInAllPlots": False,
                "bold": True,
                "size": 16,
                "color": "#FF0000",
                "bg": True,
            }
        }

        result = MultipleColumnTextAnnotation.deserialize_model(api_data)

        assert len(result) == 1
        assert result[0]["text"] == "Test annotation"
        assert result[0]["bold"] is True
        assert result[0]["size"] == 16
        assert result[0]["color"] == "#FF0000"
        assert result[0]["bg"] is True


class TestMultipleColumnTextAnnotationRoundTrip:
    """Test round-trip serialization/deserialization."""

    def test_roundtrip_with_plot(self):
        """Test that annotation survives serialization and deserialization."""
        original = MultipleColumnTextAnnotation(
            text="Test annotation",
            x="2020-01-01",
            y=100,
            plot="Mumbai (Bombay)",
            show_in_all_plots=False,
        )

        # Serialize
        serialized = original.serialize_model()

        # Simulate API response format
        api_data = {"test_id": serialized}

        # Deserialize
        deserialized_list = MultipleColumnTextAnnotation.deserialize_model(api_data)
        deserialized_dict = deserialized_list[0]

        # Create new instance from deserialized data
        reconstructed = MultipleColumnTextAnnotation(**deserialized_dict)

        # Verify fields match
        assert reconstructed.text == original.text
        assert reconstructed.x == original.x
        assert reconstructed.y == original.y
        assert reconstructed.plot == original.plot
        assert reconstructed.show_in_all_plots == original.show_in_all_plots

    def test_roundtrip_without_plot(self):
        """Test round-trip without plot field."""
        original = MultipleColumnTextAnnotation(
            text="Test annotation",
            x="2020-01-01",
            y=100,
            show_in_all_plots=True,
        )

        serialized = original.serialize_model()
        api_data = {"test_id": serialized}
        deserialized_list = MultipleColumnTextAnnotation.deserialize_model(api_data)
        reconstructed = MultipleColumnTextAnnotation(**deserialized_list[0])

        assert reconstructed.text == original.text
        assert reconstructed.x == original.x
        assert reconstructed.y == original.y
        assert reconstructed.plot is None
        assert reconstructed.show_in_all_plots == original.show_in_all_plots


class TestMultipleColumnChartIntegration:
    """Test MultipleColumnTextAnnotation integration with MultipleColumnChart."""

    def test_chart_uses_multiple_column_text_annotation(self):
        """Test that MultipleColumnChart uses MultipleColumnTextAnnotation for serialization."""
        chart = MultipleColumnChart(
            title="Test Chart",
            text_annotations=[
                {
                    "text": "Test annotation",
                    "x": "2020-01-01",
                    "y": 100,
                    "plot": "Delhi",
                    "show_in_all_plots": False,
                }
            ],
        )

        serialized = chart.serialize_model()
        text_annos = serialized["metadata"]["visualize"]["text-annotations"]

        # Should have one annotation in list format (matching LineChart pattern)
        assert len(text_annos) == 1
        anno_data = text_annos[0]

        # Verify multi-panel fields are present
        assert anno_data["position"]["plot"] == "Delhi"
        assert anno_data["showInAllPlots"] is False

    def test_chart_deserializes_with_multiple_column_text_annotation(self):
        """Test that MultipleColumnChart deserializes text annotations correctly."""
        api_response = {
            "id": "test123",
            "type": "multiple-columns",
            "title": "Test Chart",
            "metadata": {
                "visualize": {
                    "text-annotations": {
                        "anno1": {
                            "text": "Test annotation",
                            "position": {
                                "x": "2020-01-01",
                                "y": 100,
                                "plot": "Mumbai (Bombay)",
                            },
                            "showInAllPlots": False,
                            "bg": True,
                            "bold": False,
                            "size": 14,
                            "align": "tl",
                            "color": False,
                            "width": 33.3,
                            "italic": False,
                            "underline": False,
                            "showMobile": True,
                            "showDesktop": True,
                            "mobileFallback": False,
                            "connectorLine": {"enabled": False},
                            "dx": 0,
                            "dy": 0,
                        }
                    }
                }
            },
        }

        init_data = MultipleColumnChart.deserialize_model(api_response)

        assert "text_annotations" in init_data
        assert len(init_data["text_annotations"]) == 1
        anno = init_data["text_annotations"][0]
        assert anno["text"] == "Test annotation"
        assert anno["plot"] == "Mumbai (Bombay)"
        assert anno["show_in_all_plots"] is False


class TestMultipleColumnTextAnnotationValidation:
    """Test validation of MultipleColumnTextAnnotation."""

    def test_requires_text_field(self):
        """Test that text field is required."""
        with pytest.raises(ValidationError):
            MultipleColumnTextAnnotation(x="2020-01-01", y=100)

    def test_requires_x_and_y_fields(self):
        """Test that x and y fields are required."""
        with pytest.raises(ValidationError):
            MultipleColumnTextAnnotation(text="Test")

    def test_plot_field_optional(self):
        """Test that plot field is optional."""
        anno = MultipleColumnTextAnnotation(
            text="Test annotation", x="2020-01-01", y=100
        )
        assert anno.plot is None

    def test_show_in_all_plots_defaults_to_false(self):
        """Test that show_in_all_plots defaults to False."""
        anno = MultipleColumnTextAnnotation(
            text="Test annotation", x="2020-01-01", y=100
        )
        assert anno.show_in_all_plots is False

    def test_accepts_alias_for_show_in_all_plots(self):
        """Test that showInAllPlots alias works."""
        anno = MultipleColumnTextAnnotation(
            text="Test annotation",
            x="2020-01-01",
            y=100,
            showInAllPlots=True,  # Using alias
        )
        assert anno.show_in_all_plots is True

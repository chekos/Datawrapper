"""Integration tests for MultipleColumnChart."""

import json
from pathlib import Path
from unittest.mock import Mock, patch

import pandas as pd

from datawrapper import MultipleColumnChart


# Helper functions to load sample data
def load_sample_json(filename: str) -> dict:
    """Load a sample JSON file from tests/samples/multiple_column/."""
    path = Path(__file__).parent.parent / "samples" / "multiple_column" / filename
    with open(path) as f:
        data = json.load(f)
    return data["chart"]["crdt"]["data"]


def load_sample_csv(filename: str) -> str:
    """Load a sample CSV file from tests/samples/multiple_column/."""
    path = Path(__file__).parent.parent / "samples" / "multiple_column" / filename
    with open(path) as f:
        return f.read()


class TestMultipleColumnChartCreation:
    """Tests for creating MultipleColumnChart instances."""

    def test_create_basic_chart(self):
        """Test creating a basic multiple column chart."""
        data = pd.DataFrame(
            {
                "Year": [2020, 2021, 2022, 2023],
                "North": [100, 110, 120, 130],
                "South": [90, 95, 100, 105],
            }
        )

        chart = MultipleColumnChart(
            title="Regional Sales",
            data=data,
        )

        assert chart.chart_type == "multiple-columns"
        assert chart.title == "Regional Sales"
        assert chart.grid_column == 2
        assert chart.grid_row_height == 140

    def test_create_with_layout_options(self):
        """Test creating chart with layout customization."""
        data = pd.DataFrame({"Year": [2020, 2021], "Value": [100, 110]})

        chart = MultipleColumnChart(
            title="Test Chart",
            data=data,
            grid_layout="minimumWidth",
            grid_column=3,
            grid_column_mobile=1,
            grid_column_width=250,
            grid_row_height=160,
        )

        assert chart.grid_layout == "minimumWidth"
        assert chart.grid_column == 3
        assert chart.grid_column_mobile == 1
        assert chart.grid_column_width == 250
        assert chart.grid_row_height == 160

    def test_create_with_sorting(self):
        """Test creating chart with sorting options."""
        data = pd.DataFrame({"Year": [2020, 2021], "Value": [100, 110]})

        chart = MultipleColumnChart(
            title="Sorted Chart",
            data=data,
            sort=True,
            sort_reverse=True,
            sort_by="start",
        )

        assert chart.sort is True
        assert chart.sort_reverse is True
        assert chart.sort_by == "start"

    def test_create_with_axes_customization(self):
        """Test creating chart with custom axes."""
        data = pd.DataFrame({"Year": [2020, 2021], "Value": [100, 110]})

        chart = MultipleColumnChart(
            title="Custom Axes",
            data=data,
            custom_range_x=[0, 100],
            custom_ticks_x=[0, 25, 50, 75, 100],
            x_grid="ticks",
            x_grid_format="0,0",
            custom_range_y=[0, 200],
            y_grid_format="0.[0]a",
            y_grid_labels="inside",
            y_grid_label_align="right",
        )

        assert chart.custom_range_x == [0, 100]
        assert chart.custom_ticks_x == [0, 25, 50, 75, 100]
        assert chart.x_grid == "ticks"
        assert chart.y_grid_labels == "inside"
        assert chart.y_grid_label_align == "right"

    def test_create_with_colors(self):
        """Test creating chart with color customization."""
        data = pd.DataFrame({"Year": [2020, 2021], "Value": [100, 110]})

        chart = MultipleColumnChart(
            title="Colored Chart",
            data=data,
            base_color="#FF5733",
            negative_color="#C70039",
            color_category={"Series A": "#FF5733", "Series B": "#C70039"},
        )

        assert chart.base_color == "#FF5733"
        assert chart.negative_color == "#C70039"
        assert chart.color_category == {"Series A": "#FF5733", "Series B": "#C70039"}

    def test_create_with_labels(self):
        """Test creating chart with label customization."""
        data = pd.DataFrame({"Year": [2020, 2021], "Value": [100, 110]})

        chart = MultipleColumnChart(
            title="Labeled Chart",
            data=data,
            show_value_labels="always",
            value_labels_placement="inside",
            value_labels_format="0,0",
            label_colors=True,
            show_color_key=True,
        )

        assert chart.show_value_labels == "always"
        assert chart.value_labels_placement == "inside"
        assert chart.value_labels_format == "0,0"
        assert chart.label_colors is True
        assert chart.show_color_key is True


class TestMultipleColumnChartSerialization:
    """Tests for serializing MultipleColumnChart to API format."""

    def test_serialize_basic_chart(self):
        """Test serializing a basic chart."""
        data = pd.DataFrame({"Year": [2020, 2021], "Value": [100, 110]})
        chart = MultipleColumnChart(title="Test", data=data)

        serialized = chart.model_dump(by_alias=True)

        assert serialized["type"] == "multiple-columns"
        assert serialized["title"] == "Test"
        assert "metadata" in serialized
        assert "visualize" in serialized["metadata"]

    def test_serialize_layout_fields(self):
        """Test that layout fields are serialized correctly."""
        data = pd.DataFrame({"Year": [2020, 2021], "Value": [100, 110]})
        chart = MultipleColumnChart(
            title="Test",
            data=data,
            grid_layout="minimumWidth",
            grid_column=3,
            grid_column_mobile=2,
            grid_column_width=250,
            grid_row_height=150,
        )

        serialized = chart.model_dump(by_alias=True)
        viz = serialized["metadata"]["visualize"]

        assert viz["gridLayout"] == "minimumWidth"
        assert viz["gridColumnCount"] == 3
        assert viz["gridColumnCountMobile"] == 2
        assert viz["gridColumnMinWidth"] == 250
        assert viz["gridRowHeightFixed"] == 150

    def test_serialize_sort_object(self):
        """Test that sort object is serialized correctly."""
        data = pd.DataFrame({"Year": [2020, 2021], "Value": [100, 110]})
        chart = MultipleColumnChart(
            title="Test",
            data=data,
            sort=True,
            sort_reverse=True,
            sort_by="range",
        )

        serialized = chart.model_dump(by_alias=True)
        sort_obj = serialized["metadata"]["visualize"]["sort"]

        assert sort_obj["enabled"] is True
        assert sort_obj["reverse"] is True
        assert sort_obj["by"] == "range"

    def test_serialize_custom_ticks(self):
        """Test that custom ticks are converted to comma-separated strings."""
        data = pd.DataFrame({"Year": [2020, 2021], "Value": [100, 110]})
        chart = MultipleColumnChart(
            title="Test",
            data=data,
            custom_ticks_x=[0, 50, 100],
            custom_ticks_y=[10, 20, 30],
        )

        serialized = chart.model_dump(by_alias=True)
        viz = serialized["metadata"]["visualize"]

        assert viz["custom-ticks-x"] == "0,50,100"
        assert viz["custom-ticks-y"] == "10,20,30"

    def test_serialize_grid_lines_x(self):
        """Test that grid-lines-x is serialized correctly."""
        data = pd.DataFrame({"Year": [2020, 2021], "Value": [100, 110]})

        # Test with x_grid off
        chart_off = MultipleColumnChart(title="Test", data=data, x_grid="off")
        serialized_off = chart_off.model_dump(by_alias=True)
        grid_lines_x_off = serialized_off["metadata"]["visualize"]["grid-lines-x"]

        assert grid_lines_x_off["enabled"] is False
        assert grid_lines_x_off["type"] == ""

        # Test with x_grid on
        chart_on = MultipleColumnChart(title="Test", data=data, x_grid="ticks")
        serialized_on = chart_on.model_dump(by_alias=True)
        grid_lines_x_on = serialized_on["metadata"]["visualize"]["grid-lines-x"]

        assert grid_lines_x_on["enabled"] is True
        assert grid_lines_x_on["type"] == "ticks"

    def test_serialize_y_axis_labels(self):
        """Test that yAxisLabels is serialized correctly."""
        data = pd.DataFrame({"Year": [2020, 2021], "Value": [100, 110]})

        # Test with labels on
        chart_on = MultipleColumnChart(
            title="Test",
            data=data,
            y_grid_labels="inside",
            y_grid_label_align="right",
        )
        serialized_on = chart_on.model_dump(by_alias=True)
        y_labels_on = serialized_on["metadata"]["visualize"]["yAxisLabels"]

        assert y_labels_on["enabled"] is True
        assert y_labels_on["placement"] == "inside"
        assert y_labels_on["alignment"] == "right"

        # Test with labels off
        chart_off = MultipleColumnChart(title="Test", data=data, y_grid_labels="off")
        serialized_off = chart_off.model_dump(by_alias=True)
        y_labels_off = serialized_off["metadata"]["visualize"]["yAxisLabels"]

        assert y_labels_off["enabled"] is False
        assert y_labels_off["placement"] == ""

    def test_serialize_negative_color(self):
        """Test that negativeColor is serialized correctly."""
        data = pd.DataFrame({"Year": [2020, 2021], "Value": [100, 110]})

        # Test with negative color enabled
        chart_enabled = MultipleColumnChart(
            title="Test", data=data, negative_color="#FF0000"
        )
        serialized_enabled = chart_enabled.model_dump(by_alias=True)
        neg_color_enabled = serialized_enabled["metadata"]["visualize"]["negativeColor"]

        assert neg_color_enabled["enabled"] is True
        assert neg_color_enabled["value"] == "#FF0000"

        # Test with negative color disabled
        chart_disabled = MultipleColumnChart(
            title="Test", data=data, negative_color=None
        )
        serialized_disabled = chart_disabled.model_dump(by_alias=True)
        neg_color_disabled = serialized_disabled["metadata"]["visualize"][
            "negativeColor"
        ]

        assert neg_color_disabled["enabled"] is False

    def test_serialize_color_category(self):
        """Test that color-category is serialized correctly."""
        data = pd.DataFrame({"Year": [2020, 2021], "Value": [100, 110]})
        chart = MultipleColumnChart(
            title="Test",
            data=data,
            color_category={"Series A": "#FF0000", "Series B": "#00FF00"},
        )

        serialized = chart.model_dump(by_alias=True)
        viz = serialized["metadata"]["visualize"]

        assert viz["color-category"]["map"] == {
            "Series A": "#FF0000",
            "Series B": "#00FF00",
        }
        assert viz["color-by-column"] is True

    def test_serialize_panels(self):
        """Test that panels list is converted to dict."""
        data = pd.DataFrame({"Year": [2020, 2021], "Value": [100, 110]})
        chart = MultipleColumnChart(
            title="Test",
            data=data,
            panels=[
                {"column": "Series A", "config": "value1"},
                {"column": "Series B", "config": "value2"},
            ],
        )

        serialized = chart.model_dump(by_alias=True)
        panels = serialized["metadata"]["visualize"]["panels"]

        assert isinstance(panels, dict)
        assert "Series A" in panels
        assert "Series B" in panels
        assert panels["Series A"]["config"] == "value1"

    def test_serialize_value_labels(self):
        """Test that valueLabels is serialized correctly."""
        data = pd.DataFrame({"Year": [2020, 2021], "Value": [100, 110]})

        # Test with value labels always on
        chart_always = MultipleColumnChart(
            title="Test",
            data=data,
            show_value_labels="always",
            value_labels_format="0,0",
            value_labels_placement="inside",
        )
        serialized_always = chart_always.model_dump(by_alias=True)
        val_labels_always = serialized_always["metadata"]["visualize"]["valueLabels"]

        assert val_labels_always["show"] == "always"
        assert val_labels_always["format"] == "0,0"
        assert val_labels_always["enabled"] is True
        assert val_labels_always["placement"] == "inside"
        # When always is True, value-labels-always should be present and True
        assert (
            serialized_always["metadata"]["visualize"].get("value-labels-always")
            is True
        )

        # Test with value labels on hover (default)
        chart_hover = MultipleColumnChart(
            title="Test",
            data=data,
            show_value_labels="hover",
            value_labels_format="0.0a",
        )
        serialized_hover = chart_hover.model_dump(by_alias=True)
        val_labels_hover = serialized_hover["metadata"]["visualize"]["valueLabels"]

        assert val_labels_hover["show"] == "hover"
        assert val_labels_hover["format"] == "0.0a"
        assert val_labels_hover["enabled"] is True
        assert val_labels_hover["placement"] == "outside"
        # When hover, value-labels-always should not be present (or False)
        assert (
            serialized_hover["metadata"]["visualize"].get("value-labels-always", False)
            is False
        )

        # Test with value labels off
        chart_off = MultipleColumnChart(
            title="Test", data=data, show_value_labels="off"
        )
        serialized_off = chart_off.model_dump(by_alias=True)
        val_labels_off = serialized_off["metadata"]["visualize"]["valueLabels"]

        assert val_labels_off["show"] == ""
        assert val_labels_off["enabled"] is False
        assert val_labels_off["placement"] == "outside"


class TestMultipleColumnChartParsing:
    """Tests for parsing API responses into MultipleColumnChart."""

    def test_parse_jobs_sample(self):
        """Test parsing the jobs.json sample."""
        chart_metadata = load_sample_json("jobs.json")
        sample_csv = load_sample_csv("jobs.csv")

        mock_client = Mock()
        mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"

        def mock_get(url):
            if url.endswith("/data"):
                return sample_csv
            return chart_metadata

        mock_client.get.side_effect = mock_get

        with patch("datawrapper.charts.base.Datawrapper", return_value=mock_client):
            chart = MultipleColumnChart.get("test-id", access_token="test-token")

            assert chart.chart_type == "multiple-columns"
            assert (
                chart.title == "Manufacturing construction has seen the highest growth"
            )
            assert chart.grid_layout == "fixedCount"
            assert chart.grid_column == 3
            assert chart.grid_column_mobile == 3
            assert chart.grid_row_height == 122
            assert chart.base_color == "#809cae"
            assert chart.bar_padding == 26
            assert chart.y_grid_format == "0.[0]a"
            assert chart.y_grid_labels == "off"
            assert chart.show_color_key is True
            assert "Manufacturing" in chart.color_category
            assert chart.color_category["Manufacturing"] == "#2d1780"

    def test_parse_population_sample(self):
        """Test parsing the population.json sample."""
        chart_metadata = load_sample_json("population.json")
        sample_csv = load_sample_csv("population.csv")

        mock_client = Mock()
        mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"

        def mock_get(url):
            if url.endswith("/data"):
                return sample_csv
            return chart_metadata

        mock_client.get.side_effect = mock_get

        with patch("datawrapper.charts.base.Datawrapper", return_value=mock_client):
            chart = MultipleColumnChart.get("test-id", access_token="test-token")

            assert chart.chart_type == "multiple-columns"
            assert "population" in chart.title.lower()
            assert chart.grid_layout == "fixedCount"

    def test_parse_social_media_sample(self):
        """Test parsing the social-media.json sample."""
        chart_metadata = load_sample_json("social-media.json")
        sample_csv = load_sample_csv("social-media.csv")

        mock_client = Mock()
        mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"

        def mock_get(url):
            if url.endswith("/data"):
                return sample_csv
            return chart_metadata

        mock_client.get.side_effect = mock_get

        with patch("datawrapper.charts.base.Datawrapper", return_value=mock_client):
            chart = MultipleColumnChart.get("test-id", access_token="test-token")

            assert chart.chart_type == "multiple-columns"
            assert chart.grid_layout == "fixedCount"

    def test_parse_uk_spending_sample(self):
        """Test parsing the uk-spending.json sample."""
        chart_metadata = load_sample_json("uk-spending.json")
        sample_csv = load_sample_csv("uk-spending.csv")

        mock_client = Mock()
        mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"

        def mock_get(url):
            if url.endswith("/data"):
                return sample_csv
            return chart_metadata

        mock_client.get.side_effect = mock_get

        with patch("datawrapper.charts.base.Datawrapper", return_value=mock_client):
            chart = MultipleColumnChart.get("test-id", access_token="test-token")

            assert chart.chart_type == "multiple-columns"
            assert chart.grid_layout == "fixedCount"

    def test_parse_preserves_all_fields(self):
        """Test that parsing preserves all important fields."""
        chart_metadata = load_sample_json("jobs.json")
        sample_csv = load_sample_csv("jobs.csv")

        mock_client = Mock()
        mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"

        def mock_get(url):
            if url.endswith("/data"):
                return sample_csv
            return chart_metadata

        mock_client.get.side_effect = mock_get

        with patch("datawrapper.charts.base.Datawrapper", return_value=mock_client):
            chart = MultipleColumnChart.get("test-id", access_token="test-token")

            # Verify layout fields
            assert isinstance(chart.grid_column, int)
            assert isinstance(chart.grid_column_mobile, int)
            assert isinstance(chart.grid_row_height, int)

            # Verify appearance fields
            assert isinstance(chart.base_color, str)
            assert isinstance(chart.bar_padding, int)

            # Verify label fields
            assert isinstance(chart.show_color_key, bool)
            assert isinstance(chart.label_colors, bool)


class TestMultipleColumnChartRoundTrip:
    """Tests for round-trip serialization and parsing."""

    def test_round_trip_basic_chart(self):
        """Test that a chart can be serialized and parsed back."""
        data = pd.DataFrame({"Year": [2020, 2021], "Value": [100, 110]})

        original = MultipleColumnChart(
            title="Test Chart",
            data=data,
            grid_column=3,
            grid_row_height=150,
            base_color="#FF5733",
        )

        # Serialize
        serialized = original.model_dump(by_alias=True)

        # Parse back (simulating API response)
        chart_metadata = {
            "type": serialized["type"],
            "title": serialized["title"],
            "metadata": serialized["metadata"],
        }

        mock_csv = "Year,Value\n2020,100\n2021,110"

        mock_client = Mock()
        mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"

        def mock_get(url):
            if url.endswith("/data"):
                return mock_csv
            return chart_metadata

        mock_client.get.side_effect = mock_get

        with patch("datawrapper.charts.base.Datawrapper", return_value=mock_client):
            parsed = MultipleColumnChart.get("test-id", access_token="test-token")

            # Verify key fields match
            assert parsed.title == original.title
            assert parsed.chart_type == original.chart_type
            assert parsed.grid_column == original.grid_column
            assert parsed.grid_row_height == original.grid_row_height
            assert parsed.base_color == original.base_color

    def test_round_trip_with_all_options(self):
        """Test round-trip with many options set."""
        data = pd.DataFrame({"Year": [2020, 2021], "Value": [100, 110]})

        original = MultipleColumnChart(
            title="Complex Chart",
            data=data,
            grid_layout="minimumWidth",
            grid_column=4,
            grid_column_mobile=2,
            sort=True,
            sort_by="range",
            custom_range_x=[0, 100],
            custom_ticks_x=[0, 50, 100],
            x_grid="ticks",
            y_grid_labels="inside",
            base_color="#123456",
            negative_color="#654321",
            color_category={"A": "#FF0000", "B": "#00FF00"},
            show_value_labels="always",
            show_color_key=True,
        )

        # Serialize
        serialized = original.model_dump(by_alias=True)

        # Parse back
        chart_metadata = {
            "type": serialized["type"],
            "title": serialized["title"],
            "metadata": serialized["metadata"],
        }

        mock_csv = "Year,Value\n2020,100\n2021,110"

        mock_client = Mock()
        mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"

        def mock_get(url):
            if url.endswith("/data"):
                return mock_csv
            return chart_metadata

        mock_client.get.side_effect = mock_get

        with patch("datawrapper.charts.base.Datawrapper", return_value=mock_client):
            parsed = MultipleColumnChart.get("test-id", access_token="test-token")

            # Verify all fields match
            assert parsed.grid_layout == original.grid_layout
            assert parsed.grid_column == original.grid_column
            assert parsed.grid_column_mobile == original.grid_column_mobile
            assert parsed.sort == original.sort
            assert parsed.sort_by == original.sort_by
            assert parsed.custom_range_x == original.custom_range_x
            assert parsed.custom_ticks_x == original.custom_ticks_x
            assert parsed.x_grid == original.x_grid
            assert parsed.y_grid_labels == original.y_grid_labels
            assert parsed.base_color == original.base_color
            assert parsed.negative_color == original.negative_color
            assert parsed.color_category == original.color_category
            assert parsed.show_value_labels == original.show_value_labels
            assert parsed.show_color_key == original.show_color_key


class TestMultipleColumnChartCompatibility:
    """Tests for compatibility with reuters_data_wire dataclass."""

    def test_metadata_structure_matches(self):
        """Test that serialized metadata structure matches dataclass output."""
        data = pd.DataFrame({"Year": [2020, 2021], "Value": [100, 110]})

        chart = MultipleColumnChart(
            title="Test",
            data=data,
            grid_column=3,
            sort=True,
            sort_by="end",
            custom_ticks_x=[0, 50, 100],
            base_color="#FF0000",
            negative_color="#00FF00",
        )

        serialized = chart.model_dump(by_alias=True)
        viz = serialized["metadata"]["visualize"]

        # Check structure matches expected format
        assert "gridLayout" in viz
        assert "gridColumnCount" in viz
        assert "sort" in viz
        assert isinstance(viz["sort"], dict)
        assert "enabled" in viz["sort"]
        assert "by" in viz["sort"]
        assert "custom-ticks-x" in viz
        assert isinstance(viz["custom-ticks-x"], str)  # Should be comma-separated
        assert "base-color" in viz
        assert "negativeColor" in viz
        assert isinstance(viz["negativeColor"], dict)
        assert "enabled" in viz["negativeColor"]

    def test_can_import_from_main_package(self):
        """Test that MultipleColumnChart can be imported from main package."""
        from datawrapper import MultipleColumnChart as MainImport

        data = pd.DataFrame({"Year": [2020, 2021], "Value": [100, 110]})
        chart = MainImport(title="Test", data=data)

        assert chart.chart_type == "multiple-columns"
        assert chart.title == "Test"

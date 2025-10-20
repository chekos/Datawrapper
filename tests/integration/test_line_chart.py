"""Integration tests for LineChart class."""

import json
from pathlib import Path
from unittest.mock import Mock, patch

import pandas as pd

from datawrapper import LineChart


# Helper to load sample files
def load_sample_json(filename: str) -> dict:
    """Load a sample JSON file from tests/samples/line directory."""
    samples_dir = Path(__file__).parent.parent / "samples" / "line"
    with open(samples_dir / filename) as f:
        return json.load(f)


def load_sample_csv(filename: str) -> str:
    """Load a sample CSV file from tests/samples/line directory."""
    samples_dir = Path(__file__).parent.parent / "samples" / "line"
    with open(samples_dir / filename) as f:
        return f.read()


class TestLineChartCreation:
    """Tests for LineChart creation and serialization."""

    def test_create_basic_line_chart(self):
        """Test creating a basic line chart."""
        chart = LineChart(
            title="Test Line Chart",
            data=pd.DataFrame(
                {"date": ["2020/01", "2020/02"], "Temperature": [15.0, 18.0]}
            ),
        )

        assert chart.chart_type == "d3-lines"
        assert chart.title == "Test Line Chart"
        assert isinstance(chart.data, pd.DataFrame)

    def test_serialize_line_chart(self):
        """Test serializing a line chart."""
        chart = LineChart(
            title="Test Chart",
            data=pd.DataFrame({"date": ["2020/01"], "Value": [10.0]}),
            y_grid="on",
            interpolation="monotone-x",
            connector_lines=True,
        )

        serialized = chart.serialize_model()

        assert serialized["type"] == "d3-lines"
        assert serialized["title"] == "Test Chart"
        assert serialized["metadata"]["visualize"]["y-grid"] == "on"
        assert serialized["metadata"]["visualize"]["interpolation"] == "monotone-x"
        assert serialized["metadata"]["visualize"]["connector-lines"] is True

    def test_serialize_with_custom_ranges(self):
        """Test serializing with custom axis ranges."""
        chart = LineChart(
            title="Test",
            data=pd.DataFrame({"x": [1, 2], "y": [10, 20]}),
            custom_range_x=["2020", "2025"],
            custom_range_y=[0, 100],
        )

        serialized = chart.serialize_model()

        assert serialized["metadata"]["visualize"]["custom-range-x"] == ["2020", "2025"]
        assert serialized["metadata"]["visualize"]["custom-range-y"] == [0, 100]

    def test_serialize_with_line_config(self):
        """Test serializing with individual line configuration."""
        chart = LineChart(
            title="Test",
            data=pd.DataFrame({"x": [1, 2], "y": [10, 20]}),
            lines=[
                {
                    "column": "y",
                    "width": "style3",
                    "dash": "style2",
                    "direct_label": True,
                    "symbols": {"enabled": True, "shape": "square", "on": "last"},
                }
            ],
        )

        serialized = chart.serialize_model()
        line_config = serialized["metadata"]["visualize"]["lines"]["y"]

        assert line_config["width"] == "style3"
        assert line_config["dash"] == "style2"
        assert line_config["directLabel"] is True
        assert line_config["symbols"]["enabled"] is True
        assert line_config["symbols"]["shape"] == "square"

    def test_serialize_with_area_fill(self):
        """Test serializing with area fills."""
        chart = LineChart(
            title="Test",
            data=pd.DataFrame({"x": [1, 2], "baseline": [0, 0], "value": [10, 20]}),
            area_fills=[
                {
                    "from_column": "baseline",
                    "to_column": "value",
                    "color": "#c3e8d5",
                    "opacity": 0.7,
                }
            ],
        )

        serialized = chart.serialize_model()
        area_fills = serialized["metadata"]["visualize"]["custom-area-fills"]

        assert isinstance(area_fills, list)
        assert len(area_fills) == 1
        fill = area_fills[0]
        assert fill["from"] == "baseline"
        assert fill["to"] == "value"
        assert fill["color"] == "#c3e8d5"
        assert fill["opacity"] == 0.7

    def test_serialize_y_axis_scale(self):
        """Test serializing Y-axis scale configuration."""
        chart = LineChart(
            title="Test",
            data=pd.DataFrame({"x": [1, 2], "y": [10, 100]}),
            scale_y="log",
            y_grid_subdivide=False,
        )

        serialized = chart.serialize_model()

        assert serialized["metadata"]["visualize"]["scale-y"] == "log"
        assert serialized["metadata"]["visualize"]["y-grid-subdivide"] is False

    def test_serialize_tooltips(self):
        """Test serializing tooltip configuration."""
        chart = LineChart(
            title="Test",
            data=pd.DataFrame({"x": [1, 2], "y": [10, 20]}),
            show_tooltips=True,
            tooltip_x_format="MMM D",
            tooltip_number_format="0,0.[00]",
        )

        serialized = chart.serialize_model()

        assert serialized["metadata"]["visualize"]["show-tooltips"] is True
        assert serialized["metadata"]["visualize"]["tooltip-x-format"] == "MMM D"
        assert (
            serialized["metadata"]["visualize"]["tooltip-number-format"] == "0,0.[00]"
        )


class TestLineChartGet:
    """Tests for LineChart.get() method."""

    def test_get_covid_sample(self):
        """Test get() with covid.json sample data (complex chart with area fills)."""
        # Load sample data
        sample_json = load_sample_json("covid.json")
        chart_metadata = sample_json["chart"]["crdt"]["data"]
        sample_csv = load_sample_csv("covid.csv")

        mock_client = Mock()
        mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"

        def mock_get(url):
            if url.endswith("/data"):
                return sample_csv
            return chart_metadata

        mock_client.get.side_effect = mock_get

        with patch("datawrapper.charts.base.Datawrapper", return_value=mock_client):
            chart = LineChart.get("rcVbZ", access_token="test-token")

            # Verify chart type and title
            assert chart.chart_type == "d3-lines"
            assert chart.title == "New COVID-19 cases in Berlin"

            # Verify axes configuration
            assert chart.x_grid == "on"
            assert chart.y_grid == "on"
            assert chart.x_grid_format == "MMM|DD"
            assert chart.y_grid_format == "0,0.[00]"
            assert chart.custom_range_x == ["2020-03-01", "2020-07-07"]
            assert chart.custom_range_y == [0, ""]

            # Verify line customization
            assert chart.interpolation == "monotone-x"
            assert chart.connector_lines is True
            assert chart.base_color == 5

            # Verify lines configuration
            new_line = next(
                (line for line in chart.lines if line.column == "new"), None
            )
            assert new_line is not None
            assert new_line.width == "style3"
            assert new_line.direct_label is False

            # Verify area fills
            assert len(chart.area_fills) == 2
            assert chart.area_fills[0].from_column == "new"
            assert chart.area_fills[0].to_column == "baseline"
            assert chart.area_fills[0].color == "#c3e8d5"

            # Verify tooltips
            assert chart.tooltip_number_format == "0,0.[00]"

    def test_get_crypto_sample(self):
        """Test get() with crypto.json sample data (multiple lines with symbols)."""
        # Load sample data
        sample_json = load_sample_json("crypto.json")
        chart_metadata = sample_json["chart"]["crdt"]["data"]
        sample_csv = load_sample_csv("crypto.csv")

        mock_client = Mock()
        mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"

        def mock_get(url):
            if url.endswith("/data"):
                return sample_csv
            return chart_metadata

        mock_client.get.side_effect = mock_get

        with patch("datawrapper.charts.base.Datawrapper", return_value=mock_client):
            chart = LineChart.get("8Fdwv", access_token="test-token")

            # Verify chart type and title
            assert chart.chart_type == "d3-lines"
            assert (
                chart.title
                == "How some of the most popular cryptocurrencies have changed over the last 72 hours"
            )

            # Verify axes
            assert chart.x_grid == "on"
            assert chart.y_grid == "on"
            assert chart.y_grid_format == "+0%"
            assert chart.x_grid_format == "MMM D|h a"

            # Verify line customization
            assert chart.interpolation == "monotone-x"
            assert chart.connector_lines is True
            assert chart.label_colors is True
            assert chart.value_label_colors is True

            # Verify individual line configurations
            btc_line = next(
                (line for line in chart.lines if line.column == "BTC"), None
            )
            assert btc_line is not None
            assert btc_line.width == "style0"
            assert btc_line.direct_label is True
            assert btc_line.symbols.enabled is True
            assert btc_line.symbols.shape == "square"
            assert btc_line.symbols.on == "last"

            # Verify color mapping
            assert "BTC" in chart.color_category
            assert chart.color_category["BTC"] == "#ae000b"

    def test_get_parses_custom_ticks(self):
        """Test get() correctly parses custom ticks from comma-separated strings."""
        mock_metadata = {
            "id": "test-id",
            "type": "d3-lines",
            "title": "Test",
            "metadata": {
                "data": {},
                "describe": {},
                "visualize": {
                    "custom-ticks-x": "2020,2021,2022",
                    "custom-ticks-y": "0,25,50,75,100",
                },
                "publish": {"blocks": {}},
                "annotate": {},
            },
        }

        mock_csv = "x,y\n1,10"

        mock_client = Mock()
        mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"

        def mock_get(url):
            if url.endswith("/data"):
                return mock_csv
            return mock_metadata

        mock_client.get.side_effect = mock_get

        with patch("datawrapper.charts.base.Datawrapper", return_value=mock_client):
            chart = LineChart.get("test-id", access_token="test-token")

            assert chart.custom_ticks_x == [2020.0, 2021.0, 2022.0]
            assert chart.custom_ticks_y == [0.0, 25.0, 50.0, 75.0, 100.0]

    def test_get_parses_line_symbols(self):
        """Test get() correctly parses line symbol configuration."""
        mock_metadata = {
            "id": "test-id",
            "type": "d3-lines",
            "title": "Test",
            "metadata": {
                "data": {},
                "describe": {},
                "visualize": {
                    "lines": {
                        "series1": {
                            "symbols": {
                                "enabled": True,
                                "shape": "diamond",
                                "style": "hollow",
                                "on": "every",
                                "size": 8,
                                "opacity": 0.8,
                            }
                        }
                    }
                },
                "publish": {"blocks": {}},
                "annotate": {},
            },
        }

        mock_csv = "x,series1\n1,10"

        mock_client = Mock()
        mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"

        def mock_get(url):
            if url.endswith("/data"):
                return mock_csv
            return mock_metadata

        mock_client.get.side_effect = mock_get

        with patch("datawrapper.charts.base.Datawrapper", return_value=mock_client):
            chart = LineChart.get("test-id", access_token="test-token")

            series1_line = next(
                (line for line in chart.lines if line.column == "series1"), None
            )
            assert series1_line is not None
            symbols = series1_line.symbols
            assert symbols.enabled is True
            assert symbols.shape == "diamond"
            assert symbols.style == "hollow"
            assert symbols.on == "every"
            assert symbols.size == 8
            assert symbols.opacity == 0.8

    def test_get_parses_area_fills(self):
        """Test get() correctly parses area fill configuration."""
        mock_metadata = {
            "id": "test-id",
            "type": "d3-lines",
            "title": "Test",
            "metadata": {
                "data": {},
                "describe": {},
                "visualize": {
                    "custom-area-fills": {
                        "fill1": {
                            "from": "baseline",
                            "to": "value",
                            "color": "#ff0000",
                            "opacity": 0.5,
                            "useMixedColors": True,
                            "colorNegative": "#0000ff",
                            "interpolation": "step-before",
                        }
                    }
                },
                "publish": {"blocks": {}},
                "annotate": {},
            },
        }

        mock_csv = "x,baseline,value\n1,0,10"

        mock_client = Mock()
        mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"

        def mock_get(url):
            if url.endswith("/data"):
                return mock_csv
            return mock_metadata

        mock_client.get.side_effect = mock_get

        with patch("datawrapper.charts.base.Datawrapper", return_value=mock_client):
            chart = LineChart.get("test-id", access_token="test-token")

            assert len(chart.area_fills) == 1
            fill = chart.area_fills[0]
            assert fill.from_column == "baseline"
            assert fill.to_column == "value"
            assert fill.color == "#ff0000"
            assert fill.opacity == 0.5
            assert fill.use_mixed_colors is True
            assert fill.color_negative == "#0000ff"
            assert fill.interpolation == "step-before"


class TestLineChartIntegration:
    """Integration tests for LineChart workflows."""

    def test_round_trip_create_and_get(self):
        """Test creating a line chart and then fetching it back."""
        original_chart = LineChart(
            title="Test Line Chart",
            data=pd.DataFrame(
                {"date": ["2020/01", "2020/02"], "Temperature": [10.0, 20.0]}
            ),
            y_grid="on",
            interpolation="monotone-x",
        )

        mock_client = Mock()
        mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"
        mock_client.create_chart.return_value = {"id": "created-chart-id"}
        mock_client.update_chart.return_value = {"id": "created-chart-id"}

        # Create the chart
        with patch.object(original_chart, "_get_client", return_value=mock_client):
            original_chart.create(access_token="test-token")
            chart_id = original_chart.chart_id

        # Now fetch it back
        serialized = original_chart.serialize_model()
        mock_metadata = {
            "id": chart_id,
            "type": serialized["type"],
            "title": serialized["title"],
            "theme": serialized.get("theme", ""),
            "language": serialized.get("language", "en-US"),
            "metadata": serialized["metadata"],
        }

        mock_csv = "date,Temperature\n2020/01,10.0\n2020/02,20.0"

        def mock_get(url):
            if url.endswith("/data"):
                return mock_csv
            return mock_metadata

        mock_client.get.side_effect = mock_get

        with patch("datawrapper.charts.base.Datawrapper", return_value=mock_client):
            fetched_chart = LineChart.get(chart_id, access_token="test-token")

            # Verify key fields match
            assert fetched_chart.title == original_chart.title
            assert fetched_chart.chart_type == original_chart.chart_type
            assert fetched_chart.y_grid == original_chart.y_grid
            assert fetched_chart.interpolation == original_chart.interpolation

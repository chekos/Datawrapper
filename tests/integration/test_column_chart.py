"""Integration tests for ColumnChart class."""

import json
from pathlib import Path
from unittest.mock import Mock, patch

import pandas as pd

from datawrapper import ColumnChart


# Helper to load sample files
def load_sample_json(filename: str) -> dict:
    """Load a sample JSON file from tests/samples/column directory."""
    samples_dir = Path(__file__).parent.parent / "samples" / "column"
    with open(samples_dir / filename) as f:
        return json.load(f)


def load_sample_csv(filename: str) -> str:
    """Load a sample CSV file from tests/samples/column directory."""
    samples_dir = Path(__file__).parent.parent / "samples" / "column"
    with open(samples_dir / filename) as f:
        return f.read()


class TestColumnChartCreation:
    """Tests for ColumnChart creation and serialization."""

    def test_create_basic_column_chart(self):
        """Test creating a basic column chart."""
        chart = ColumnChart(
            title="Test Column Chart",
            data=pd.DataFrame({"date": ["2020/01", "2020/02"], "Value": [4.0, 3.8]}),
        )

        assert chart.chart_type == "column-chart"
        assert chart.title == "Test Column Chart"
        assert isinstance(chart.data, pd.DataFrame)

    def test_serialize_column_chart(self):
        """Test serializing a column chart."""
        chart = ColumnChart(
            title="Test Chart",
            data=pd.DataFrame({"date": ["2020/01"], "Value": [4.0]}),
            y_grid=True,
            show_value_labels="always",
            bar_padding=60,
        )

        serialized = chart.serialize_model()

        assert serialized["type"] == "column-chart"
        assert serialized["title"] == "Test Chart"
        assert serialized["metadata"]["visualize"]["grid-lines"] is True
        assert serialized["metadata"]["visualize"]["valueLabels"]["enabled"] is True
        assert serialized["metadata"]["visualize"]["value-labels-always"] is True
        assert serialized["metadata"]["visualize"]["bar-padding"] == 60

    def test_serialize_with_custom_ranges(self):
        """Test serializing with custom axis ranges."""
        chart = ColumnChart(
            title="Test",
            data=pd.DataFrame({"x": [1, 2], "y": [10, 20]}),
            custom_range_x=["2020", "2025"],
            custom_range_y=[0, 100],
        )

        serialized = chart.serialize_model()

        assert serialized["metadata"]["visualize"]["custom-range-x"] == ["2020", "2025"]
        assert serialized["metadata"]["visualize"]["custom-range"] == [0, 100]

    def test_serialize_with_custom_ticks(self):
        """Test serializing with custom tick marks."""
        chart = ColumnChart(
            title="Test",
            data=pd.DataFrame({"x": [1, 2], "y": [10, 20]}),
            custom_ticks_x=[2020, 2021, 2022],
            custom_ticks_y=[0, 25, 50, 75, 100],
        )

        serialized = chart.serialize_model()

        assert serialized["metadata"]["visualize"]["custom-ticks-x"] == "2020,2021,2022"
        assert serialized["metadata"]["visualize"]["custom-ticks"] == "0,25,50,75,100"

    def test_serialize_with_negative_color(self):
        """Test serializing with negative color enabled."""
        chart = ColumnChart(
            title="Test",
            data=pd.DataFrame({"x": [1, 2], "y": [10, -5]}),
            negative_color="#FF0000",
        )

        serialized = chart.serialize_model()

        assert serialized["metadata"]["visualize"]["negativeColor"]["enabled"] is True
        assert (
            serialized["metadata"]["visualize"]["negativeColor"]["value"] == "#FF0000"
        )

    def test_serialize_without_negative_color(self):
        """Test serializing with negative color disabled."""
        chart = ColumnChart(
            title="Test",
            data=pd.DataFrame({"x": [1, 2], "y": [10, 20]}),
            negative_color=None,
        )

        serialized = chart.serialize_model()

        assert serialized["metadata"]["visualize"]["negativeColor"]["enabled"] is False

    def test_serialize_y_axis_labels(self):
        """Test serializing Y-axis label configuration."""
        chart = ColumnChart(
            title="Test",
            data=pd.DataFrame({"x": [1, 2], "y": [10, 20]}),
            y_grid_labels="inside",
            y_grid_label_align="right",
        )

        serialized = chart.serialize_model()

        y_axis_labels = serialized["metadata"]["visualize"]["yAxisLabels"]
        assert y_axis_labels["enabled"] is True
        assert y_axis_labels["placement"] == "inside"
        assert y_axis_labels["alignment"] == "right"

    def test_serialize_plot_height_fixed(self):
        """Test serializing with fixed plot height."""
        chart = ColumnChart(
            title="Test",
            data=pd.DataFrame({"x": [1, 2], "y": [10, 20]}),
            plot_height_mode="fixed",
            plot_height_fixed=400,
        )

        serialized = chart.serialize_model()

        assert serialized["metadata"]["visualize"]["plotHeightMode"] == "fixed"
        assert serialized["metadata"]["visualize"]["plotHeightFixed"] == 400

    def test_serialize_plot_height_ratio(self):
        """Test serializing with ratio plot height."""
        chart = ColumnChart(
            title="Test",
            data=pd.DataFrame({"x": [1, 2], "y": [10, 20]}),
            plot_height_mode="ratio",
            plot_height_ratio=0.75,
        )

        serialized = chart.serialize_model()

        assert serialized["metadata"]["visualize"]["plotHeightMode"] == "ratio"
        assert serialized["metadata"]["visualize"]["plotHeightRatio"] == 0.75


class TestColumnChartGet:
    """Tests for ColumnChart.get() method."""

    def test_get_claims_sample(self):
        """Test get() with claims.json sample data (hover disabled)."""
        # Load sample data
        sample_json = load_sample_json("claims.json")
        chart_metadata = sample_json["chart"]["crdt"]["data"]
        sample_csv = load_sample_csv("claims.csv")

        mock_client = Mock()
        mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"

        def mock_get(url):
            if url.endswith("/data"):
                return sample_csv
            return chart_metadata

        mock_client.get.side_effect = mock_get

        with patch("datawrapper.charts.base.Datawrapper", return_value=mock_client):
            chart = ColumnChart.get("r8CFr", access_token="test-token")

            # Verify chart type and title
            assert chart.chart_type == "column-chart"
            assert chart.title == "US unemployment claims"

            # Verify value labels are off (enabled=false with show="hover" means off)
            assert chart.show_value_labels == "off"
            assert chart.value_labels_format == "0.[0]a"
            assert chart.value_labels_placement == "outside"

            # Verify other settings
            assert chart.base_color == "#7ec5ef"
            assert chart.bar_padding == 30

    def test_get_payrolls_sample(self):
        """Test get() with payrolls.json sample data (labels always on)."""
        # Load sample data
        sample_json = load_sample_json("payrolls.json")
        chart_metadata = sample_json["chart"]["crdt"]["data"]
        sample_csv = load_sample_csv("payrolls.csv")

        mock_client = Mock()
        mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"

        def mock_get(url):
            if url.endswith("/data"):
                return sample_csv
            return chart_metadata

        mock_client.get.side_effect = mock_get

        with patch("datawrapper.charts.base.Datawrapper", return_value=mock_client):
            chart = ColumnChart.get("4o25S", access_token="test-token")

            # Verify chart type and title
            assert chart.chart_type == "column-chart"
            assert chart.title == "Monthly change in US private payrolls"

            # Verify value labels are always on
            assert chart.show_value_labels == "always"
            assert chart.value_labels_format == "+1,000"
            assert chart.value_labels_placement == "outside"

            # Verify other settings
            assert chart.base_color == "#7ec5ef"
            assert chart.bar_padding == 30
            assert chart.y_grid_format == "+1a"

    def test_get_unemployment_sample(self):
        """Test get() with unemployment.json sample data."""
        # Load sample data
        sample_json = load_sample_json("unemployment.json")
        chart_metadata = sample_json["chart"]["crdt"]["data"]
        sample_csv = load_sample_csv("unemployment.csv")

        mock_client = Mock()
        mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"

        def mock_get(url):
            if url.endswith("/data"):
                return sample_csv
            return chart_metadata

        mock_client.get.side_effect = mock_get

        with patch("datawrapper.charts.base.Datawrapper", return_value=mock_client):
            chart = ColumnChart.get("4W1MA", access_token="test-token")

            # Verify chart type
            assert chart.chart_type == "column-chart"
            assert (
                chart.title
                == "Figure 4. Nowcast estimates for 2020Q1-2020Q3 and projections for working-hour losses in 2020Q4, world (percentage)"
            )

            # Verify description fields
            assert (
                chart.notes
                == "Note: See Technical Annex 2 for further details on the scenarios used to obtain these projections."
            )

            # Verify axis configuration
            assert chart.x_grid == "off"
            assert chart.y_grid is True
            assert chart.y_grid_labels == "outside"
            assert chart.y_grid_label_align == "left"

            # Verify appearance
            assert chart.bar_padding == 60
            assert chart.plot_height_mode == "fixed"
            assert chart.plot_height_fixed == 228
            assert chart.negative_color is None  # disabled in sample

            # Verify value labels
            assert chart.show_value_labels == "always"
            assert chart.value_labels_placement == "outside"

    def test_get_parses_grid_lines_x(self):
        """Test get() correctly parses X-axis grid lines."""
        mock_metadata = {
            "id": "test-id",
            "type": "column-chart",
            "title": "Test",
            "metadata": {
                "data": {},
                "describe": {},
                "visualize": {
                    "grid-lines-x": {
                        "type": "ticks",
                        "enabled": True,
                    }
                },
                "publish": {"blocks": {}},
                "annotate": {},
            },
        }

        mock_csv = "x,y\n1,10\n2,20"

        mock_client = Mock()
        mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"

        def mock_get(url):
            if url.endswith("/data"):
                return mock_csv
            return mock_metadata

        mock_client.get.side_effect = mock_get

        with patch("datawrapper.charts.base.Datawrapper", return_value=mock_client):
            chart = ColumnChart.get("test-id", access_token="test-token")

            assert chart.x_grid == "ticks"

    def test_get_parses_custom_ticks(self):
        """Test get() correctly parses custom ticks from comma-separated strings."""
        mock_metadata = {
            "id": "test-id",
            "type": "column-chart",
            "title": "Test",
            "metadata": {
                "data": {},
                "describe": {},
                "visualize": {
                    "custom-ticks-x": "2020,2021,2022",
                    "custom-ticks": "0,25,50,75,100",
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
            chart = ColumnChart.get("test-id", access_token="test-token")

            assert chart.custom_ticks_x == [2020.0, 2021.0, 2022.0]
            assert chart.custom_ticks_y == [0.0, 25.0, 50.0, 75.0, 100.0]

    def test_get_parses_negative_color_enabled(self):
        """Test get() correctly parses negative color when enabled."""
        mock_metadata = {
            "id": "test-id",
            "type": "column-chart",
            "title": "Test",
            "metadata": {
                "data": {},
                "describe": {},
                "visualize": {
                    "negativeColor": {
                        "enabled": True,
                        "value": "#FF0000",
                    }
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
            chart = ColumnChart.get("test-id", access_token="test-token")

            assert chart.negative_color == "#FF0000"

    def test_get_parses_negative_color_disabled(self):
        """Test get() correctly parses negative color when disabled."""
        mock_metadata = {
            "id": "test-id",
            "type": "column-chart",
            "title": "Test",
            "metadata": {
                "data": {},
                "describe": {},
                "visualize": {
                    "negativeColor": {
                        "enabled": False,
                        "value": "#FF0000",
                    }
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
            chart = ColumnChart.get("test-id", access_token="test-token")

            assert chart.negative_color is None

    def test_get_parses_value_labels(self):
        """Test get() correctly parses value label configuration."""
        mock_metadata = {
            "id": "test-id",
            "type": "column-chart",
            "title": "Test",
            "metadata": {
                "data": {},
                "describe": {},
                "visualize": {
                    "valueLabels": {
                        "enabled": True,
                        "show": "always",
                        "format": "0.0%",
                        "placement": "inside",
                    }
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
            chart = ColumnChart.get("test-id", access_token="test-token")

            assert chart.show_value_labels == "always"
            assert chart.value_labels_format == "0.0%"
            assert chart.value_labels_placement == "inside"


class TestColumnChartIntegration:
    """Integration tests for ColumnChart workflows."""

    def test_round_trip_create_and_get(self):
        """Test creating a column chart and then fetching it back."""
        original_chart = ColumnChart(
            title="Test Column Chart",
            data=pd.DataFrame({"date": ["2020/01", "2020/02"], "Value": [10.0, 20.0]}),
            y_grid=True,
            show_value_labels="always",
            bar_padding=50,
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

        mock_csv = "date,Value\n2020/01,10.0\n2020/02,20.0"

        def mock_get(url):
            if url.endswith("/data"):
                return mock_csv
            return mock_metadata

        mock_client.get.side_effect = mock_get

        with patch("datawrapper.charts.base.Datawrapper", return_value=mock_client):
            fetched_chart = ColumnChart.get(chart_id, access_token="test-token")

            # Verify key fields match
            assert fetched_chart.title == original_chart.title
            assert fetched_chart.chart_type == original_chart.chart_type
            assert fetched_chart.y_grid == original_chart.y_grid
            assert fetched_chart.show_value_labels == original_chart.show_value_labels
            assert fetched_chart.bar_padding == original_chart.bar_padding


class TestColumnChartCategoryLabels:
    """Tests for category labels functionality in ColumnChart."""

    def test_serialize_with_category_labels(self):
        """Test serializing with category labels."""
        chart = ColumnChart(
            title="Test",
            data=pd.DataFrame({"x": [1, 2], "y": [10, 20]}),
            color_category={"Series A": "#FF0000", "Series B": "#00FF00"},
            category_labels={"Series A": "First Series", "Series B": "Second Series"},
        )

        serialized = chart.serialize_model()
        color_category = serialized["metadata"]["visualize"]["color-category"]

        assert color_category["map"] == {"Series A": "#FF0000", "Series B": "#00FF00"}
        assert color_category["categoryLabels"] == {
            "Series A": "First Series",
            "Series B": "Second Series",
        }

    def test_serialize_with_category_order(self):
        """Test serializing with category order."""
        chart = ColumnChart(
            title="Test",
            data=pd.DataFrame({"x": [1, 2], "y": [10, 20]}),
            color_category={"Series A": "#FF0000", "Series B": "#00FF00"},
            category_order=["Series B", "Series A"],
        )

        serialized = chart.serialize_model()
        color_category = serialized["metadata"]["visualize"]["color-category"]

        assert color_category["categoryOrder"] == ["Series B", "Series A"]

    def test_serialize_without_category_labels(self):
        """Test serializing without category labels (should not include empty fields)."""
        chart = ColumnChart(
            title="Test",
            data=pd.DataFrame({"x": [1, 2], "y": [10, 20]}),
            color_category={"Series A": "#FF0000"},
        )

        serialized = chart.serialize_model()
        color_category = serialized["metadata"]["visualize"]["color-category"]

        assert "categoryLabels" not in color_category
        assert "categoryOrder" not in color_category

    def test_get_parses_category_labels(self):
        """Test get() correctly parses category labels from API response."""
        mock_metadata = {
            "id": "test-id",
            "type": "column-chart",
            "title": "Test",
            "metadata": {
                "data": {},
                "describe": {},
                "visualize": {
                    "color-category": {
                        "map": {"Series A": "#FF0000", "Series B": "#00FF00"},
                        "categoryLabels": {"Series A": "First", "Series B": "Second"},
                        "categoryOrder": ["Series B", "Series A"],
                    }
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
            chart = ColumnChart.get("test-id", access_token="test-token")

            assert chart.color_category == {
                "Series A": "#FF0000",
                "Series B": "#00FF00",
            }
            assert chart.category_labels == {"Series A": "First", "Series B": "Second"}
            assert chart.category_order == ["Series B", "Series A"]

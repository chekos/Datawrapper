"""Integration tests for AreaChart class."""

import json
from pathlib import Path
from unittest.mock import Mock, patch

import pandas as pd

from datawrapper import AreaChart


# Helper to load sample files
def load_sample_json(filename: str) -> dict:
    """Load a sample JSON file from tests/samples/area directory."""
    samples_dir = Path(__file__).parent.parent / "samples" / "area"
    with open(samples_dir / filename) as f:
        return json.load(f)


def load_sample_csv(filename: str) -> str:
    """Load a sample CSV file from tests/samples/area directory."""
    samples_dir = Path(__file__).parent.parent / "samples" / "area"
    with open(samples_dir / filename) as f:
        return f.read()


class TestAreaChartCreation:
    """Tests for AreaChart creation and serialization."""

    def test_create_basic_area_chart(self):
        """Test creating a basic area chart."""
        chart = AreaChart(
            title="Test Area Chart",
            data=pd.DataFrame(
                {
                    "year": ["2020", "2021", "2022"],
                    "Region A": [100, 120, 140],
                    "Region B": [80, 90, 100],
                }
            ),
        )

        assert chart.chart_type == "d3-area"
        assert chart.title == "Test Area Chart"
        assert isinstance(chart.data, pd.DataFrame)

    def test_serialize_area_chart(self):
        """Test serializing an area chart."""
        chart = AreaChart(
            title="Test Chart",
            data=pd.DataFrame({"year": ["2020"], "Value": [100]}),
            stack_areas=True,
            area_opacity=0.9,
            interpolation="monotone-x",
        )

        serialized = chart.serialize_model()

        assert serialized["type"] == "d3-area"
        assert serialized["title"] == "Test Chart"
        assert serialized["metadata"]["visualize"]["stack-areas"] is True
        assert serialized["metadata"]["visualize"]["area-opacity"] == 0.9
        assert serialized["metadata"]["visualize"]["interpolation"] == "monotone-x"

    def test_serialize_with_stacking(self):
        """Test serializing with area stacking options."""
        chart = AreaChart(
            title="Test",
            data=pd.DataFrame({"x": [1, 2], "y": [10, 20]}),
            stack_areas=True,
            stack_to_100=True,
            sort_areas="desc",
        )

        serialized = chart.serialize_model()

        assert serialized["metadata"]["visualize"]["stack-areas"] is True
        assert serialized["metadata"]["visualize"]["stack-to-100"] is True
        assert serialized["metadata"]["visualize"]["sort-areas"] == "desc"

    def test_serialize_with_separator_lines(self):
        """Test serializing with area separator lines."""
        chart = AreaChart(
            title="Test",
            data=pd.DataFrame({"x": [1, 2], "y": [10, 20]}),
            area_separator_lines=True,
            area_separator_color="#ff0000",
        )

        serialized = chart.serialize_model()

        assert serialized["metadata"]["visualize"]["area-separator-lines"] is True
        assert serialized["metadata"]["visualize"]["area-separator-color"] == "#ff0000"

    def test_serialize_with_custom_colors(self):
        """Test serializing with custom color mapping."""
        chart = AreaChart(
            title="Test",
            data=pd.DataFrame({"x": [1, 2], "Series A": [10, 20], "Series B": [5, 15]}),
            color_category={"Series A": "#ff0000", "Series B": "#0000ff"},
            show_color_key=True,
        )

        serialized = chart.serialize_model()

        assert serialized["metadata"]["visualize"]["color-category"]["map"] == {
            "Series A": "#ff0000",
            "Series B": "#0000ff",
        }
        assert serialized["metadata"]["visualize"]["show-color-key"] is True

    def test_serialize_with_tooltips(self):
        """Test serializing with tooltip configuration."""
        chart = AreaChart(
            title="Test",
            data=pd.DataFrame({"x": [1, 2], "y": [10, 20]}),
            show_tooltips=True,
            tooltip_x_format="YYYY",
            tooltip_number_format="0,0.[00]",
        )

        serialized = chart.serialize_model()

        assert serialized["metadata"]["visualize"]["show-tooltips"] is True
        assert serialized["metadata"]["visualize"]["tooltip-x-format"] == "YYYY"
        assert (
            serialized["metadata"]["visualize"]["tooltip-number-format"] == "0,0.[00]"
        )

    def test_serialize_with_annotations(self):
        """Test serializing with text and range annotations."""
        chart = AreaChart(
            title="Test",
            data=pd.DataFrame({"x": [1, 2], "y": [10, 20]}),
            text_annotations=[
                {
                    "text": "Important event",
                    "x": "2020",
                    "y": 100,
                }
            ],
            range_annotations=[
                {
                    "x0": "2020",
                    "x1": "2021",
                    "y0": 0,
                    "y1": 100,
                }
            ],
        )

        serialized = chart.serialize_model()

        # Annotations should be lists of dicts
        assert isinstance(serialized["metadata"]["visualize"]["text-annotations"], list)
        assert isinstance(
            serialized["metadata"]["visualize"]["range-annotations"], list
        )
        assert len(serialized["metadata"]["visualize"]["text-annotations"]) == 1
        assert len(serialized["metadata"]["visualize"]["range-annotations"]) == 1


class TestAreaChartGet:
    """Tests for AreaChart.get() method."""

    def test_get_migration_sample(self):
        """Test get() with migration.json sample data (complex stacked chart)."""
        # Load sample data
        sample_json = load_sample_json("migration.json")
        chart_metadata = sample_json["chart"]["crdt"]["data"]
        sample_csv = load_sample_csv("migration.csv")

        mock_client = Mock()
        mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"

        def mock_get(url):
            if url.endswith("/data"):
                return sample_csv
            return chart_metadata

        mock_client.get.side_effect = mock_get

        with patch("datawrapper.charts.base.Datawrapper", return_value=mock_client):
            chart = AreaChart.get("y71E1", access_token="test-token")

            # Verify chart type and title
            assert chart.chart_type == "d3-area"
            assert chart.title == "Migration to the US by world region, 1820-2009"

            # Verify axes configuration
            assert chart.x_grid == "off"
            assert chart.y_grid == "on"
            assert chart.x_grid_format == "YYYY"
            assert chart.y_grid_format == "0.[00]a"
            assert chart.y_grid_labels == "auto"

            # Verify area customization
            assert chart.stack_areas is True
            assert chart.area_opacity == 1
            assert chart.interpolation == "natural"
            assert chart.sort_areas == "keep"

            # Verify color mapping (should have many regions)
            assert len(chart.color_category) > 10
            assert "China" in chart.color_category
            assert "Mexico" in chart.color_category

            # Verify tooltips
            assert chart.show_tooltips is True
            assert chart.tooltip_x_format == "YYYY"
            assert chart.tooltip_number_format == "0.00a"

    def test_get_plastic_sample(self):
        """Test get() with plastic.json sample data."""
        # Load sample data
        sample_json = load_sample_json("plastic.json")
        chart_metadata = sample_json["chart"]["crdt"]["data"]
        sample_csv = load_sample_csv("plastic.csv")

        mock_client = Mock()
        mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"

        def mock_get(url):
            if url.endswith("/data"):
                return sample_csv
            return chart_metadata

        mock_client.get.side_effect = mock_get

        with patch("datawrapper.charts.base.Datawrapper", return_value=mock_client):
            chart = AreaChart.get("test-id", access_token="test-token")

            # Verify chart type
            assert chart.chart_type == "d3-area"

            # Verify it parsed successfully
            assert chart.title is not None

    def test_get_population_sample(self):
        """Test get() with population.json sample data."""
        # Load sample data
        sample_json = load_sample_json("population.json")
        chart_metadata = sample_json["chart"]["crdt"]["data"]
        sample_csv = load_sample_csv("population.csv")

        mock_client = Mock()
        mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"

        def mock_get(url):
            if url.endswith("/data"):
                return sample_csv
            return chart_metadata

        mock_client.get.side_effect = mock_get

        with patch("datawrapper.charts.base.Datawrapper", return_value=mock_client):
            chart = AreaChart.get("test-id", access_token="test-token")

            # Verify chart type
            assert chart.chart_type == "d3-area"

            # Verify it parsed successfully
            assert chart.title is not None

    def test_get_tate_sample(self):
        """Test get() with tate.json sample data."""
        # Load sample data
        sample_json = load_sample_json("tate.json")
        chart_metadata = sample_json["chart"]["crdt"]["data"]
        sample_csv = load_sample_csv("tate.csv")

        mock_client = Mock()
        mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"

        def mock_get(url):
            if url.endswith("/data"):
                return sample_csv
            return chart_metadata

        mock_client.get.side_effect = mock_get

        with patch("datawrapper.charts.base.Datawrapper", return_value=mock_client):
            chart = AreaChart.get("test-id", access_token="test-token")

            # Verify chart type
            assert chart.chart_type == "d3-area"

            # Verify it parsed successfully
            assert chart.title is not None

    def test_get_parses_custom_ticks(self):
        """Test get() correctly parses custom ticks from comma-separated strings."""
        mock_metadata = {
            "id": "test-id",
            "type": "d3-area",
            "title": "Test",
            "metadata": {
                "data": {},
                "describe": {},
                "visualize": {
                    "custom-ticks-x": "2020,2021,2022",
                    "custom-ticks-y": "0,50,100",
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
            chart = AreaChart.get("test-id", access_token="test-token")

            assert chart.custom_ticks_x == [2020.0, 2021.0, 2022.0]
            assert chart.custom_ticks_y == [0.0, 50.0, 100.0]


class TestAreaChartIntegration:
    """Integration tests for AreaChart workflows."""

    def test_round_trip_create_and_get(self):
        """Test creating an area chart and then fetching it back."""
        original_chart = AreaChart(
            title="Test Area Chart",
            data=pd.DataFrame(
                {
                    "year": ["2020", "2021", "2022"],
                    "Region A": [100, 120, 140],
                    "Region B": [80, 90, 100],
                }
            ),
            stack_areas=True,
            area_opacity=0.8,
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

        mock_csv = "year,Region A,Region B\n2020,100,80\n2021,120,90\n2022,140,100"

        def mock_get(url):
            if url.endswith("/data"):
                return mock_csv
            return mock_metadata

        mock_client.get.side_effect = mock_get

        with patch("datawrapper.charts.base.Datawrapper", return_value=mock_client):
            fetched_chart = AreaChart.get(chart_id, access_token="test-token")

            # Verify key fields match
            assert fetched_chart.title == original_chart.title
            assert fetched_chart.chart_type == original_chart.chart_type
            assert fetched_chart.stack_areas == original_chart.stack_areas
            assert fetched_chart.area_opacity == original_chart.area_opacity

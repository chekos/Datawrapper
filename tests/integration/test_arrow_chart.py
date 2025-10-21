"""Integration tests for ArrowChart class."""

import json
from pathlib import Path
from unittest.mock import Mock, patch

import pandas as pd

from datawrapper import ArrowChart


# Helper to load sample files
def load_sample_json(filename: str) -> dict:
    """Load a sample JSON file from tests/samples/arrow directory."""
    samples_dir = Path(__file__).parent.parent / "samples" / "arrow"
    with open(samples_dir / filename) as f:
        return json.load(f)


def load_sample_csv(filename: str) -> str:
    """Load a sample CSV file from tests/samples/arrow directory."""
    samples_dir = Path(__file__).parent.parent / "samples" / "arrow"
    with open(samples_dir / filename) as f:
        return f.read()


class TestArrowChartCreation:
    """Tests for ArrowChart creation and serialization."""

    def test_serialize_with_axis_colors_and_labels(self):
        """Test serializing with color_column and label_column."""
        chart = ArrowChart(
            title="Test",
            data=pd.DataFrame({"Country": ["A", "B"], "Start": [1, 2], "End": [3, 4]}),
            start_column="Start",
            end_column="End",
            color_column="Country",
            label_column="Country",
        )

        serialized = chart.serialize_model()

        assert serialized["metadata"]["axes"]["colors"] == "Country"
        assert serialized["metadata"]["axes"]["labels"] == "Country"

    def test_serialize_conditional_axes_fields(self):
        """Test that axes fields are only included when non-None (conditional serialization)."""
        # Test with only start and end columns (minimal axes)
        chart = ArrowChart(
            title="Test",
            data=pd.DataFrame({"x": [1, 2], "y": [10, 20], "z": [15, 25]}),
            start_column="y",
            end_column="z",
        )

        serialized = chart.serialize_model()

        # Should only include start and end
        assert "axes" in serialized["metadata"]
        assert serialized["metadata"]["axes"]["start"] == "y"
        assert serialized["metadata"]["axes"]["end"] == "z"
        assert "colors" not in serialized["metadata"]["axes"]
        assert "labels" not in serialized["metadata"]["axes"]

    def test_serialize_no_axes_when_all_none(self):
        """Test that axes section is omitted when all axes fields are None."""
        chart = ArrowChart(
            title="Test",
            data=pd.DataFrame({"x": [1, 2], "y": [10, 20]}),
            # No axes columns specified
        )

        serialized = chart.serialize_model()

        # axes section should not be present at all
        assert "axes" not in serialized["metadata"]

    def test_serialize_partial_axes_fields(self):
        """Test serializing with only some axes fields set."""
        # Test with start, end, and color but no label
        chart = ArrowChart(
            title="Test",
            data=pd.DataFrame({"Country": ["A", "B"], "Start": [1, 2], "End": [3, 4]}),
            start_column="Start",
            end_column="End",
            color_column="Country",
            # label_column intentionally omitted
        )

        serialized = chart.serialize_model()

        assert "axes" in serialized["metadata"]
        assert serialized["metadata"]["axes"]["start"] == "Start"
        assert serialized["metadata"]["axes"]["end"] == "End"
        assert serialized["metadata"]["axes"]["colors"] == "Country"
        assert "labels" not in serialized["metadata"]["axes"]

    def test_create_basic_arrow_chart(self):
        """Test creating a basic arrow chart."""
        chart = ArrowChart(
            title="Test Arrow Chart",
            data=pd.DataFrame(
                {
                    "Region": ["North", "South", "East", "West"],
                    "2020": [100, 150, 120, 90],
                    "2023": [110, 160, 115, 95],
                }
            ),
            start_column="2020",
            end_column="2023",
        )

        assert chart.chart_type == "d3-arrow-plot"
        assert chart.title == "Test Arrow Chart"
        assert isinstance(chart.data, pd.DataFrame)
        assert chart.start_column == "2020"
        assert chart.end_column == "2023"

    def test_serialize_arrow_chart(self):
        """Test serializing an arrow chart."""
        chart = ArrowChart(
            title="Test Chart",
            data=pd.DataFrame({"Region": ["A"], "Start": [10], "End": [20]}),
            start_column="Start",
            end_column="End",
            thick_arrows=True,
            y_grid="on",
        )

        serialized = chart.serialize_model()

        assert serialized["type"] == "d3-arrow-plot"
        assert serialized["title"] == "Test Chart"
        assert serialized["metadata"]["visualize"]["thick-arrows"] is True
        assert serialized["metadata"]["visualize"]["y-grid"] == "on"
        assert serialized["metadata"]["axes"]["start"] == "Start"
        assert serialized["metadata"]["axes"]["end"] == "End"

    def test_serialize_with_sorting(self):
        """Test serializing with sorting options."""
        chart = ArrowChart(
            title="Test",
            data=pd.DataFrame({"x": [1, 2], "y": [10, 20], "z": [15, 25]}),
            start_column="y",
            end_column="z",
            sort_ranges=True,
            sort_by="difference",
            reverse_order=True,
        )

        serialized = chart.serialize_model()

        assert serialized["metadata"]["visualize"]["sort-range"]["enabled"] is True
        assert serialized["metadata"]["visualize"]["sort-range"]["by"] == "difference"
        assert serialized["metadata"]["visualize"]["reverse-order"] is True

    def test_serialize_with_flags(self):
        """Test serializing with flag replacement."""
        chart = ArrowChart(
            title="Test",
            data=pd.DataFrame(
                {"Country": ["US", "UK"], "2020": [10, 20], "2023": [15, 25]}
            ),
            start_column="2020",
            end_column="2023",
            replace_flags="4x3",
        )

        serialized = chart.serialize_model()

        assert serialized["metadata"]["visualize"]["replace-flags"]["enabled"] is True
        assert serialized["metadata"]["visualize"]["replace-flags"]["style"] == "4x3"

    def test_serialize_with_flags_off(self):
        """Test serializing with flags disabled."""
        chart = ArrowChart(
            title="Test",
            data=pd.DataFrame({"x": [1], "y": [10], "z": [20]}),
            start_column="y",
            end_column="z",
            replace_flags="off",
        )

        serialized = chart.serialize_model()

        assert serialized["metadata"]["visualize"]["replace-flags"]["enabled"] is False
        assert serialized["metadata"]["visualize"]["replace-flags"]["style"] == ""

    def test_serialize_with_custom_colors(self):
        """Test serializing with custom color mapping."""
        chart = ArrowChart(
            title="Test",
            data=pd.DataFrame({"x": [1, 2], "y": [10, 20], "z": [15, 25]}),
            start_column="y",
            end_column="z",
            color_category={"Series A": "#ff0000", "Series B": "#0000ff"},
        )

        serialized = chart.serialize_model()

        assert serialized["metadata"]["visualize"]["color-category"]["map"] == {
            "Series A": "#ff0000",
            "Series B": "#0000ff",
        }

    def test_serialize_with_features(self):
        """Test serializing with feature flags."""
        chart = ArrowChart(
            title="Test",
            data=pd.DataFrame({"x": [1, 2], "y": [10, 20], "z": [15, 25]}),
            start_column="y",
            end_column="z",
            groups_column="x",  # Setting groups_column should enable group-by-column
            arrow_key=True,
        )

        serialized = chart.serialize_model()

        assert serialized["metadata"]["visualize"]["group-by-column"] is True
        assert serialized["metadata"]["visualize"]["show-arrow-key"] is True

    def test_serialize_with_formatting(self):
        """Test serializing with value label formatting."""
        chart = ArrowChart(
            title="Test",
            data=pd.DataFrame({"x": [1, 2], "y": [10, 20], "z": [15, 25]}),
            start_column="y",
            end_column="z",
            value_label_format="0.0%",
            range_value_labels="both",
        )

        serialized = chart.serialize_model()

        assert serialized["metadata"]["visualize"]["value-label-format"] == "0.0%"
        assert serialized["metadata"]["visualize"]["range-value-labels"] == "both"

    def test_serialize_with_custom_range(self):
        """Test serializing with custom range."""
        chart = ArrowChart(
            title="Test",
            data=pd.DataFrame({"x": [1, 2], "y": [10, 20], "z": [15, 25]}),
            start_column="y",
            end_column="z",
            custom_range=[0, 100],
            range_extent="custom",
        )

        serialized = chart.serialize_model()

        assert serialized["metadata"]["visualize"]["custom-range"] == [0, 100]
        assert serialized["metadata"]["visualize"]["range-extent"] == "custom"


class TestArrowChartGet:
    """Tests for ArrowChart.get() method."""

    def test_get_babies_sample(self):
        """Test get() with babies.json sample data (complex chart with groups)."""
        # Load sample data
        sample_json = load_sample_json("babies.json")
        chart_metadata = sample_json["chart"]["crdt"]["data"]
        sample_csv = load_sample_csv("babies.csv")

        mock_client = Mock()
        mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"

        def mock_get(url):
            if url.endswith("/data"):
                return sample_csv
            return chart_metadata

        mock_client.get.side_effect = mock_get

        with patch("datawrapper.charts.base.Datawrapper", return_value=mock_client):
            chart = ArrowChart.get("YG69c", access_token="test-token")

            # Verify chart type and title
            assert chart.chart_type == "d3-arrow-plot"
            assert (
                chart.title
                == "Far fewer babies share the most popular names now than in 1950"
            )

            # Verify axes
            assert chart.start_column == "1950"
            assert chart.end_column == "2022"

            # Verify features
            assert chart.thick_arrows is True
            assert chart.arrow_key is True
            assert chart.groups_column == "Gender"

            # Verify sorting
            assert chart.sort_ranges is False
            assert chart.sort_by == "start"

            # Verify color mapping
            assert len(chart.color_category) > 0
            assert "1950" in chart.color_category

    def test_get_english_sample(self):
        """Test get() with english.json sample data."""
        # Load sample data
        sample_json = load_sample_json("english.json")
        chart_metadata = sample_json["chart"]["crdt"]["data"]
        sample_csv = load_sample_csv("english.csv")

        mock_client = Mock()
        mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"

        def mock_get(url):
            if url.endswith("/data"):
                return sample_csv
            return chart_metadata

        mock_client.get.side_effect = mock_get

        with patch("datawrapper.charts.base.Datawrapper", return_value=mock_client):
            chart = ArrowChart.get("test-id", access_token="test-token")

            # Verify chart type
            assert chart.chart_type == "d3-arrow-plot"

            # Verify it parsed successfully
            assert chart.title is not None

    def test_get_ev_sample(self):
        """Test get() with ev.json sample data."""
        # Load sample data
        sample_json = load_sample_json("ev.json")
        chart_metadata = sample_json["chart"]["crdt"]["data"]
        sample_csv = load_sample_csv("ev.csv")

        mock_client = Mock()
        mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"

        def mock_get(url):
            if url.endswith("/data"):
                return sample_csv
            return chart_metadata

        mock_client.get.side_effect = mock_get

        with patch("datawrapper.charts.base.Datawrapper", return_value=mock_client):
            chart = ArrowChart.get("test-id", access_token="test-token")

            # Verify chart type
            assert chart.chart_type == "d3-arrow-plot"

            # Verify it parsed successfully
            assert chart.title is not None

    def test_get_inequality_sample(self):
        """Test get() with inequality.json sample data."""
        # Load sample data
        sample_json = load_sample_json("inequality.json")
        chart_metadata = sample_json["chart"]["crdt"]["data"]
        sample_csv = load_sample_csv("inequality.csv")

        mock_client = Mock()
        mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"

        def mock_get(url):
            if url.endswith("/data"):
                return sample_csv
            return chart_metadata

        mock_client.get.side_effect = mock_get

        with patch("datawrapper.charts.base.Datawrapper", return_value=mock_client):
            chart = ArrowChart.get("test-id", access_token="test-token")

            # Verify chart type
            assert chart.chart_type == "d3-arrow-plot"

            # Verify it parsed successfully
            assert chart.title is not None

    def test_get_parses_flags_enabled(self):
        """Test get() correctly parses replace-flags when enabled."""
        mock_metadata = {
            "id": "test-id",
            "type": "d3-arrow-plot",
            "title": "Test",
            "metadata": {
                "data": {},
                "describe": {},
                "visualize": {
                    "replace-flags": {
                        "enabled": True,
                        "type": "4x3",
                        "style": "4x3",
                    }
                },
                "axes": {"start": "2020", "end": "2023"},
                "publish": {"blocks": {}},
                "annotate": {},
            },
        }

        mock_csv = "x,y,z\n1,10,20"

        mock_client = Mock()
        mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"

        def mock_get(url):
            if url.endswith("/data"):
                return mock_csv
            return mock_metadata

        mock_client.get.side_effect = mock_get

        with patch("datawrapper.charts.base.Datawrapper", return_value=mock_client):
            chart = ArrowChart.get("test-id", access_token="test-token")

            assert chart.replace_flags == "4x3"

    def test_get_parses_flags_disabled(self):
        """Test get() correctly parses replace-flags when disabled."""
        mock_metadata = {
            "id": "test-id",
            "type": "d3-arrow-plot",
            "title": "Test",
            "metadata": {
                "data": {},
                "describe": {},
                "visualize": {
                    "replace-flags": {
                        "enabled": False,
                        "type": "",
                        "style": "",
                    }
                },
                "axes": {"start": "2020", "end": "2023"},
                "publish": {"blocks": {}},
                "annotate": {},
            },
        }

        mock_csv = "x,y,z\n1,10,20"

        mock_client = Mock()
        mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"

        def mock_get(url):
            if url.endswith("/data"):
                return mock_csv
            return mock_metadata

        mock_client.get.side_effect = mock_get

        with patch("datawrapper.charts.base.Datawrapper", return_value=mock_client):
            chart = ArrowChart.get("test-id", access_token="test-token")

            assert chart.replace_flags == "off"


class TestArrowChartIntegration:
    """Integration tests for ArrowChart workflows."""

    def test_round_trip_create_and_get(self):
        """Test creating an arrow chart and then fetching it back."""
        original_chart = ArrowChart(
            title="Test Arrow Chart",
            data=pd.DataFrame(
                {
                    "Region": ["North", "South", "East", "West"],
                    "2020": [100, 150, 120, 90],
                    "2023": [110, 160, 115, 95],
                }
            ),
            start_column="2020",
            end_column="2023",
            thick_arrows=True,
            sort_ranges=True,
            sort_by="difference",
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

        mock_csv = (
            "Region,2020,2023\nNorth,100,110\nSouth,150,160\nEast,120,115\nWest,90,95"
        )

        def mock_get(url):
            if url.endswith("/data"):
                return mock_csv
            return mock_metadata

        mock_client.get.side_effect = mock_get

        with patch("datawrapper.charts.base.Datawrapper", return_value=mock_client):
            fetched_chart = ArrowChart.get(chart_id, access_token="test-token")

            # Verify key fields match
            assert fetched_chart.title == original_chart.title
            assert fetched_chart.chart_type == original_chart.chart_type
            assert fetched_chart.start_column == original_chart.start_column
            assert fetched_chart.end_column == original_chart.end_column
            assert fetched_chart.thick_arrows == original_chart.thick_arrows
            assert fetched_chart.sort_ranges == original_chart.sort_ranges
            assert fetched_chart.sort_by == original_chart.sort_by

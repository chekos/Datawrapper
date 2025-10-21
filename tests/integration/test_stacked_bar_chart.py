"""Integration tests for StackedBarChart class."""

import json
from pathlib import Path
from unittest.mock import Mock, patch

import pandas as pd

from datawrapper.charts import StackedBarChart


# Helper functions to load sample data
def load_sample_json(filename: str) -> dict:
    """Load a sample JSON file from tests/samples/stacked_bar/."""
    sample_path = Path(__file__).parent.parent / "samples" / "stacked_bar" / filename
    with open(sample_path) as f:
        data = json.load(f)
        # Extract the actual chart data from the CRDT wrapper
        return data["chart"]["crdt"]["data"]


def load_sample_csv(filename: str) -> str:
    """Load a sample CSV file from tests/samples/stacked_bar/."""
    sample_path = Path(__file__).parent.parent / "samples" / "stacked_bar" / filename
    with open(sample_path) as f:
        return f.read()


class TestStackedBarChartCreation:
    """Test creating StackedBarChart instances with various configurations."""

    def test_create_minimal_chart(self):
        """Test creating a minimal stacked bar chart."""
        df = pd.DataFrame({"A": [1, 3], "B": [2, 4]})
        chart = StackedBarChart(
            title="Test Chart",
            data=df,
        )
        assert chart.title == "Test Chart"
        assert chart.chart_type == "d3-bars-stacked"

    def test_create_with_colors(self):
        """Test creating a chart with color mappings."""
        df = pd.DataFrame({"A": [1], "B": [2]})
        chart = StackedBarChart(
            title="Colored Chart",
            data=df,
            color_category={"Series A": "#ff0000", "Series B": "#00ff00"},
        )
        assert chart.color_category == {"Series A": "#ff0000", "Series B": "#00ff00"}

    def test_create_with_flags(self):
        """Test creating a chart with flag replacement."""
        df = pd.DataFrame({"Country": ["USA"], "Value": [100]})
        chart = StackedBarChart(
            title="Flag Chart",
            data=df,
            replace_flags="4x3",
        )
        assert chart.replace_flags == "4x3"

    def test_create_with_sorting(self):
        """Test creating a chart with sorting options."""
        df = pd.DataFrame({"A": [1], "B": [2]})
        chart = StackedBarChart(
            title="Sorted Chart",
            data=df,
            sort_bars=True,
            sort_by="B",
            reverse_order=True,
        )
        assert chart.sort_bars is True
        assert chart.sort_by == "B"
        assert chart.reverse_order is True

    def test_create_with_percentages(self):
        """Test creating a chart with percentage display."""
        df = pd.DataFrame({"A": [1], "B": [2]})
        chart = StackedBarChart(
            title="Percentage Chart",
            data=df,
            stack_percentages=True,
            value_label_format="0%",
        )
        assert chart.stack_percentages is True
        assert chart.value_label_format == "0%"

    def test_create_with_grouping(self):
        """Test creating a chart with grouping."""
        df = pd.DataFrame({"A": [1], "B": [2], "Group": ["G1"]})
        chart = StackedBarChart(
            title="Grouped Chart",
            data=df,
            groups_column="Group",
        )
        assert chart.groups_column == "Group"

    def test_create_with_negative_colors(self):
        """Test creating a chart with negative color configuration."""
        df = pd.DataFrame({"A": [1], "B": [-2]})
        chart = StackedBarChart(
            title="Negative Color Chart",
            data=df,
            negative_color="#ff0000",
        )
        assert chart.negative_color == "#ff0000"

    def test_create_with_all_options(self):
        """Test creating a chart with many options."""
        df = pd.DataFrame({"A": [1], "B": [2]})
        chart = StackedBarChart(
            title="Full Chart",
            data=df,
            intro="Test intro",
            byline="Test byline",
            source_name="Test source",
            source_url="https://example.com",
            color_category={"A": "#ff0000"},
            thick_bars=True,
            show_color_key=True,
            value_label_mode="diverging",
            stack_percentages=True,
            sort_bars=True,
            block_labels=True,
        )
        assert chart.intro == "Test intro"
        assert chart.thick_bars is True
        assert chart.value_label_mode == "diverging"
        assert chart.block_labels is True


class TestStackedBarChartSerialization:
    """Test serializing StackedBarChart to API format."""

    def test_serialize_minimal(self):
        """Test serializing a minimal chart."""
        df = pd.DataFrame({"A": [1], "B": [2]})
        chart = StackedBarChart(
            title="Test",
            data=df,
        )
        serialized = chart.model_dump(mode="json", by_alias=True, exclude_none=True)

        assert serialized["title"] == "Test"
        assert serialized["type"] == "d3-bars-stacked"
        assert "metadata" in serialized
        assert "visualize" in serialized["metadata"]

    def test_serialize_color_category(self):
        """Test that color_category is serialized correctly."""
        df = pd.DataFrame({"A": [1], "B": [2]})
        chart = StackedBarChart(
            title="Test",
            data=df,
            color_category={"Series A": "#ff0000", "Series B": "#00ff00"},
        )
        serialized = chart.model_dump(mode="json", by_alias=True, exclude_none=True)

        color_cat = serialized["metadata"]["visualize"]["color-category"]
        assert color_cat == {"map": {"Series A": "#ff0000", "Series B": "#00ff00"}}

    def test_serialize_replace_flags_enabled(self):
        """Test that replace_flags is serialized correctly when enabled."""
        df = pd.DataFrame({"A": [1], "B": [2]})
        chart = StackedBarChart(
            title="Test",
            data=df,
            replace_flags="4x3",
        )
        serialized = chart.model_dump(mode="json", by_alias=True, exclude_none=True)

        flags = serialized["metadata"]["visualize"]["replace-flags"]
        assert flags["enabled"] is True
        assert flags["style"] == "4x3"

    def test_serialize_replace_flags_disabled(self):
        """Test that replace_flags is serialized correctly when disabled."""
        df = pd.DataFrame({"A": [1], "B": [2]})
        chart = StackedBarChart(
            title="Test",
            data=df,
            replace_flags="off",
        )
        serialized = chart.model_dump(mode="json", by_alias=True, exclude_none=True)

        flags = serialized["metadata"]["visualize"]["replace-flags"]
        assert flags["enabled"] is False
        assert flags["style"] == ""

    def test_serialize_negative_color(self):
        """Test that negative color is serialized correctly."""
        df = pd.DataFrame({"A": [1], "B": [2]})
        chart = StackedBarChart(
            title="Test",
            data=df,
            negative_color="#ff0000",
        )
        serialized = chart.model_dump(mode="json", by_alias=True, exclude_none=True)

        neg_color = serialized["metadata"]["visualize"]["negativeColor"]
        assert neg_color["enabled"] is True
        assert neg_color["value"] == "#ff0000"

    def test_serialize_with_groups(self):
        """Test that groups_column is serialized to axes inside metadata."""
        df = pd.DataFrame({"A": [1], "B": [2]})
        chart = StackedBarChart(
            title="Test",
            data=df,
            groups_column="Description",
        )
        serialized = chart.model_dump(mode="json", by_alias=True, exclude_none=True)

        assert "axes" in serialized["metadata"]
        assert serialized["metadata"]["axes"]["groups"] == "Description"

    def test_serialize_describe_section(self):
        """Test that describe section is serialized correctly."""
        df = pd.DataFrame({"A": [1], "B": [2]})
        chart = StackedBarChart(
            title="Test",
            data=df,
            intro="Test intro",
            byline="Test byline",
            source_name="Test source",
            source_url="https://example.com",
            aria_description="Test aria",
        )
        serialized = chart.model_dump(mode="json", by_alias=True, exclude_none=True)

        describe = serialized["metadata"]["describe"]
        assert describe["intro"] == "Test intro"
        assert describe["byline"] == "Test byline"
        assert describe["source-name"] == "Test source"
        assert describe["source-url"] == "https://example.com"
        assert describe["aria-description"] == "Test aria"


class TestStackedBarChartParsing:
    """Test parsing StackedBarChart from API responses."""

    def test_parse_candy_sample(self):
        """Test parsing the candy.json sample."""
        chart_metadata = load_sample_json("candy.json")
        sample_csv = load_sample_csv("candy.csv")

        mock_client = Mock()
        mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"

        def mock_get(url):
            if url.endswith("/data"):
                return sample_csv
            return chart_metadata

        mock_client.get.side_effect = mock_get

        with patch("datawrapper.charts.base.Datawrapper", return_value=mock_client):
            chart = StackedBarChart.get("test-id", access_token="test-token")

            assert (
                chart.title
                == "Bounty &amp; Snickers are the two most controversial candy bars in Celebrations"
            )
            assert chart.chart_type == "d3-bars-stacked"
            assert chart.intro.startswith("Replies to the question")
            assert chart.byline == "Lisa Charlotte Muth, Datawrapper"
            assert chart.source_name == "YouGov, November 2017"
            assert chart.thick_bars is True
            assert chart.stack_percentages is True
            assert chart.sort_bars is True
            assert chart.sort_by == "I like them a lot"
            assert chart.base_color == 2
            assert chart.show_color_key is True
            assert chart.value_label_format == "0%"
            assert len(chart.color_category) > 0
            assert "I like them a lot" in chart.color_category

    def test_parse_capitals_sample(self):
        """Test parsing the capitals.json sample."""
        chart_metadata = load_sample_json("capitals.json")
        sample_csv = load_sample_csv("capitals.csv")

        mock_client = Mock()
        mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"

        def mock_get(url):
            if url.endswith("/data"):
                return sample_csv
            return chart_metadata

        mock_client.get.side_effect = mock_get

        with patch("datawrapper.charts.base.Datawrapper", return_value=mock_client):
            chart = StackedBarChart.get("test-id", access_token="test-token")

            assert chart.title == "How many live in the capital?"
            assert chart.intro.startswith("Share of population")
            assert chart.byline == "Lisa Charlotte Muth"
            assert chart.source_name == "UN Population Division"
            assert chart.replace_flags == "4x3"  # enabled with style 4x3
            assert chart.thick_bars is False
            assert chart.stack_percentages is False
            assert chart.sort_bars is True
            assert chart.sort_by == "share of people in capital"
            assert chart.base_color == 0
            assert chart.show_color_key is True
            assert chart.negative_color is None

    def test_parse_media_trust_sample(self):
        """Test parsing the media-trust.json sample."""
        chart_metadata = load_sample_json("media-trust.json")
        sample_csv = load_sample_csv("media-trust.csv")

        mock_client = Mock()
        mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"

        def mock_get(url):
            if url.endswith("/data"):
                return sample_csv
            return chart_metadata

        mock_client.get.side_effect = mock_get

        with patch("datawrapper.charts.base.Datawrapper", return_value=mock_client):
            chart = StackedBarChart.get("test-id", access_token="test-token")

            assert chart.title == "Trust in Media Reporting"
            assert (
                chart.intro
                == "Trust in Media Reporting regarding widely reported topics of 2015"
            )
            assert chart.source_name == "Infratest dimap"
            assert chart.thick_bars is True
            assert chart.stack_percentages is True
            assert chart.sort_bars is True
            assert chart.sort_by == "Low trust"
            assert chart.base_color == 2
            assert chart.reverse_order is True
            assert chart.value_label_mode == "diverging"
            assert chart.block_labels is True
            assert chart.show_color_key is True

    def test_parse_sugar_sample(self):
        """Test parsing the sugar.json sample."""
        chart_metadata = load_sample_json("sugar.json")
        sample_csv = load_sample_csv("sugar.csv")

        mock_client = Mock()
        mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"

        def mock_get(url):
            if url.endswith("/data"):
                return sample_csv
            return chart_metadata

        mock_client.get.side_effect = mock_get

        with patch("datawrapper.charts.base.Datawrapper", return_value=mock_client):
            chart = StackedBarChart.get("test-id", access_token="test-token")

            assert chart.title == "Six kinds of sugar in thirty kinds of food"
            assert chart.intro.startswith("Gram of sugar")
            assert chart.byline == "Lisa Charlotte Muth, Datawrapper"
            assert (
                chart.source_name
                == "United States Department of Agriculture Food Composition Databases"
            )
            assert chart.thick_bars is False
            assert chart.stack_percentages is False
            assert chart.sort_bars is False
            assert chart.sort_by == "Sucrose (Fructose+Glucose)"
            assert chart.base_color == 0
            assert chart.show_color_key is True
            assert chart.groups_column == "Description"  # From axes.groups
            assert chart.value_label_format == "0.[0]"


class TestStackedBarChartRoundTrip:
    """Test that serialization and parsing are consistent."""

    def test_roundtrip_candy(self):
        """Test roundtrip with candy sample."""
        chart_metadata = load_sample_json("candy.json")
        sample_csv = load_sample_csv("candy.csv")

        mock_client = Mock()
        mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"

        def mock_get(url):
            if url.endswith("/data"):
                return sample_csv
            return chart_metadata

        mock_client.get.side_effect = mock_get

        # Parse from API
        with patch("datawrapper.charts.base.Datawrapper", return_value=mock_client):
            chart = StackedBarChart.get("test-id", access_token="test-token")

        # Serialize back
        serialized = chart.model_dump(mode="json", by_alias=True, exclude_none=True)

        # Parse again
        chart_metadata2 = {
            "type": serialized["type"],
            "title": serialized["title"],
            "metadata": serialized["metadata"],
        }
        if "axes" in serialized:
            chart_metadata2["axes"] = serialized["axes"]

        def mock_get2(url):
            if url.endswith("/data"):
                return sample_csv
            return chart_metadata2

        mock_client.get.side_effect = mock_get2

        with patch("datawrapper.charts.base.Datawrapper", return_value=mock_client):
            chart2 = StackedBarChart.get("test-id", access_token="test-token")

        # Compare key fields
        assert chart.title == chart2.title
        assert chart.thick_bars == chart2.thick_bars
        assert chart.stack_percentages == chart2.stack_percentages
        assert chart.sort_bars == chart2.sort_bars
        assert chart.base_color == chart2.base_color
        assert chart.value_label_mode == chart2.value_label_mode

    def test_roundtrip_capitals(self):
        """Test roundtrip with capitals sample."""
        chart_metadata = load_sample_json("capitals.json")
        sample_csv = load_sample_csv("capitals.csv")

        mock_client = Mock()
        mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"

        def mock_get(url):
            if url.endswith("/data"):
                return sample_csv
            return chart_metadata

        mock_client.get.side_effect = mock_get

        with patch("datawrapper.charts.base.Datawrapper", return_value=mock_client):
            chart = StackedBarChart.get("test-id", access_token="test-token")

        serialized = chart.model_dump(mode="json", by_alias=True, exclude_none=True)

        chart_metadata2 = {
            "type": serialized["type"],
            "title": serialized["title"],
            "metadata": serialized["metadata"],
        }
        if "axes" in serialized:
            chart_metadata2["axes"] = serialized["axes"]

        def mock_get2(url):
            if url.endswith("/data"):
                return sample_csv
            return chart_metadata2

        mock_client.get.side_effect = mock_get2

        with patch("datawrapper.charts.base.Datawrapper", return_value=mock_client):
            chart2 = StackedBarChart.get("test-id", access_token="test-token")

        assert chart.replace_flags == chart2.replace_flags
        assert chart.stack_percentages == chart2.stack_percentages
        assert chart.sort_by == chart2.sort_by

    def test_roundtrip_media_trust(self):
        """Test roundtrip with media-trust sample."""
        chart_metadata = load_sample_json("media-trust.json")
        sample_csv = load_sample_csv("media-trust.csv")

        mock_client = Mock()
        mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"

        def mock_get(url):
            if url.endswith("/data"):
                return sample_csv
            return chart_metadata

        mock_client.get.side_effect = mock_get

        with patch("datawrapper.charts.base.Datawrapper", return_value=mock_client):
            chart = StackedBarChart.get("test-id", access_token="test-token")

        serialized = chart.model_dump(mode="json", by_alias=True, exclude_none=True)

        chart_metadata2 = {
            "type": serialized["type"],
            "title": serialized["title"],
            "metadata": serialized["metadata"],
        }
        if "axes" in serialized:
            chart_metadata2["axes"] = serialized["axes"]

        def mock_get2(url):
            if url.endswith("/data"):
                return sample_csv
            return chart_metadata2

        mock_client.get.side_effect = mock_get2

        with patch("datawrapper.charts.base.Datawrapper", return_value=mock_client):
            chart2 = StackedBarChart.get("test-id", access_token="test-token")

        assert chart.reverse_order == chart2.reverse_order
        assert chart.value_label_mode == chart2.value_label_mode
        assert chart.block_labels == chart2.block_labels

    def test_roundtrip_sugar(self):
        """Test roundtrip with sugar sample."""
        chart_metadata = load_sample_json("sugar.json")
        sample_csv = load_sample_csv("sugar.csv")

        mock_client = Mock()
        mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"

        def mock_get(url):
            if url.endswith("/data"):
                return sample_csv
            return chart_metadata

        mock_client.get.side_effect = mock_get

        with patch("datawrapper.charts.base.Datawrapper", return_value=mock_client):
            chart = StackedBarChart.get("test-id", access_token="test-token")

        serialized = chart.model_dump(mode="json", by_alias=True, exclude_none=True)

        chart_metadata2 = {
            "type": serialized["type"],
            "title": serialized["title"],
            "metadata": serialized["metadata"],
        }
        if "axes" in serialized:
            chart_metadata2["axes"] = serialized["axes"]

        def mock_get2(url):
            if url.endswith("/data"):
                return sample_csv
            return chart_metadata2

        mock_client.get.side_effect = mock_get2

        with patch("datawrapper.charts.base.Datawrapper", return_value=mock_client):
            chart2 = StackedBarChart.get("test-id", access_token="test-token")

        assert chart.groups_column == chart2.groups_column
        assert chart.value_label_format == chart2.value_label_format


class TestStackedBarChartCompatibility:
    """Test compatibility with original dataclass structure."""

    def test_has_all_original_fields(self):
        """Test that all original dataclass fields are present."""
        df = pd.DataFrame({"A": [1], "B": [2]})
        chart = StackedBarChart(title="Test", data=df)

        # Original fields from dataclass
        assert hasattr(chart, "chart_type")
        assert hasattr(chart, "color_category")
        assert hasattr(chart, "replace_flags")
        assert hasattr(chart, "sort_ranges")
        assert hasattr(chart, "thick_bars")
        assert hasattr(chart, "reverse_order")
        assert hasattr(chart, "value_label_format")
        assert hasattr(chart, "date_label_format")
        assert hasattr(chart, "intro")
        assert hasattr(chart, "byline")
        assert hasattr(chart, "source_name")
        assert hasattr(chart, "source_url")
        assert hasattr(chart, "aria_description")
        assert hasattr(chart, "range_value_labels")
        assert hasattr(chart, "groups_column")
        assert hasattr(chart, "show_color_key")
        assert hasattr(chart, "value_label_mode")

    def test_default_values_match_original(self):
        """Test that default values match the original dataclass."""
        df = pd.DataFrame({"A": [1], "B": [2]})
        chart = StackedBarChart(title="Test", data=df)

        assert chart.chart_type == "d3-bars-stacked"
        assert chart.color_category == {}
        assert chart.replace_flags == "off"
        assert chart.sort_ranges is False
        assert chart.thick_bars is False
        assert chart.reverse_order is False
        assert chart.value_label_format == ""
        assert chart.date_label_format == ""
        assert chart.intro == ""
        assert chart.byline == ""
        assert chart.source_name == ""
        assert chart.source_url == ""
        assert chart.aria_description == ""
        assert chart.range_value_labels == ""
        assert chart.groups_column is None
        assert chart.show_color_key is False
        assert chart.value_label_mode == "left"

    def test_can_import_from_charts(self):
        """Test that StackedBarChart can be imported from datawrapper.charts."""
        from datawrapper.charts import StackedBarChart as ImportedChart

        assert ImportedChart is StackedBarChart

    def test_can_import_from_main(self):
        """Test that StackedBarChart can be imported from datawrapper."""
        from datawrapper import StackedBarChart as ImportedChart

        assert ImportedChart is StackedBarChart

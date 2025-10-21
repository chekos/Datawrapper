"""Integration tests for ScatterPlot chart class."""

import json
from pathlib import Path
from unittest.mock import Mock, patch

import pandas as pd

from datawrapper.charts import ScatterPlot


# Helper functions to load sample data
def load_sample_json(filename: str) -> dict:
    """Load a sample JSON file from tests/samples/scatter/."""
    path = Path(__file__).parent.parent / "samples" / "scatter" / filename
    with open(path) as f:
        data = json.load(f)
        return data["chart"]["crdt"]["data"]


def load_sample_csv(filename: str) -> str:
    """Load a sample CSV file from tests/samples/scatter/."""
    path = Path(__file__).parent.parent / "samples" / "scatter" / filename
    # Read the file and convert tabs to commas if needed
    with open(path) as f:
        content = f.read()
        # Check if this is a tab-delimited file
        if "\t" in content.split("\n")[0]:
            # Convert tab-delimited to comma-delimited
            lines = content.split("\n")
            csv_lines = []
            for line in lines:
                if line.strip():
                    # Split by tab and rejoin with comma, quoting fields that contain commas
                    fields = line.split("\t")
                    quoted_fields = [
                        f'"{field}"' if "," in field else field for field in fields
                    ]
                    csv_lines.append(",".join(quoted_fields))
            return "\n".join(csv_lines)
        return content


class TestScatterPlotCreation:
    """Test creating ScatterPlot instances with various configurations."""

    def test_create_basic_chart(self):
        """Test creating a basic scatter plot."""
        df = pd.DataFrame(
            {
                "Country": ["USA", "China", "India"],
                "GDP": [60000, 15000, 7000],
                "Life Expectancy": [79, 76, 69],
            }
        )

        chart = ScatterPlot(
            title="GDP vs Life Expectancy",
            data=df,
            x_column="GDP",
            y_column="Life Expectancy",
        )

        assert chart.chart_type == "d3-scatter-plot"
        assert chart.title == "GDP vs Life Expectancy"
        assert chart.x_column == "GDP"
        assert chart.y_column == "Life Expectancy"

    def test_create_with_size_and_color(self):
        """Test creating a scatter plot with size and color columns."""
        df = pd.DataFrame(
            {
                "Country": ["USA", "China", "India"],
                "GDP": [60000, 15000, 7000],
                "Life Expectancy": [79, 76, 69],
                "Population": [330, 1400, 1380],
                "Region": ["Americas", "Asia", "Asia"],
            }
        )

        chart = ScatterPlot(
            title="GDP vs Life Expectancy",
            data=df,
            x_column="GDP",
            y_column="Life Expectancy",
            size="dynamic",
            size_column="Population",
            shape_column="Region",
        )

        assert chart.size == "dynamic"
        assert chart.size_column == "Population"
        assert chart.shape_column == "Region"

    def test_create_with_logarithmic_axes(self):
        """Test creating a scatter plot with logarithmic axes."""
        df = pd.DataFrame({"X": [1, 10, 100], "Y": [1, 10, 100]})

        chart = ScatterPlot(
            title="Log Scale Chart",
            data=df,
            x_column="X",
            y_column="Y",
            x_log=True,
            y_log=True,
        )

        assert chart.x_log is True
        assert chart.y_log is True

    def test_create_with_custom_ranges(self):
        """Test creating a scatter plot with custom axis ranges."""
        df = pd.DataFrame({"X": [1, 2, 3], "Y": [4, 5, 6]})

        chart = ScatterPlot(
            title="Custom Range Chart",
            data=df,
            x_column="X",
            y_column="Y",
            x_range=[0, 10],
            y_range=[0, 20],
            x_ticks=[0, 5, 10],
            y_ticks=[0, 10, 20],
        )

        assert chart.x_range == [0, 10]
        assert chart.y_range == [0, 20]
        assert chart.x_ticks == [0, 5, 10]
        assert chart.y_ticks == [0, 10, 20]

    def test_create_with_regression_line(self):
        """Test creating a scatter plot with a regression line."""
        df = pd.DataFrame({"X": [1, 2, 3, 4, 5], "Y": [2, 4, 6, 8, 10]})

        chart = ScatterPlot(
            title="Regression Chart",
            data=df,
            x_column="X",
            y_column="Y",
            regression=True,
            regression_method="linear",
        )

        assert chart.regression is True
        assert chart.regression_method == "linear"

    def test_create_with_size_legend(self):
        """Test creating a scatter plot with size legend configuration."""
        df = pd.DataFrame({"X": [1, 2, 3], "Y": [4, 5, 6], "Size": [100, 200, 300]})

        chart = ScatterPlot(
            title="Size Legend Chart",
            data=df,
            x_column="X",
            y_column="Y",
            size="dynamic",
            size_column="Size",
            show_size_legend=True,
            size_legend_position="above",
            size_legend_title_enabled=True,
            size_legend_title="Population",
        )

        assert chart.show_size_legend is True
        assert chart.size_legend_position == "above"
        assert chart.size_legend_title_enabled is True
        assert chart.size_legend_title == "Population"

    def test_create_with_tooltips(self):
        """Test creating a scatter plot with custom tooltips."""
        df = pd.DataFrame({"X": [1, 2, 3], "Y": [4, 5, 6]})

        chart = ScatterPlot(
            title="Tooltip Chart",
            data=df,
            x_column="X",
            y_column="Y",
            tooltip_enabled=True,
            tooltip_title="{{ X }}",
            tooltip_body="Value: {{ Y }}",
            tooltip_sticky=True,
        )

        assert chart.tooltip_enabled is True
        assert chart.tooltip_title == "{{ X }}"
        assert chart.tooltip_body == "Value: {{ Y }}"
        assert chart.tooltip_sticky is True

    def test_create_with_labels(self):
        """Test creating a scatter plot with labels."""
        df = pd.DataFrame({"X": [1, 2, 3], "Y": [4, 5, 6], "Label": ["A", "B", "C"]})

        chart = ScatterPlot(
            title="Labeled Chart",
            data=df,
            x_column="X",
            y_column="Y",
            label_column="Label",
            auto_labels=False,
            add_labels=["A", "C"],
            highlight_labeled=True,
        )

        assert chart.label_column == "Label"
        assert chart.auto_labels is False
        assert chart.add_labels == ["A", "C"]
        assert chart.highlight_labeled is True


class TestScatterPlotSerialization:
    """Test serialization of ScatterPlot to API format."""

    def test_serialize_basic_chart(self):
        """Test serializing a basic scatter plot."""
        df = pd.DataFrame({"X": [1, 2, 3], "Y": [4, 5, 6]})

        chart = ScatterPlot(
            title="Test Chart",
            data=df,
            x_column="X",
            y_column="Y",
        )

        serialized = chart.model_dump(by_alias=True)

        assert serialized["type"] == "d3-scatter-plot"
        assert serialized["title"] == "Test Chart"
        assert "axes" in serialized["metadata"]
        assert serialized["metadata"]["axes"]["x"] == "X"
        assert serialized["metadata"]["axes"]["y"] == "Y"

    def test_serialize_axes_objects(self):
        """Test that axes are serialized as nested objects."""
        df = pd.DataFrame({"X": [1, 2, 3], "Y": [4, 5, 6]})

        chart = ScatterPlot(
            title="Test Chart",
            data=df,
            x_column="X",
            y_column="Y",
            x_log=True,
            x_range=[0, 10],
            x_ticks=[0, 5, 10],
            y_log=False,
            y_range=[0, 20],
            y_ticks=[0, 10, 20],
        )

        serialized = chart.model_dump(by_alias=True)
        visualize = serialized["metadata"]["visualize"]

        assert "x-axis" in visualize
        assert visualize["x-axis"]["log"] is True
        assert visualize["x-axis"]["range"] == [0, 10]
        assert visualize["x-axis"]["ticks"] == [0, 5, 10]

        assert "y-axis" in visualize
        assert visualize["y-axis"]["log"] is False
        assert visualize["y-axis"]["range"] == [0, 20]
        assert visualize["y-axis"]["ticks"] == [0, 10, 20]

    def test_serialize_axis_formatting(self):
        """Test serialization of axis formatting fields."""
        df = pd.DataFrame({"X": [1, 2, 3], "Y": [4, 5, 6]})

        chart = ScatterPlot(
            title="Test Chart",
            data=df,
            x_column="X",
            y_column="Y",
            x_format="0a",
            x_position="bottom",
            x_grid_lines="on",
            y_format="0,0",
            y_position="top",
            y_grid_lines="off",
        )

        serialized = chart.model_dump(by_alias=True)
        visualize = serialized["metadata"]["visualize"]

        assert visualize["x-format"] == "0a"
        assert visualize["x-pos"] == "bottom"
        assert visualize["x-grid-lines"] == "on"
        assert visualize["y-format"] == "0,0"
        assert visualize["y-pos"] == "top"
        assert visualize["y-grid-lines"] == "off"

    def test_serialize_color_fields(self):
        """Test serialization of color-related fields."""
        df = pd.DataFrame({"X": [1, 2, 3], "Y": [4, 5, 6]})

        chart = ScatterPlot(
            title="Test Chart",
            data=df,
            x_column="X",
            y_column="Y",
            base_color="#ff0000",
            opacity=0.8,
            outlines=True,
            color_outline="#000000",
            show_color_key=True,
        )

        serialized = chart.model_dump(by_alias=True)
        visualize = serialized["metadata"]["visualize"]

        assert visualize["base-color"] == "#ff0000"
        assert visualize["opacity"] == 0.8
        assert visualize["outlines"] is True
        assert visualize["color-outline"] == "#000000"
        assert visualize["show-color-key"] is True

    def test_serialize_size_fields(self):
        """Test serialization of size-related fields."""
        df = pd.DataFrame({"X": [1, 2, 3], "Y": [4, 5, 6], "Size": [10, 20, 30]})

        chart = ScatterPlot(
            title="Test Chart",
            data=df,
            x_column="X",
            y_column="Y",
            size="dynamic",
            size_column="Size",
            fixed_size=10,
            max_size=50,
            responsive_symbol_size=True,
        )

        serialized = chart.model_dump(by_alias=True)
        visualize = serialized["metadata"]["visualize"]

        assert visualize["size"] == "dynamic"
        assert serialized["metadata"]["axes"]["size"] == "Size"
        assert visualize["fixed-size"] == 10
        assert visualize["max-size"] == 50
        assert visualize["responsive-symbol-size"] is True

    def test_serialize_size_legend(self):
        """Test serialization of size legend configuration."""
        df = pd.DataFrame({"X": [1, 2, 3], "Y": [4, 5, 6], "Size": [10, 20, 30]})

        chart = ScatterPlot(
            title="Test Chart",
            data=df,
            x_column="X",
            y_column="Y",
            size="dynamic",
            size_column="Size",
            show_size_legend=True,
            size_legend_position="above",
            legend_offset_x=10,
            legend_offset_y=20,
            size_legend_values_format="custom",
            size_legend_values=[10, 20, 30],
            size_legend_label_position="right",
            size_legend_label_format="0a",
            size_legend_title_enabled=True,
            size_legend_title="Population",
            size_legend_title_position="left",
            size_legend_title_width=150,
        )

        serialized = chart.model_dump(by_alias=True)
        visualize = serialized["metadata"]["visualize"]

        assert visualize["show-size-legend"] is True
        assert visualize["size-legend-position"] == "above"
        assert visualize["legend-offset-x"] == 10
        assert visualize["legend-offset-y"] == 20
        assert visualize["size-legend-values-setting"] == "custom"
        assert visualize["size-legend-values"] == [10, 20, 30]
        assert visualize["size-legend-label-position"] == "right"
        assert visualize["size-legend-label-format"] == "0a"
        assert visualize["size-legend-title-enabled"] is True
        assert visualize["size-legend-title"] == "Population"
        assert visualize["size-legend-title-position"] == "left"
        assert visualize["size-legend-title-width"] == 150

    def test_serialize_shape_fields(self):
        """Test serialization of shape-related fields."""
        df = pd.DataFrame({"X": [1, 2, 3], "Y": [4, 5, 6], "Shape": ["A", "B", "C"]})

        chart = ScatterPlot(
            title="Test Chart",
            data=df,
            x_column="X",
            y_column="Y",
            shape="dynamic",
            shape_column="Shape",
            fixed_shape="symbolSquare",
        )

        serialized = chart.model_dump(by_alias=True)
        visualize = serialized["metadata"]["visualize"]

        assert visualize["shape"] == "dynamic"
        assert serialized["metadata"]["axes"]["shape"] == "Shape"
        assert visualize["fixed-shape"] == "symbolSquare"

    def test_serialize_regression(self):
        """Test serialization of regression line settings."""
        df = pd.DataFrame({"X": [1, 2, 3], "Y": [4, 5, 6]})

        chart = ScatterPlot(
            title="Test Chart",
            data=df,
            x_column="X",
            y_column="Y",
            regression=True,
            regression_method="exponential",
        )

        serialized = chart.model_dump(by_alias=True)
        visualize = serialized["metadata"]["visualize"]

        assert visualize["regression"] is True
        assert visualize["regression-method"] == "exponential"

    def test_serialize_tooltip(self):
        """Test serialization of tooltip configuration."""
        df = pd.DataFrame({"X": [1, 2, 3], "Y": [4, 5, 6]})

        chart = ScatterPlot(
            title="Test Chart",
            data=df,
            x_column="X",
            y_column="Y",
            tooltip_enabled=True,
            tooltip_title="Title: {{ X }}",
            tooltip_body="Body: {{ Y }}",
            tooltip_sticky=True,
        )

        serialized = chart.model_dump(by_alias=True)
        visualize = serialized["metadata"]["visualize"]

        assert "tooltip" in visualize
        assert visualize["tooltip"]["enabled"] is True
        assert visualize["tooltip"]["title"] == "Title: {{ X }}"
        assert visualize["tooltip"]["body"] == "Body: {{ Y }}"
        assert visualize["tooltip"]["sticky"] is True
        assert visualize["tooltip"]["migrated"] is True

    def test_serialize_labeling(self):
        """Test serialization of labeling configuration."""
        df = pd.DataFrame({"X": [1, 2, 3], "Y": [4, 5, 6], "Label": ["A", "B", "C"]})

        chart = ScatterPlot(
            title="Test Chart",
            data=df,
            x_column="X",
            y_column="Y",
            label_column="Label",
            auto_labels=False,
            add_labels=["A", "C"],
            highlight_labeled=False,
        )

        serialized = chart.model_dump(by_alias=True)
        visualize = serialized["metadata"]["visualize"]

        assert serialized["metadata"]["axes"]["labels"] == "Label"
        assert visualize["auto-labels"] is False
        assert visualize["add-labels"] == ["A", "C"]
        assert visualize["highlight-labeled"] is False


class TestScatterPlotParsing:
    """Test parsing ScatterPlot from API responses."""

    def test_parse_automation_sample(self):
        """Test parsing the automation sample JSON."""
        chart_metadata = load_sample_json("automation.json")
        sample_csv = load_sample_csv("automation.csv")

        mock_client = Mock()
        mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"

        def mock_get(url):
            if url.endswith("/data"):
                return sample_csv
            return chart_metadata

        mock_client.get.side_effect = mock_get

        with patch("datawrapper.charts.base.Datawrapper", return_value=mock_client):
            chart = ScatterPlot.get("test-id", access_token="test-token")

            assert chart.chart_type == "d3-scatter-plot"
            assert chart.title == "Higher Risk of Job Automation in Lower Paying Jobs"
            assert chart.x_column == "prob"
            assert chart.y_column == "medWage"
            assert chart.size_column == "numbEmployed"
            assert chart.x_log is False
            assert chart.y_log is True
            assert chart.regression is True
            assert chart.regression_method == "exponential"

    def test_parse_elements_sample(self):
        """Test parsing the elements sample JSON."""
        chart_metadata = load_sample_json("elements.json")
        sample_csv = load_sample_csv("elements.csv")

        mock_client = Mock()
        mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"

        def mock_get(url):
            if url.endswith("/data"):
                return sample_csv
            return chart_metadata

        mock_client.get.side_effect = mock_get

        with patch("datawrapper.charts.base.Datawrapper", return_value=mock_client):
            chart = ScatterPlot.get("test-id", access_token="test-token")

            assert chart.chart_type == "d3-scatter-plot"
            assert chart.title == "When were chemical elements discovered?"
            assert chart.x_column == "Group"
            assert chart.y_column == "Period"
            assert chart.shape_column == "time range"
            assert chart.label_column == "Symbol"
            assert chart.fixed_size == 20
            assert chart.show_color_key is True

    def test_parse_german_students_sample(self):
        """Test parsing the german-students sample JSON."""
        chart_metadata = load_sample_json("german-students.json")
        sample_csv = load_sample_csv("german-students.csv")

        mock_client = Mock()
        mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"

        def mock_get(url):
            if url.endswith("/data"):
                return sample_csv
            return chart_metadata

        mock_client.get.side_effect = mock_get

        with patch("datawrapper.charts.base.Datawrapper", return_value=mock_client):
            chart = ScatterPlot.get("test-id", access_token="test-token")

            assert chart.chart_type == "d3-scatter-plot"
            assert chart.title == "What are the student cities in Germany?"
            assert chart.x_column == "students"
            assert chart.y_column == "percent"
            assert chart.size == "dynamic"
            assert chart.size_column == "students"
            assert chart.label_column == "city"
            assert chart.add_labels == ["Berlin", "Frankfurt am Main", "München"]
            assert chart.highlight_labeled is True

    def test_parse_life_expectancy_sample(self):
        """Test parsing the life-expectancy sample JSON."""
        chart_metadata = load_sample_json("life-expectancy.json")
        sample_csv = load_sample_csv("life-expectancy.csv")

        mock_client = Mock()
        mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"

        def mock_get(url):
            if url.endswith("/data"):
                return sample_csv
            return chart_metadata

        mock_client.get.side_effect = mock_get

        with patch("datawrapper.charts.base.Datawrapper", return_value=mock_client):
            chart = ScatterPlot.get("test-id", access_token="test-token")

            assert chart.chart_type == "d3-scatter-plot"
            assert (
                chart.title
                == "Every country has a higher life expectancy now than in 1800"
            )
            assert chart.x_column == "gdp"
            assert chart.y_column == "health"
            assert chart.size_column == "population"
            assert chart.label_column == "country"
            assert chart.x_log is True
            assert chart.y_log is False
            assert chart.auto_labels is False
            assert chart.show_color_key is False

    def test_parse_preserves_all_fields(self):
        """Test that parsing preserves all scatter-specific fields."""
        chart_metadata = load_sample_json("automation.json")
        sample_csv = load_sample_csv("automation.csv")

        mock_client = Mock()
        mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"

        def mock_get(url):
            if url.endswith("/data"):
                return sample_csv
            return chart_metadata

        mock_client.get.side_effect = mock_get

        with patch("datawrapper.charts.base.Datawrapper", return_value=mock_client):
            chart = ScatterPlot.get("test-id", access_token="test-token")

            # Verify key fields are preserved
            assert chart.opacity == 0.86
            assert chart.outlines is True
            assert chart.color_outline == "#fff"
            assert chart.show_color_key is True
            assert chart.max_size > 0
            assert chart.plot_height_mode == "fixed"
            assert chart.plot_height_fixed > 0


class TestScatterPlotRoundTrip:
    """Test round-trip serialization and parsing."""

    def test_round_trip_basic_chart(self):
        """Test that a chart can be serialized and parsed back."""
        df = pd.DataFrame({"X": [1, 2, 3], "Y": [4, 5, 6]})

        original = ScatterPlot(
            title="Test Chart",
            data=df,
            x_column="X",
            y_column="Y",
            x_log=True,
            y_range=[0, 10],
        )

        # Serialize
        serialized = original.model_dump(by_alias=True)

        # Parse back (simulating API response)
        chart_metadata = {
            "type": serialized["type"],
            "title": serialized["title"],
            "metadata": serialized["metadata"],
        }

        mock_csv = "X,Y\n1,4\n2,5\n3,6"

        mock_client = Mock()
        mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"

        def mock_get(url):
            if url.endswith("/data"):
                return mock_csv
            return chart_metadata

        mock_client.get.side_effect = mock_get

        with patch("datawrapper.charts.base.Datawrapper", return_value=mock_client):
            parsed = ScatterPlot.get("test-id", access_token="test-token")

            # Verify key fields match
            assert parsed.title == original.title
            assert parsed.x_column == original.x_column
            assert parsed.y_column == original.y_column
            assert parsed.x_log == original.x_log
            assert parsed.y_range == original.y_range

    def test_round_trip_with_all_options(self):
        """Test round-trip with many options set."""
        df = pd.DataFrame(
            {
                "X": [1, 2, 3],
                "Y": [4, 5, 6],
                "Size": [10, 20, 30],
                "Label": ["A", "B", "C"],
            }
        )

        original = ScatterPlot(
            title="Complex Chart",
            data=df,
            x_column="X",
            y_column="Y",
            size="dynamic",
            size_column="Size",
            label_column="Label",
            x_log=True,
            y_log=False,
            x_range=[0, 10],
            y_range=[0, 20],
            regression=True,
            regression_method="linear",
            opacity=0.8,
            outlines=True,
            show_size_legend=True,
            tooltip_enabled=True,
            tooltip_title="{{ Label }}",
            tooltip_body="X: {{ X }}, Y: {{ Y }}",
        )

        # Serialize
        serialized = original.model_dump(by_alias=True)

        # Parse back
        chart_metadata = {
            "type": serialized["type"],
            "title": serialized["title"],
            "metadata": serialized["metadata"],
        }

        mock_csv = "X,Y,Size,Label\n1,4,10,A\n2,5,20,B\n3,6,30,C"

        mock_client = Mock()
        mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"

        def mock_get(url):
            if url.endswith("/data"):
                return mock_csv
            return chart_metadata

        mock_client.get.side_effect = mock_get

        with patch("datawrapper.charts.base.Datawrapper", return_value=mock_client):
            parsed = ScatterPlot.get("test-id", access_token="test-token")

            # Verify fields match
            assert parsed.title == original.title
            assert parsed.x_column == original.x_column
            assert parsed.y_column == original.y_column
            assert parsed.size == original.size
            assert parsed.size_column == original.size_column
            assert parsed.label_column == original.label_column
            assert parsed.x_log == original.x_log
            assert parsed.y_log == original.y_log
            assert parsed.regression == original.regression
            assert parsed.regression_method == original.regression_method
            assert parsed.opacity == original.opacity
            assert parsed.outlines == original.outlines


class TestScatterPlotCompatibility:
    """Test compatibility with original dataclass implementation."""

    def test_metadata_structure_matches(self):
        """Test that the metadata structure matches the expected API format."""
        df = pd.DataFrame({"X": [1, 2, 3], "Y": [4, 5, 6]})

        chart = ScatterPlot(
            title="Test Chart",
            data=df,
            x_column="X",
            y_column="Y",
        )

        serialized = chart.model_dump(by_alias=True)

        # Check top-level structure
        assert "metadata" in serialized
        assert "visualize" in serialized["metadata"]
        assert "axes" in serialized["metadata"]

        # Check axes structure
        visualize = serialized["metadata"]["visualize"]
        assert "x-axis" in visualize
        assert "y-axis" in visualize
        assert isinstance(visualize["x-axis"], dict)
        assert isinstance(visualize["y-axis"], dict)

        # Check tooltip structure
        assert "tooltip" in visualize
        assert isinstance(visualize["tooltip"], dict)
        assert "migrated" in visualize["tooltip"]
        assert visualize["tooltip"]["migrated"] is True

    def test_can_import_from_main_package(self):
        """Test that ScatterPlot can be imported from main package."""
        from datawrapper import ScatterPlot as ImportedScatterPlot

        assert ImportedScatterPlot is ScatterPlot

"""Integration tests for Table class."""

import io
import json
from pathlib import Path
from unittest.mock import Mock, patch

import pandas as pd

from datawrapper import (
    BorderWidth,
    ColorStop,
    ColumnFormat,
    HeatMapContinuous,
    HeatMapSteps,
    MiniColumn,
    MiniLine,
    NumberFormat,
    Table,
    TableBodyRow,
    TableColumn,
    TableRow,
    TableTextStyle,
)


# Helper to load sample files
def load_sample_json(filename: str) -> dict:
    """Load a sample JSON file from tests/samples/table directory."""
    samples_dir = Path(__file__).parent.parent / "samples" / "table"
    with open(samples_dir / filename) as f:
        return json.load(f)


def load_sample_csv(filename: str) -> str:
    """Load a sample CSV file from tests/samples/table directory."""
    samples_dir = Path(__file__).parent.parent / "samples" / "table"
    with open(samples_dir / filename) as f:
        return f.read()


class TestTableChartCreation:
    """Tests for TableChart creation and serialization."""

    def test_create_basic_table_chart(self):
        """Test creating a basic area chart."""
        chart = Table(
            title="Test Table",
            data=pd.DataFrame(
                {
                    "year": ["2020", "2021", "2022"],
                    "Region A": [100, 120, 140],
                    "Region B": [80, 90, 100],
                }
            ),
        )

        assert chart.chart_type == "tables"
        assert chart.title == "Test Table"
        assert isinstance(chart.data, pd.DataFrame)

    def test_serialize_table_chart(self):
        """Test serializing a table chart."""
        chart = Table(
            title="Test Table",
            data=pd.DataFrame(
                {
                    "year": ["2020", "2021", "2022"],
                    "Region A": [100, 120, 140],
                    "Region B": [80, 90, 100],
                    "Region C": [60, 70, 75],
                }
            ),
            striped=True,
            searchable=True,
            rows_per_page=2,
        )

        serialized = chart.serialize_model()

        assert serialized["type"] == "tables"
        assert serialized["title"] == "Test Table"
        assert serialized["metadata"]["visualize"]["striped"] is True
        assert serialized["metadata"]["visualize"]["searchable"] is True
        assert serialized["metadata"]["visualize"]["perPage"] == 2


class TestTableChartGet:
    """Tests for TableChart.get() method."""

    def test_get_life_expectancy_sample(self):
        """Test get() with life_expectancy.json sample data (complex table with mini charts)."""
        # Load sample data
        sample_json = load_sample_json("life_expectancy.json")
        chart_metadata = sample_json["chart"]["crdt"]["data"]
        sample_csv = load_sample_csv("life_expectancy.csv")

        mock_client = Mock()
        mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"

        def mock_get(url):
            if url.endswith("/data"):
                return sample_csv
            return chart_metadata

        mock_client.get.side_effect = mock_get

        with patch("datawrapper.charts.base.Datawrapper", return_value=mock_client):
            chart = Table.get("563hg", access_token="test-token")

            # Verify chart type and title
            assert chart.chart_type == "tables"
            assert (
                chart.title
                == "Life expectancy in all countries increased since 1960, but with a different pace"
            )

            # Verify basic properties
            assert chart.searchable is True
            assert chart.striped is False
            assert chart.rows_per_page == 6
            assert chart.mobile_fallback is True

            # Verify sorting
            assert chart.sort_table is True
            assert chart.sort_by == "Increase between 1960 and 2016"
            assert chart.sort_direction == "asc"

            # Verify column properties
            country_col = next(
                col for col in chart.column_styles if col.name == "Country"
            )
            assert country_col.fixed_width is True
            assert country_col.width == 0.21

            bar_col = next(
                col
                for col in chart.column_styles
                if col.name == "Increase between 1960 and 2016"
            )
            assert bar_col.show_as_bar is True
            assert bar_col.bar_color == "#15607a"

            # verify custom colors
            continent_col = next(
                col for col in chart.column_styles if col.name == "Continent"
            )
            assert continent_col.custom_color is True
            assert continent_col.custom_color_background == {
                "Africa": "#FFCF90",
                "Asia": "#EF9278",
                "Europe": "#8dbbc1",
                "North America": "#86BA90",
                "Oceania": "#b989b0",
                "South America": "#92cdb2",
            }

            # verify column format
            col_fmts = chart.column_format
            increase_col = next(
                col
                for col in col_fmts
                if col.column == "Increase between 1960 and 2016"
            )
            assert increase_col.number_append == " years"

            # verify mini chart
            mini_charts = chart.mini_charts
            assert mini_charts[0].color == "#c71e1d"
            assert mini_charts[0].height == 40

    def test_get_museum_sample(self):
        """Test get() with museum.json sample data (table with bar chart)."""
        # Load sample data
        sample_json = load_sample_json("museums.json")
        chart_metadata = sample_json["chart"]["crdt"]["data"]
        sample_csv = load_sample_csv("museums.csv")

        mock_client = Mock()
        mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"

        def mock_get(url):
            if url.endswith("/data"):
                return sample_csv
            return chart_metadata

        mock_client.get.side_effect = mock_get

        with patch("datawrapper.charts.base.Datawrapper", return_value=mock_client):
            chart = Table.get("7Jgac", access_token="test-token")

            # Verify chart type and title
            assert chart.chart_type == "tables"
            assert chart.title == "The most visited art museums in the world"

            # Verify basic properties
            assert chart.searchable is True
            assert chart.striped is True
            assert chart.rows_per_page == 10
            assert chart.show_ranks is True

            # Verify column properties
            rank_col = next(col for col in chart.column_styles if col.name == "Rank")
            assert rank_col.show_on_mobile is False
            assert rank_col.show_on_desktop is False

            city_col = next(col for col in chart.column_styles if col.name == "City")
            assert city_col.replace_flags is True
            assert city_col.flag_style == "circle"
            assert city_col.style.color == "#989898"

            visitor_col = next(
                col for col in chart.column_styles if col.name == "Visitors in 2018"
            )
            assert visitor_col.format == "0.[0]a"


class TestTableChartIntegration:
    """Integration tests for Table chart workflows."""

    def test_round_trip_create_and_get(self):
        """Test creating a table chart and then fetching it back."""

        # Load CSV sample for initial chart creation
        csv_text = load_sample_csv("unemployment.csv")
        df = pd.read_csv(io.StringIO(csv_text))

        # Build column styles dynamically (all except 'Country')
        column_names = [col for col in df.columns if col.lower() != "country"]
        column_styles = [
            TableColumn(name=col, format=NumberFormat.PERCENT_ONE_DECIMAL)
            for col in column_names
        ]

        original_chart = Table(
            title="Unemployment rate in selected countries",
            intro="January-August 2020, sorted by the unemployment rate in January",
            source_name="OECD",
            source_url="data.oecd.org/unemp/unemployment-rate.htm",
            data=df,
            sort_table=True,
            sort_by="Jan",
            sort_direction="asc",
            rows_per_page=45,
            header_style=TableRow(
                border_bottom=BorderWidth.MEDIUM,
                style=TableTextStyle(font_size=0.9, bold=False),
            ),
            row_styles=[
                TableBodyRow(row_index=4, style=TableTextStyle(bold=True)),
                TableBodyRow(row_index=9, style=TableTextStyle(bold=True)),
            ],
            heatmap=HeatMapContinuous(
                legend=False,
                colors=[
                    "#feebe2",
                    "#fcc5c0",
                    "#fa9fb5",
                    "#f768a1",
                    "#c51b8a",
                    "#7a0177",
                ],
            ),
            column_styles=column_styles,
        )

        # Mock client for create/update
        mock_client = Mock()
        mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"
        mock_client.create_chart.return_value = {"id": "table-chart-id"}
        mock_client.update_chart.return_value = {"id": "table-chart-id"}

        # Create the chart
        with patch.object(original_chart, "_get_client", return_value=mock_client):
            original_chart.create(access_token="test-token")
            chart_id = original_chart.chart_id

        # Prepare mocked metadata for GET
        serialized = original_chart.serialize_model()
        mock_metadata = {
            "id": chart_id,
            "type": serialized["type"],
            "title": serialized["title"],
            "intro": serialized.get("intro"),
            "source_name": serialized.get("source_name"),
            "source_url": serialized.get("source_url"),
            "theme": serialized.get("theme", ""),
            "language": serialized.get("language", "en-US"),
            "metadata": serialized["metadata"],
        }

        # GET /data should return the CSV sample
        mock_csv = csv_text

        def mock_get(url):
            if url.endswith("/data"):
                return mock_csv
            return mock_metadata

        mock_client.get.side_effect = mock_get

        # Fetch the chart back
        with patch("datawrapper.charts.base.Datawrapper", return_value=mock_client):
            fetched_chart = Table.get(chart_id, access_token="test-token")

        # Verify fields match

        assert fetched_chart.title == original_chart.title
        assert fetched_chart.sort_table == original_chart.sort_table
        assert fetched_chart.sort_by == original_chart.sort_by
        assert fetched_chart.rows_per_page == original_chart.rows_per_page

        # Verify header style
        assert fetched_chart.header_style.border_bottom == BorderWidth.MEDIUM
        assert fetched_chart.header_style.style.font_size == 0.9

        # Verify row styles
        assert fetched_chart.row_styles[0].row_index == 4
        assert fetched_chart.row_styles[0].style.bold is True
        assert fetched_chart.row_styles[1].row_index == 9

        # Verify heatmap
        assert isinstance(fetched_chart.heatmap, HeatMapContinuous)
        assert fetched_chart.heatmap.legend is False
        assert fetched_chart.heatmap.colors == [
            ColorStop(color="#feebe2", position=0.0),
            ColorStop(color="#fcc5c0", position=0.2),
            ColorStop(color="#fa9fb5", position=0.4),
            ColorStop(color="#f768a1", position=0.6),
            ColorStop(color="#c51b8a", position=0.8),
            ColorStop(color="#7a0177", position=1.0),
        ]

        # Verify column styles
        for col in column_names:
            fetched_col = next(c for c in fetched_chart.column_styles if c.name == col)
            assert fetched_col.format == NumberFormat.PERCENT_ONE_DECIMAL


class TestTableColumnStyles:
    """Basic tests for column styles in Table charts."""

    def test_create_table_with_column_styles(self):
        df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})

        col_a = TableColumn(name="A", sortable=False, alignment="left")
        col_b = TableColumn(name="B", sortable=True, alignment="right")

        chart = Table(
            title="Styled Table",
            data=df,
            column_styles=[col_a, col_b],
        )

        assert chart.column_styles[0].name == "A"
        assert chart.column_styles[0].sortable is False
        assert chart.column_styles[0].alignment == "left"

        assert chart.column_styles[1].name == "B"
        assert chart.column_styles[1].sortable is True
        assert chart.column_styles[1].alignment == "right"

    def test_serialize_table_with_column_styles(self):
        df = pd.DataFrame({"A": [1], "B": [2]})

        col = TableColumn(name="A", sortable=False, alignment="center")

        chart = Table(
            title="Serialize Column Styles",
            data=df,
            column_styles=[col],
        )

        serialized = chart.serialize_model()
        columns = serialized["metadata"]["visualize"]["columns"]

        assert "A" in columns
        assert columns["A"]["sortable"] is False
        assert columns["A"]["alignment"] == "center"


class TestTableRowStyles:
    """Basic tests for row styles in Table charts."""

    def test_create_table_with_row_styles(self):
        df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})

        row0 = TableBodyRow(row_index=0, sticky=True)
        row1 = TableBodyRow(row_index=1, sticky=False)

        chart = Table(
            title="Row Styled Table",
            data=df,
            row_styles=[row0, row1],
        )

        assert chart.row_styles[0].row_index == 0
        assert chart.row_styles[0].sticky is True

        assert chart.row_styles[1].row_index == 1
        assert chart.row_styles[1].sticky is False

    def test_serialize_table_with_row_styles(self):
        df = pd.DataFrame({"A": [1, 2]})

        row0 = TableBodyRow(row_index=0, sticky=True)

        chart = Table(
            title="Serialize Row Styles",
            data=df,
            row_styles=[row0],
        )

        serialized = chart.serialize_model()
        rows = serialized["metadata"]["visualize"]["rows"]

        assert "row-0" in rows
        assert rows["row-0"]["sticky"] is True


class TestTableHeatmap:
    """Basic tests for heatmap support in Table charts."""

    def test_create_table_with_heatmap(self):
        df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})

        heatmap = HeatMapContinuous()

        chart = Table(
            title="Heatmap Table",
            data=df,
            heatmap=heatmap,
        )

        assert isinstance(chart.heatmap, HeatMapContinuous)

    def test_serialize_table_with_heatmap(self):
        df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})

        heatmap = HeatMapContinuous()

        chart = Table(
            title="Serialize Heatmap",
            data=df,
            heatmap=heatmap,
        )

        serialized = chart.serialize_model()
        visualize = serialized["metadata"]["visualize"]

        assert "heatmap" in visualize
        assert visualize["heatmap"]["enabled"] is True
        assert (
            visualize["legend"]["enabled"] is True
        )  # legend should be enabled by default

    def test_legend_can_be_disabled(self):
        df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})

        heatmap = HeatMapContinuous(legend=False)

        chart = Table(
            title="Serialize Heatmap",
            data=df,
            heatmap=heatmap,
        )

        serialized = chart.serialize_model()
        visualize = serialized["metadata"]["visualize"]
        assert "heatmap" in visualize
        assert visualize["heatmap"]["enabled"] is True
        assert visualize["legend"]["enabled"] is False

    def test_set_custom_stops(self):
        df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
        custom_stops = [None, 0.5, 1.2]
        heatmap = HeatMapSteps(stops="custom", stop_count=3, custom_stops=custom_stops)

        chart = Table(title="Serialize Heatmap", data=df, heatmap=heatmap)
        serialized = chart.serialize_model()
        visualize = serialized["metadata"]["visualize"]
        assert "heatmap" in visualize
        assert visualize["heatmap"]["stopCount"] == 3
        assert visualize["heatmap"]["stops"] == "custom"
        assert visualize["heatmap"]["mode"] == "discrete"
        for stop in custom_stops:
            assert stop in visualize["heatmap"]["customStops"]

    def test_disable_heatmap_on_individual_columns(self):
        df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})

        heatmap = HeatMapContinuous()

        chart = Table(
            title="Serialize Heatmap",
            data=df,
            heatmap=heatmap,
            column_styles=[TableColumn(name="B", heatmap=False)],
        )

        serialized = chart.serialize_model()
        visualize = serialized["metadata"]["visualize"]
        columns = visualize.get("columns")

        assert "heatmap" in visualize
        assert visualize["heatmap"]["enabled"] is True
        assert columns["A"]["heatmap"]["enabled"] is True
        assert columns["B"]["heatmap"]["enabled"] is False


class TestTableColumnFormat:
    """Basic tests for column-format support."""

    def test_serialize_column_format(self):
        df = pd.DataFrame({"A": [1, 2]})

        chart = Table(
            title="Format Table",
            data=df,
            column_format=[ColumnFormat(column="A", type="number", number_prepend="$")],
        )

        serialized = chart.serialize_model()
        fmt = serialized["metadata"]["data"]["column-format"]

        assert "A" in fmt
        assert fmt["A"]["type"] == "number"
        assert fmt["A"]["number-prepend"] == "$"


class TestTableMiniCharts:
    """Basic tests for mini chart support in Table charts."""

    def test_mini_chart_serialization_excludes_columns(self):
        mini = MiniLine(columns=["A", "B"], type="line", height=20, stroke=2)

        serialized = mini.serialize_model()

        # Columns must NOT appear in serialized output
        assert "columns" not in serialized

        # Other fields should appear
        assert serialized["type"] == "line"
        assert serialized["enabled"] is True
        assert serialized["height"] == 20
        assert serialized["stroke"] == 2

    def test_table_serializes_sparkline_to_each_column(self):
        df = pd.DataFrame({"A": [1], "B": [2]})

        mini = MiniLine(columns=["A", "B"], enabled=True, type="line")

        chart = Table(
            title="Sparkline Table",
            data=df,
            mini_charts=[mini],
        )

        serialized = chart.serialize_model()
        columns = serialized["metadata"]["visualize"]["columns"]

        # Both columns must have sparkline metadata
        assert "sparkline" in columns["A"]
        assert "sparkline" in columns["B"]

        assert columns["A"]["sparkline"]["type"] == "line"
        assert columns["B"]["sparkline"]["type"] == "line"

    def test_deserialize_grouped_sparkline_into_single_mini_chart(self):
        df = pd.DataFrame({"A": [1], "B": [2], "C": [3]})

        chart = Table(title="Deserialize Mini", data=df)

        # Fake serialized metadata with identical sparkline configs
        serialized = chart.serialize_model()
        serialized["metadata"]["visualize"]["columns"] = {
            "A": {"sparkline": {"enabled": True, "type": "line"}},
            "B": {"sparkline": {"enabled": True, "type": "line"}},
            "C": {"sparkline": {"enabled": True, "type": "line"}},
        }

        deserialized = Table.deserialize_model(serialized)
        mini_charts = deserialized["mini_charts"]
        # Should reconstruct ONE MiniLine
        assert len(mini_charts) == 1
        mini = mini_charts[0]

        assert isinstance(mini, MiniLine)
        assert mini.columns == ["A", "B", "C"]

    def test_deserialize_separate_sparklines_for_different_configs(self):
        df = pd.DataFrame({"A": [1], "B": [2], "C": [3]})

        chart = Table(title="Separate Mini", data=df)

        serialized = chart.serialize_model()
        serialized["metadata"]["visualize"]["columns"] = {
            "A": {"sparkline": {"enabled": True, "type": "line"}},
            "B": {"sparkline": {"enabled": True, "type": "columns"}},
            "C": {"sparkline": {"enabled": True, "type": "line"}},
        }

        deserialized = Table.deserialize_model(serialized)
        mini_charts = deserialized["mini_charts"]

        # Expect 2 mini charts:
        # - One MiniLine for A + C
        # - One MiniColumn for B
        assert len(mini_charts) == 2

        line_chart = next(mc for mc in mini_charts if isinstance(mc, MiniLine))
        col_chart = next(mc for mc in mini_charts if isinstance(mc, MiniColumn))

        assert sorted(line_chart.columns) == ["A", "C"]
        assert col_chart.columns == ["B"]

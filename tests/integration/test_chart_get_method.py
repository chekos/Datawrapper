"""Integration tests for chart get() method using sample data."""

import json
import os
from pathlib import Path
from unittest.mock import Mock, patch

import pandas as pd
import pytest

from datawrapper import BarChart, BaseChart


# Helper to load sample files
def load_sample_json(filename: str) -> dict:
    """Load a sample JSON file from tests/samples/bar directory."""
    samples_dir = Path(__file__).parent.parent / "samples" / "bar"
    with open(samples_dir / filename) as f:
        return json.load(f)


def load_sample_csv(filename: str) -> str:
    """Load a sample CSV file from tests/samples/bar directory."""
    samples_dir = Path(__file__).parent.parent / "samples" / "bar"
    with open(samples_dir / filename) as f:
        return f.read()


class TestBaseChartGet:
    """Tests for BaseChart.get() method."""

    def test_get_client_creation(self):
        """Test that get() creates a client with the provided token."""
        mock_metadata = {
            "id": "test-id",
            "type": "d3-bars",
            "title": "Test Chart",
            "metadata": {
                "data": {},
                "describe": {},
                "visualize": {},
                "publish": {"blocks": {}},
                "annotate": {},
            },
        }

        mock_csv = "a,b\n1,2"

        mock_client = Mock()
        mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"

        def mock_get(url):
            if url.endswith("/data"):
                return mock_csv
            return mock_metadata

        mock_client.get.side_effect = mock_get

        with patch("datawrapper.charts.base.Datawrapper", return_value=mock_client):
            chart = BaseChart.get("test-id", access_token="test-token")

            assert chart.chart_id == "test-id"
            assert chart._client == mock_client

    def test_get_with_environment_token(self):
        """Test get() uses environment variable for token."""
        mock_metadata = {
            "id": "test-id",
            "type": "d3-bars",
            "title": "Test Chart",
            "metadata": {
                "data": {},
                "describe": {},
                "visualize": {},
                "publish": {"blocks": {}},
                "annotate": {},
            },
        }

        mock_csv = "a,b\n1,2"

        mock_client = Mock()
        mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"

        def mock_get(url):
            if url.endswith("/data"):
                return mock_csv
            return mock_metadata

        mock_client.get.side_effect = mock_get

        with patch.dict(os.environ, {"DATAWRAPPER_ACCESS_TOKEN": "env-token"}):
            with patch(
                "datawrapper.charts.base.Datawrapper", return_value=mock_client
            ) as mock_dw:
                chart = BaseChart.get("test-id")

                mock_dw.assert_called_once_with(access_token="env-token")
                assert chart.chart_id == "test-id"

    def test_get_no_token_raises_error(self):
        """Test get() raises error when no token is available."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(
                ValueError, match="No Datawrapper access token provided"
            ):
                BaseChart.get("test-id")

    def test_get_api_error_handling(self):
        """Test get() handles API errors gracefully."""
        mock_client = Mock()
        mock_client.get.side_effect = Exception("API Error")
        mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"

        with patch("datawrapper.charts.base.Datawrapper", return_value=mock_client):
            with pytest.raises(Exception, match="Failed to fetch chart"):
                BaseChart.get("test-id", access_token="test-token")

    def test_get_invalid_response_type(self):
        """Test get() handles invalid response types."""
        mock_client = Mock()
        mock_client.get.return_value = "invalid response"  # Not a dict
        mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"

        with patch("datawrapper.charts.base.Datawrapper", return_value=mock_client):
            with pytest.raises(Exception, match="Failed to fetch chart"):
                BaseChart.get("test-id", access_token="test-token")

    def test_get_parses_common_fields(self):
        """Test get() correctly parses common chart fields."""
        mock_metadata = {
            "id": "test-chart-id",
            "type": "d3-bars",
            "title": "Test Chart Title",
            "theme": "datawrapper",
            "language": "en-US",
            "metadata": {
                "data": {
                    "transpose": False,
                    "vertical-header": True,
                    "horizontal-header": True,
                },
                "describe": {
                    "intro": "Test intro",
                    "source-name": "Test Source",
                    "source-url": "https://example.com",
                    "byline": "Test Author",
                    "aria-description": "Test description",
                    "hide-title": False,
                },
                "visualize": {
                    "dark-mode-invert": True,
                    "sharing": {"enabled": True, "url": "https://share.url"},
                },
                "publish": {
                    "autoDarkMode": True,
                    "force-attribution": False,
                    "blocks": {
                        "get-the-data": True,
                        "download-image": True,
                        "download-pdf": False,
                        "download-svg": False,
                        "embed": True,
                        "logo": {"enabled": True, "id": "logo-123"},
                    },
                },
                "annotate": {
                    "notes": "Test notes",
                    "byline": "Test Author",
                },
                "custom": {"key": "value"},
            },
        }

        mock_csv = "col1,col2\n1,2\n3,4"

        mock_client = Mock()
        mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"

        def mock_get(url):
            if url.endswith("/data"):
                return mock_csv
            return mock_metadata

        mock_client.get.side_effect = mock_get

        with patch("datawrapper.charts.base.Datawrapper", return_value=mock_client):
            chart = BaseChart.get("test-chart-id", access_token="test-token")

            # Verify common fields
            assert chart.chart_id == "test-chart-id"
            assert chart.chart_type == "d3-bars"
            assert chart.title == "Test Chart Title"
            assert chart.theme == "datawrapper"
            assert chart.language == "en-US"

            # Verify description fields
            assert chart.intro == "Test intro"
            assert chart.source_name == "Test Source"
            assert chart.source_url == "https://example.com"
            assert chart.byline == "Test Author"
            assert chart.aria_description == "Test description"
            assert chart.hide_title is False

            # Verify layout/publish fields
            assert chart.auto_dark_mode is True
            assert chart.dark_mode_invert is True
            assert chart.get_the_data is True
            assert chart.download_image is True
            assert chart.download_pdf is False
            assert chart.embed is True
            assert chart.logo is True
            assert chart.logo_id == "logo-123"
            assert chart.share_buttons is True
            assert chart.share_url == "https://share.url"

            # Verify custom fields
            assert chart.custom == {"key": "value"}

            # Verify data was parsed
            assert isinstance(chart.data, pd.DataFrame)
            assert len(chart.data) == 2
            assert list(chart.data.columns) == ["col1", "col2"]

    def test_get_with_empty_optional_fields(self):
        """Test get() handles empty optional fields correctly."""
        mock_metadata = {
            "id": "test-id",
            "type": "d3-bars",
            "title": "Test",
            "metadata": {
                "data": {},
                "describe": {},
                "visualize": {},
                "publish": {"blocks": {}},
                "annotate": {},
            },
        }

        mock_csv = "a,b\n1,2"

        mock_client = Mock()
        mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"

        def mock_get(url):
            if url.endswith("/data"):
                return mock_csv
            return mock_metadata

        mock_client.get.side_effect = mock_get

        with patch("datawrapper.charts.base.Datawrapper", return_value=mock_client):
            chart = BaseChart.get("test-id", access_token="test-token")

            # Should use default values
            assert chart.intro == ""
            assert chart.source_name == ""
            assert chart.byline == ""
            assert chart.auto_dark_mode is False
            assert chart.get_the_data is False


class TestBarChartGet:
    """Tests for BarChart.get() method using sample data."""

    def test_get_european_turnout_sample(self):
        """Test get() with european-turnout.json sample data."""
        # Load sample data
        sample_json = load_sample_json("european-turnout.json")
        chart_metadata = sample_json["chart"]["crdt"]["data"]

        # Note: The sample uses tab-separated values, need to handle that
        sample_csv = "Country\tTurnout\nMalta (2022)\t85.6\nTurkey (2023)\t87.0"

        mock_client = Mock()
        mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"

        def mock_get(url):
            if url.endswith("/data"):
                return sample_csv
            return chart_metadata

        mock_client.get.side_effect = mock_get

        with patch("datawrapper.charts.base.Datawrapper", return_value=mock_client):
            chart = BarChart.get("u3Jwc", access_token="test-token")

            # Verify chart type
            assert chart.chart_type == "d3-bars"
            assert (
                chart.title
                == "European countries with lowest &amp; highest voter turnout"
            )

            # Verify description fields
            assert chart.source_name == "Parties & Elections, 2024"
            assert chart.source_url == "http://www.parties-and-elections.eu/"
            assert chart.notes == "Voting is compulsory in Belgium."

            # Verify bar-specific fields
            assert chart.sort_bars is True
            assert chart.reverse_order is True
            assert chart.background is True
            assert chart.rules is True
            assert chart.thick is False
            assert chart.tick_position == "top"

            # Verify custom range
            assert chart.custom_range == ["", 100]

            # Verify highlighted series
            assert len(chart.highlighted_series) == 6
            assert "Malta (2022)" in chart.highlighted_series
            assert "Turkey (2023)" in chart.highlighted_series
            assert "Belgium (2024)" in chart.highlighted_series

            # Verify color category structure
            assert isinstance(chart.color_category, dict)
            assert len(chart.color_category) > 0
            assert "Malta (2022)" in chart.color_category
            assert chart.color_category["Malta (2022)"] == "#267c87"

            # Verify category labels
            assert isinstance(chart.category_labels, dict)
            assert len(chart.category_labels) > 0

            # Verify category order
            assert isinstance(chart.category_order, list)
            assert len(chart.category_order) == 11
            assert chart.category_order[0] == "Romania (2020)"
            assert chart.category_order[1] == "Malta (2022)"

            # Verify show color key
            assert chart.show_color_key is True

            # Verify label settings
            assert chart.label_alignment == "left"
            assert chart.block_labels is False
            assert chart.show_value_labels is True
            assert chart.value_label_alignment == "left"
            assert chart.value_label_format == "0.[0]%"

            # Verify replace flags
            assert chart.replace_flags == "off"

    def test_get_bar_chart_with_overlays(self):
        """Test get() correctly parses overlays."""
        mock_metadata = {
            "id": "test-id",
            "type": "d3-bars",
            "title": "Test",
            "metadata": {
                "data": {},
                "describe": {},
                "visualize": {
                    "overlays": [
                        {
                            "type": "value",
                            "to": "column1",
                            "from": "--zero-baseline--",
                            "color": "#ff0000",
                            "opacity": 0.5,
                        },
                        {
                            "type": "range",
                            "to": "column2",
                            "from": "column1",
                            "color": "#00ff00",
                            "pattern": "diagonal-up",
                        },
                    ]
                },
                "publish": {"blocks": {}},
                "annotate": {},
                "axes": {},
            },
        }

        mock_csv = "a,b\n1,2"

        mock_client = Mock()
        mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"

        def mock_get(url):
            if url.endswith("/data"):
                return mock_csv
            return mock_metadata

        mock_client.get.side_effect = mock_get

        with patch("datawrapper.charts.base.Datawrapper", return_value=mock_client):
            chart = BarChart.get("test-id", access_token="test-token")

            # Verify overlays were parsed
            assert len(chart.overlays) == 2

            # Check first overlay
            overlay1 = chart.overlays[0]
            assert overlay1.type == "value"
            assert overlay1.to_column == "column1"
            assert overlay1.color == "#ff0000"
            assert overlay1.opacity == 0.5

            # Check second overlay
            overlay2 = chart.overlays[1]
            assert overlay2.type == "range"
            assert overlay2.to_column == "column2"
            assert overlay2.from_column == "column1"
            assert overlay2.color == "#00ff00"
            assert overlay2.pattern == "diagonal-up"

    def test_get_bar_chart_with_custom_grid_lines(self):
        """Test get() correctly parses custom grid lines from comma-separated string."""
        mock_metadata = {
            "id": "test-id",
            "type": "d3-bars",
            "title": "Test",
            "metadata": {
                "data": {},
                "describe": {},
                "visualize": {
                    "custom-grid-lines": "0,25,50,75,100",
                },
                "publish": {"blocks": {}},
                "annotate": {},
                "axes": {},
            },
        }

        mock_csv = "a,b\n1,2"

        mock_client = Mock()
        mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"

        def mock_get(url):
            if url.endswith("/data"):
                return mock_csv
            return mock_metadata

        mock_client.get.side_effect = mock_get

        with patch("datawrapper.charts.base.Datawrapper", return_value=mock_client):
            chart = BarChart.get("test-id", access_token="test-token")

            # Verify grid lines were parsed correctly
            assert chart.custom_grid_lines == [0.0, 25.0, 50.0, 75.0, 100.0]

    def test_get_bar_chart_axes_configuration(self):
        """Test get() correctly parses axes configuration."""
        mock_metadata = {
            "id": "test-id",
            "type": "d3-bars",
            "title": "Test",
            "metadata": {
                "data": {},
                "describe": {},
                "visualize": {},
                "publish": {"blocks": {}},
                "annotate": {},
                "axes": {
                    "labels": "Country",
                    "bars": "Value",
                    "colors": "Category",
                    "groups": "Region",
                },
            },
        }

        mock_csv = "a,b\n1,2"

        mock_client = Mock()
        mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"

        def mock_get(url):
            if url.endswith("/data"):
                return mock_csv
            return mock_metadata

        mock_client.get.side_effect = mock_get

        with patch("datawrapper.charts.base.Datawrapper", return_value=mock_client):
            chart = BarChart.get("test-id", access_token="test-token")

            # Verify axes configuration
            assert chart.label_column == "Country"
            assert chart.bar_column == "Value"
            assert chart.color_column == "Category"
            assert chart.groups_column == "Region"

    def test_get_bar_chart_replace_flags_enabled(self):
        """Test get() correctly parses replace-flags when enabled."""
        mock_metadata = {
            "id": "test-id",
            "type": "d3-bars",
            "title": "Test",
            "metadata": {
                "data": {},
                "describe": {},
                "visualize": {
                    "replace-flags": {
                        "enabled": True,
                        "style": "4x3",
                    }
                },
                "publish": {"blocks": {}},
                "annotate": {},
                "axes": {},
            },
        }

        mock_csv = "a,b\n1,2"

        mock_client = Mock()
        mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"

        def mock_get(url):
            if url.endswith("/data"):
                return mock_csv
            return mock_metadata

        mock_client.get.side_effect = mock_get

        with patch("datawrapper.charts.base.Datawrapper", return_value=mock_client):
            chart = BarChart.get("test-id", access_token="test-token")

            # Verify replace flags
            assert chart.replace_flags == "4x3"

    def test_get_bar_chart_replace_flags_disabled(self):
        """Test get() correctly parses replace-flags when disabled."""
        mock_metadata = {
            "id": "test-id",
            "type": "d3-bars",
            "title": "Test",
            "metadata": {
                "data": {},
                "describe": {},
                "visualize": {
                    "replace-flags": {
                        "enabled": False,
                        "type": "4x3",
                    }
                },
                "publish": {"blocks": {}},
                "annotate": {},
                "axes": {},
            },
        }

        mock_csv = "a,b\n1,2"

        mock_client = Mock()
        mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"

        def mock_get(url):
            if url.endswith("/data"):
                return mock_csv
            return mock_metadata

        mock_client.get.side_effect = mock_get

        with patch("datawrapper.charts.base.Datawrapper", return_value=mock_client):
            chart = BarChart.get("test-id", access_token="test-token")

            # Verify replace flags defaults to "off" when disabled
            assert chart.replace_flags == "off"


class TestChartGetIntegration:
    """Integration tests for get() method workflows."""

    def test_round_trip_create_and_get(self):
        """Test creating a chart and then fetching it back."""
        original_chart = BarChart(
            title="Test Chart",
            data=pd.DataFrame({"Country": ["A", "B"], "Value": [10, 20]}),
            label_column="Country",
            bar_column="Value",
            sort_bars=True,
            background=True,
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

        mock_csv = "Country,Value\nA,10\nB,20"

        def mock_get(url):
            if url.endswith("/data"):
                return mock_csv
            return mock_metadata

        mock_client.get.side_effect = mock_get

        with patch("datawrapper.charts.base.Datawrapper", return_value=mock_client):
            fetched_chart = BarChart.get(chart_id, access_token="test-token")

            # Verify key fields match
            assert fetched_chart.title == original_chart.title
            assert fetched_chart.chart_type == original_chart.chart_type
            assert fetched_chart.sort_bars == original_chart.sort_bars
            assert fetched_chart.background == original_chart.background
            assert fetched_chart.label_column == original_chart.label_column
            assert fetched_chart.bar_column == original_chart.bar_column

    def test_get_modify_and_update(self):
        """Test fetching a chart, modifying it, and updating."""
        mock_metadata = {
            "id": "existing-chart-id",
            "type": "d3-bars",
            "title": "Original Title",
            "metadata": {
                "data": {},
                "describe": {"source-name": "Original Source"},
                "visualize": {"sort-bars": False},
                "publish": {"blocks": {}},
                "annotate": {},
                "axes": {},
            },
        }

        mock_csv = "a,b\n1,2"

        mock_client = Mock()
        mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"

        def mock_get(url):
            if url.endswith("/data"):
                return mock_csv
            return mock_metadata

        mock_client.get.side_effect = mock_get
        mock_client.update_chart.return_value = {"id": "existing-chart-id"}

        with patch("datawrapper.charts.base.Datawrapper", return_value=mock_client):
            # Fetch the chart
            chart = BarChart.get("existing-chart-id", access_token="test-token")

            assert chart.title == "Original Title"
            assert chart.source_name == "Original Source"
            assert chart.sort_bars is False

            # Modify it
            chart.title = "Updated Title"
            chart.source_name = "Updated Source"
            chart.sort_bars = True

            # Update it
            chart.update(access_token="test-token")

            # Verify update was called
            mock_client.update_chart.assert_called_once()
            call_args = mock_client.update_chart.call_args
            assert call_args[1]["chart_id"] == "existing-chart-id"
            assert call_args[1]["title"] == "Updated Title"

    def test_chart_type_mismatch_error(self):
        """Test that using wrong chart class raises error."""
        mock_metadata = {
            "id": "test-id",
            "type": "d3-lines",  # Line chart, not bar chart
            "title": "Test",
            "metadata": {
                "data": {},
                "describe": {},
                "visualize": {},
                "publish": {"blocks": {}},
                "annotate": {},
            },
        }

        mock_csv = "a,b\n1,2"

        mock_client = Mock()
        mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"

        def mock_get(url):
            if url.endswith("/data"):
                return mock_csv
            return mock_metadata

        mock_client.get.side_effect = mock_get

        with patch("datawrapper.charts.base.Datawrapper", return_value=mock_client):
            # Should raise error because chart is d3-lines but we're using BarChart
            with pytest.raises(Exception, match="Chart type mismatch"):
                BarChart.get("test-id", access_token="test-token")

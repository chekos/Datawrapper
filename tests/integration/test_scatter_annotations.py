"""Integration tests for ScatterPlot annotation deserialization.

Tests that ScatterPlot can correctly deserialize real-world chart configurations
with text annotations in dict format (UUID keys from API).
"""

import json
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from datawrapper.charts import ScatterPlot


@pytest.fixture
def policy_poll_json():
    """Load the policy-poll.json sample file."""
    sample_path = (
        Path(__file__).parent.parent / "samples" / "scatter" / "policy-poll.json"
    )
    with open(sample_path) as f:
        data = json.load(f)
        return data["chart"]["crdt"]["data"]


@pytest.fixture
def policy_poll_csv():
    """Load the policy-poll.csv sample file."""
    sample_path = (
        Path(__file__).parent.parent / "samples" / "scatter" / "policy-poll.csv"
    )
    with open(sample_path) as f:
        return f.read()


def test_scatter_plot_deserialize_with_text_annotations(
    policy_poll_json, policy_poll_csv
):
    """Test that ScatterPlot can deserialize a chart with text annotations in dict format."""
    mock_client = Mock()
    mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"

    def mock_get(url):
        if url.endswith("/data"):
            return policy_poll_csv
        return policy_poll_json

    mock_client.get.side_effect = mock_get

    with patch("datawrapper.charts.base.Datawrapper", return_value=mock_client):
        chart = ScatterPlot.get("test-id", access_token="test-token")

        # Verify the chart was created successfully
        assert chart is not None
        assert isinstance(chart, ScatterPlot)
        assert chart.title == "Which party has a better policy? &nbsp;&nbsp; (Copy)"


def test_scatter_plot_text_annotations_count(policy_poll_json, policy_poll_csv):
    """Test that all text annotations are correctly deserialized."""
    mock_client = Mock()
    mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"

    def mock_get(url):
        if url.endswith("/data"):
            return policy_poll_csv
        return policy_poll_json

    mock_client.get.side_effect = mock_get

    with patch("datawrapper.charts.base.Datawrapper", return_value=mock_client):
        chart = ScatterPlot.get("test-id", access_token="test-token")

        # Verify we have 4 text annotations
        assert len(chart.text_annotations) == 4


def test_scatter_plot_text_annotations_content(policy_poll_json, policy_poll_csv):
    """Test that text annotation properties are correctly deserialized."""
    mock_client = Mock()
    mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"

    def mock_get(url):
        if url.endswith("/data"):
            return policy_poll_csv
        return policy_poll_json

    mock_client.get.side_effect = mock_get

    with patch("datawrapper.charts.base.Datawrapper", return_value=mock_client):
        chart = ScatterPlot.get("test-id", access_token="test-token")

        # Get the annotation texts (annotations are TextAnnotation objects)
        annotation_texts = [anno.text for anno in chart.text_annotations]

        # Verify the expected annotations are present
        assert "Crime" in annotation_texts
        assert "Immigration" in annotation_texts
        assert "Respect for democracy" in annotation_texts
        assert "Cost of living" in annotation_texts


def test_scatter_plot_text_annotation_properties(policy_poll_json, policy_poll_csv):
    """Test that individual text annotation properties are correctly preserved."""
    mock_client = Mock()
    mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"

    def mock_get(url):
        if url.endswith("/data"):
            return policy_poll_csv
        return policy_poll_json

    mock_client.get.side_effect = mock_get

    with patch("datawrapper.charts.base.Datawrapper", return_value=mock_client):
        chart = ScatterPlot.get("test-id", access_token="test-token")

        # Find the "Crime" annotation (annotations are TextAnnotation objects)
        crime_anno = next(
            anno for anno in chart.text_annotations if anno.text == "Crime"
        )

        # Verify properties
        assert crime_anno.id == "aJXGEJA8Bj"
        assert crime_anno.bold is True
        assert crime_anno.size == 15
        assert crime_anno.align == "mc"
        assert crime_anno.color == "#404040"
        assert crime_anno.x == "4"
        assert crime_anno.y == "48"
        assert crime_anno.show_mobile is True
        assert crime_anno.show_desktop is True


def test_scatter_plot_text_annotation_connector_line(policy_poll_json, policy_poll_csv):
    """Test that connector line properties are correctly deserialized."""
    mock_client = Mock()
    mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"

    def mock_get(url):
        if url.endswith("/data"):
            return policy_poll_csv
        return policy_poll_json

    mock_client.get.side_effect = mock_get

    with patch("datawrapper.charts.base.Datawrapper", return_value=mock_client):
        chart = ScatterPlot.get("test-id", access_token="test-token")

        # Find the "Crime" annotation (annotations are TextAnnotation objects)
        crime_anno = next(
            anno for anno in chart.text_annotations if anno.text == "Crime"
        )

        # Verify connector line is disabled (enabled: false in API)
        assert crime_anno.connector_line is None


def test_scatter_plot_range_annotations(policy_poll_json, policy_poll_csv):
    """Test that range annotations are correctly handled (empty in this case)."""
    mock_client = Mock()
    mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"

    def mock_get(url):
        if url.endswith("/data"):
            return policy_poll_csv
        return policy_poll_json

    mock_client.get.side_effect = mock_get

    with patch("datawrapper.charts.base.Datawrapper", return_value=mock_client):
        chart = ScatterPlot.get("test-id", access_token="test-token")

        # Verify range annotations is an empty list (empty dict in API)
        assert chart.range_annotations == []


def test_scatter_plot_serialization_roundtrip(policy_poll_json, policy_poll_csv):
    """Test that serialization and deserialization maintain data integrity."""
    mock_client = Mock()
    mock_client._CHARTS_URL = "https://api.datawrapper.de/v3/charts"

    def mock_get(url):
        if url.endswith("/data"):
            return policy_poll_csv
        return policy_poll_json

    mock_client.get.side_effect = mock_get

    with patch("datawrapper.charts.base.Datawrapper", return_value=mock_client):
        chart = ScatterPlot.get("test-id", access_token="test-token")

        # Serialize
        serialized = chart.serialize_model()

        # Verify text annotations are present in serialized output
        assert "text-annotations" in serialized["metadata"]["visualize"]

        # Note: Serialization produces a list format, not dict format
        # This is expected behavior - the API accepts both formats
        text_annos = serialized["metadata"]["visualize"]["text-annotations"]
        assert isinstance(text_annos, list)
        assert len(text_annos) == 4

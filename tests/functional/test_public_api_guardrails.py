"""Guardrail tests for public API paths agents commonly modify."""

from unittest.mock import MagicMock, patch

import pytest

from datawrapper import BarChart, Datawrapper, get_chart


@pytest.mark.parametrize(
    ("metadata_type", "expected_error"),
    [
        (None, "has no type field in metadata"),
        ("", "has no type field in metadata"),
        ("unknown-chart-type", "Unsupported chart type: unknown-chart-type"),
    ],
)
def test_get_chart_rejects_missing_or_unsupported_chart_types(
    clean_env, metadata_type, expected_error
):
    """The typed chart factory must fail clearly instead of guessing a class."""
    mock_client = MagicMock(spec=Datawrapper)
    mock_client.get_chart.return_value = {
        "id": "chart-123",
        "title": "Unknown chart",
        "type": metadata_type,
        "metadata": {"visualize": {}},
    }

    with patch("datawrapper.Datawrapper", return_value=mock_client):
        with pytest.raises(ValueError, match=expected_error):
            get_chart("chart-123")

    mock_client.get_chart.assert_called_once_with("chart-123")


def test_get_chart_prefers_explicit_token_over_environment(env_with_token):
    """Explicit credentials should win over ambient environment state."""
    mock_client = MagicMock(spec=Datawrapper)
    mock_client.get_chart.return_value = {
        "id": "bar-123",
        "title": "Explicit token chart",
        "type": "d3-bars",
        "metadata": {"visualize": {}},
    }

    with (
        patch("datawrapper.Datawrapper", return_value=mock_client) as mock_dw_class,
        patch.object(
            BarChart, "get", return_value=BarChart(title="Explicit token chart")
        ) as mock_get,
    ):
        get_chart("bar-123", access_token="explicit-token")

    mock_dw_class.assert_called_once_with(access_token="explicit-token")
    mock_get.assert_called_once_with(chart_id="bar-123", access_token="explicit-token")


def test_get_chart_converts_empty_environment_token_to_none(monkeypatch):
    """An empty DATAWRAPPER_ACCESS_TOKEN should not be passed as a real token."""
    monkeypatch.setenv("DATAWRAPPER_ACCESS_TOKEN", "")
    mock_client = MagicMock(spec=Datawrapper)
    mock_client.get_chart.return_value = {
        "id": "bar-456",
        "title": "Empty token chart",
        "type": "d3-bars",
        "metadata": {"visualize": {}},
    }

    with (
        patch("datawrapper.Datawrapper", return_value=mock_client) as mock_dw_class,
        patch.object(
            BarChart, "get", return_value=BarChart(title="Empty token chart")
        ) as mock_get,
    ):
        get_chart("bar-456")

    mock_dw_class.assert_called_once_with(access_token=None)
    mock_get.assert_called_once_with(chart_id="bar-456", access_token=None)

"""Guardrail tests for public API paths agents commonly modify."""

from unittest.mock import MagicMock, patch

import pytest

from datawrapper import BarChart, BaseChart, Datawrapper, get_chart


@pytest.mark.parametrize(
    ("metadata_type", "expected_error"),
    [
        (None, "has no type field in metadata"),
        ("", "has no type field in metadata"),
    ],
)
def test_get_chart_rejects_missing_chart_types(
    clean_env, metadata_type, expected_error
):
    """The chart factory must fail clearly when metadata does not include a type."""
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


def test_get_chart_unsupported_type_returns_base_chart_with_warning(clean_env):
    """Unsupported types should use the BaseChart compatibility shim."""
    mock_client = MagicMock(spec=Datawrapper)
    mock_client.get_chart.return_value = {
        "id": "map-123",
        "title": "Unsupported map",
        "type": "d3-maps-choropleth",
        "metadata": {"visualize": {}},
    }

    with (
        patch("datawrapper.Datawrapper", return_value=mock_client),
        patch.object(
            BaseChart, "get", return_value=BaseChart(chart_type="d3-maps-choropleth")
        ) as mock_get,
    ):
        with pytest.warns(
            UserWarning, match="does not have a dedicated datawrapper class"
        ):
            result = get_chart("map-123")

    assert isinstance(result, BaseChart)
    assert result.chart_type == "d3-maps-choropleth"
    mock_get.assert_called_once_with(chart_id="map-123", access_token=None)


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

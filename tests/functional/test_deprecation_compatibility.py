"""Compatibility tests for legacy client method deprecations."""

import warnings
from unittest.mock import MagicMock, patch

import pytest

from datawrapper import BaseChart, Datawrapper


def test_update_chart_warning_documents_compatibility_for_maps():
    """Legacy updates should be deprecated only where a typed class exists."""
    client = Datawrapper()

    with patch.object(Datawrapper, "patch", return_value={"id": "map123"}):
        with pytest.warns(DeprecationWarning) as warnings_record:
            client.update_chart(
                "map123",
                chart_type="d3-maps-choropleth",
                metadata={"visualize": {"basemap": "world"}},
            )

    message = str(warnings_record[0].message)
    assert "deprecated for chart types with object-oriented classes" in message
    assert "maps, tables and other unsupported visualization types" in message
    assert "supported compatibility path" in message


def test_base_chart_accepts_unsupported_map_type_as_forward_compatible_shim():
    """BaseChart should support map types that lack a dedicated class."""
    chart = BaseChart(
        chart_type="d3-maps-choropleth",
        title="Map example",
        custom={"source": "issue-522"},
    )

    assert chart.chart_type == "d3-maps-choropleth"
    serialized = chart.serialize_model()
    assert serialized["type"] == "d3-maps-choropleth"
    assert serialized["title"] == "Map example"


def test_base_chart_preserves_raw_metadata_for_unsupported_types():
    """The fallback shim should not discard unsupported chart-specific settings."""
    parsed = BaseChart.deserialize_model(
        {
            "id": "map123",
            "title": "Map example",
            "type": "d3-maps-choropleth",
            "metadata": {
                "visualize": {
                    "basemap": "usa-states",
                    "colors": {"palette": "YlOrRd"},
                },
                "custom": {"source": "issue-522"},
            },
        }
    )
    chart = BaseChart(**parsed)

    serialized = chart.serialize_model()
    assert serialized["metadata"]["visualize"]["basemap"] == "usa-states"
    assert serialized["metadata"]["visualize"]["colors"] == {"palette": "YlOrRd"}
    assert serialized["metadata"]["custom"] == {"source": "issue-522"}


@pytest.mark.parametrize("method_name", ["create", "update", "publish"])
def test_base_chart_methods_do_not_emit_internal_legacy_warnings(method_name):
    """Object-oriented calls should not leak warnings from legacy client internals."""
    chart = BaseChart(chart_type="d3-maps-choropleth", title="Map example")
    chart._client = Datawrapper()

    if method_name == "create":

        def create_chart_with_warning(**kwargs):
            warnings.warn(
                "create_chart() is deprecated for chart types with object-oriented classes.",
                DeprecationWarning,
                stacklevel=2,
            )
            return {"id": "map123"}

        mock_method = MagicMock(side_effect=create_chart_with_warning)
        with patch.object(Datawrapper, "create_chart", mock_method):
            with warnings.catch_warnings(record=True) as warnings_record:
                warnings.simplefilter("always")
                chart.create()
        assert chart.chart_id == "map123"
    elif method_name == "update":
        chart.chart_id = "map123"

        def update_chart_with_warning(**kwargs):
            warnings.warn(
                "update_chart() is deprecated for chart types with object-oriented classes.",
                DeprecationWarning,
                stacklevel=2,
            )
            return {"id": "map123"}

        mock_method = MagicMock(side_effect=update_chart_with_warning)
        with patch.object(Datawrapper, "update_chart", mock_method):
            with warnings.catch_warnings(record=True) as warnings_record:
                warnings.simplefilter("always")
                chart.update()
    else:
        chart.chart_id = "map123"

        def publish_chart_with_warning(**kwargs):
            warnings.warn(
                "publish_chart() is deprecated for chart types with object-oriented classes.",
                DeprecationWarning,
                stacklevel=2,
            )
            return {"ok": True}

        mock_method = MagicMock(side_effect=publish_chart_with_warning)
        with patch.object(Datawrapper, "publish_chart", mock_method):
            with warnings.catch_warnings(record=True) as warnings_record:
                warnings.simplefilter("always")
                chart.publish()

    mock_method.assert_called_once()
    assert not warnings_record

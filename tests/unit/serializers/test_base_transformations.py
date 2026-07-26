"""Tests for BaseChart's high-level transformation fields."""

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

import datawrapper


def serialized_data(chart: datawrapper.BaseChart) -> dict:
    """Return the Datawrapper metadata.data section for a chart."""
    return chart.serialize_model()["metadata"]["data"]


def test_base_chart_accepts_flat_transformation_fields():
    """Top-level fields serialize into metadata.data without a Transform wrapper."""
    chart = datawrapper.BaseChart(
        chart_type="d3-lines",
        title="Flat transformations",
        transpose=True,
        column_order=[2, 1, 0],
        column_format=[
            datawrapper.ColumnFormat(
                column="sales",
                type="number",
                number_prepend="$",
            )
        ],
        changes=[
            datawrapper.DataChange(
                row=9,
                column=3,
                value="1.7",
                time=1573134075869,
                previous="0.7",
            )
        ],
        external_data="https://example.com/data.csv",
        use_datawrapper_cdn=False,
        upload_method="external-data",
    )

    data = serialized_data(chart)

    assert data["transpose"] is True
    assert data["column-order"] == [2, 1, 0]
    assert data["column-format"] == {"sales": {"type": "number", "number-prepend": "$"}}
    assert data["changes"] == [
        {
            "row": 9,
            "column": 3,
            "value": "1.7",
            "time": 1573134075869,
            "previous": "0.7",
        }
    ]
    assert data["external-data"] == "https://example.com/data.csv"
    assert data["use-datawrapper-cdn"] is False
    assert data["upload-method"] == "external-data"
    assert chart.transformations.transpose is True
    assert chart.transformations.column_order == [2, 1, 0]
    assert chart.transformations.external_data == "https://example.com/data.csv"


def test_flat_column_format_accepts_api_shaped_fixture():
    """Real sample metadata.data column-format maps work at top level too.

    The existing ColumnFormat serializer normalizes away default values from API
    samples, so this asserts the substantive non-default setting is preserved.
    """
    fixture_path = Path(__file__).parents[2] / "samples" / "line" / "land-temps.json"
    fixture = json.loads(fixture_path.read_text())
    data = fixture["chart"]["crdt"]["data"]["metadata"]["data"]

    chart = datawrapper.BaseChart(
        chart_type="d3-lines",
        title="Academy sample",
        column_format=data["column-format"],
    )

    assert serialized_data(chart)["column-format"] == {
        "LandAverageTemperature": {"number-append": " °C"}
    }


def test_flat_transformation_fields_compose_with_nested_defaults():
    """Flat values can fill unset/default nested Transform settings."""
    chart = datawrapper.BaseChart(
        chart_type="d3-lines",
        title="Composed transformations",
        transformations=datawrapper.Transform(column_order=[0, 1, 2]),
        column_format=[{"column": "sales", "type": "number"}],
    )

    data = serialized_data(chart)

    assert data["column-order"] == [0, 1, 2]
    assert data["column-format"] == {"sales": {"type": "number"}}


def test_matching_flat_and_nested_transformation_values_are_accepted():
    """Supplying both forms is okay when the overlapping values match."""
    chart = datawrapper.BaseChart(
        chart_type="d3-lines",
        title="Matching transformations",
        transformations={"transpose": True},
        transpose=True,
    )

    assert chart.transformations.transpose is True
    assert serialized_data(chart)["transpose"] is True


def test_flat_transformation_assignment_updates_nested_transformations():
    """Assignment keeps updates and serialization pointed at metadata.data."""
    chart = datawrapper.BaseChart(
        chart_type="d3-lines",
        title="Updated transformations",
    )

    chart.transpose = True
    chart.column_order = [1, 0]

    assert chart.transformations.transpose is True
    assert chart.transformations.column_order == [1, 0]
    assert serialized_data(chart)["transpose"] is True
    assert serialized_data(chart)["column-order"] == [1, 0]


def test_conflicting_flat_and_nested_transformation_values_raise_validation_error():
    """Conflicts fail instead of silently preferring flat or nested input."""
    with pytest.raises(ValidationError, match="Conflicting transformation values"):
        datawrapper.BaseChart(
            chart_type="d3-lines",
            title="Conflicting transformations",
            transformations={"transpose": True},
            transpose=False,
        )


def test_api_response_deserialization_keeps_nested_transform_only():
    """API-shaped input remains represented by transformations for round trips."""
    api_response = {
        "id": "abc123",
        "type": "d3-lines",
        "title": "API chart",
        "language": "en-US",
        "theme": "datawrapper",
        "metadata": {
            "data": {
                "transpose": True,
                "vertical-header": True,
                "horizontal-header": True,
                "column-format": {"sales": {"type": "number"}},
                "upload-method": "copy",
            },
            "describe": {},
            "annotate": {},
            "visualize": {},
            "publish": {"blocks": {}},
        },
    }

    parsed = datawrapper.BaseChart.deserialize_model(api_response)
    chart = datawrapper.BaseChart(**parsed)

    assert chart.transpose is None
    assert chart.transformations.transpose is True
    assert serialized_data(chart)["column-format"] == {"sales": {"type": "number"}}

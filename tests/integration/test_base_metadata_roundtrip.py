"""Round-trip tests for the metadata sections that BaseChart serializes.

Fetching a chart and saving it again without changes must not alter the
``describe``, ``publish``, ``annotate`` or ``visualize.sharing`` settings
that came back from the API, including keys BaseChart does not model.
"""

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

import pytest
from pydantic import ValidationError

from datawrapper import (
    AreaChart,
    ArrowChart,
    BarChart,
    BaseChart,
    ColumnChart,
    LineChart,
    MultipleColumnChart,
    ScatterPlot,
    StackedBarChart,
)

SAMPLES_DIR = Path(__file__).parent.parent / "samples"

SAMPLE_CLASSES: dict[str, type[BaseChart]] = {
    "area": AreaChart,
    "arrow": ArrowChart,
    "bar": BarChart,
    "column": ColumnChart,
    "line": LineChart,
    "multiple_column": MultipleColumnChart,
    "scatter": ScatterPlot,
    "stacked_bar": StackedBarChart,
}

SAMPLE_PATHS = sorted(
    path for folder in SAMPLE_CLASSES for path in (SAMPLES_DIR / folder).glob("*.json")
)

# These samples store annotation numbers as strings or floats ("opacity": "10",
# "dy": -29.5). The typed annotation models accept them on load but reject them
# when the chart is serialized again, a separate bug from the one tested here.
TYPED_ANNOTATION_FAILURES = {
    "area/migration",
    "area/plastic",
    "area/population",
    "line/covid",
    "line/crypto",
}


def sample_id(path: Path) -> str:
    """Name a sample by its folder and file stem, e.g. ``bar/happiness-scores``."""
    return f"{path.parent.name}/{path.stem}"


def typed_sample_params() -> list:
    """Typed-class cases, marking the known annotation failures as xfail."""
    params = []
    for path in SAMPLE_PATHS:
        marks = []
        if sample_id(path) in TYPED_ANNOTATION_FAILURES:
            marks.append(
                pytest.mark.xfail(
                    raises=ValidationError,
                    strict=True,
                    reason="annotation numbers stored as strings or floats",
                )
            )
        params.append(pytest.param(path, id=sample_id(path), marks=marks))
    return params


def load_sample(path: Path) -> dict[str, Any]:
    """Load the chart metadata stored in a sample file."""
    with open(path, encoding="utf-8") as f:
        return json.load(f)["chart"]["crdt"]["data"]


def roundtrip(chart_class: type[BaseChart], api_response: dict) -> dict:
    """Parse an API response and serialize it back, as get() then update() do."""
    chart = chart_class(**chart_class.deserialize_model(api_response))
    return chart.serialize_model()["metadata"]


def assert_preserved(source: Any, result: Any, path: str) -> None:
    """Assert every value in ``source`` survives unchanged in ``result``."""
    if isinstance(source, dict):
        assert isinstance(result, dict), f"{path} is no longer a dict"
        for key, value in source.items():
            assert key in result, f"{path}.{key} was dropped"
            assert_preserved(value, result[key], f"{path}.{key}")
    else:
        assert result == source, f"{path} changed from {source!r} to {result!r}"


def assert_common_sections_preserved(source: dict, result: dict) -> None:
    """Check the sections BaseChart rebuilds from its own fields."""
    for section in ("describe", "publish", "annotate"):
        assert_preserved(source.get(section, {}), result[section], section)
    assert_preserved(
        source.get("visualize", {}).get("sharing", {}),
        result["visualize"]["sharing"],
        "visualize.sharing",
    )


@pytest.mark.parametrize("sample_path", SAMPLE_PATHS, ids=sample_id)
def test_base_chart_roundtrip_preserves_common_sections(sample_path):
    """Real samples keep their describe, publish, annotate and sharing settings."""
    api_response = load_sample(sample_path)

    result = roundtrip(BaseChart, api_response)

    assert_common_sections_preserved(api_response["metadata"], result)


@pytest.mark.parametrize("sample_path", typed_sample_params())
def test_typed_chart_roundtrip_preserves_common_sections(sample_path):
    """Typed chart classes inherit the same guarantee from BaseChart."""
    api_response = load_sample(sample_path)
    chart_class = SAMPLE_CLASSES[sample_path.parent.name]

    result = roundtrip(chart_class, api_response)

    assert_common_sections_preserved(api_response["metadata"], result)


def test_roundtrip_preserves_number_formatting():
    """Number formatting set in the Datawrapper editor survives a round trip."""
    api_response = deepcopy(load_sample(SAMPLES_DIR / "bar" / "happiness-scores.json"))
    api_response["metadata"]["describe"].update(
        {
            "number-format": "0.0%",
            "number-divisor": 3,
            "number-prepend": "$",
            "number-append": " mil",
        }
    )

    for chart_class in (BaseChart, BarChart):
        describe = roundtrip(chart_class, api_response)["describe"]

        assert describe["number-format"] == "0.0%"
        assert describe["number-divisor"] == 3
        assert describe["number-prepend"] == "$"
        assert describe["number-append"] == " mil"


def test_roundtrip_keeps_unmodeled_publish_blocks():
    """Publish blocks BaseChart does not model are kept, not replaced wholesale."""
    api_response = load_sample(SAMPLES_DIR / "column" / "unemployment.json")
    assert "edit-in-datawrapper" in api_response["metadata"]["publish"]["blocks"]

    blocks = roundtrip(BaseChart, api_response)["publish"]["blocks"]

    assert (
        blocks["edit-in-datawrapper"]
        == api_response["metadata"]["publish"]["blocks"]["edit-in-datawrapper"]
    )


def test_typed_fields_still_override_raw_metadata():
    """Values set on the model win over the metadata it was loaded from."""
    api_response = load_sample(SAMPLES_DIR / "bar" / "happiness-scores.json")
    chart = BarChart(**BarChart.deserialize_model(api_response))
    chart.intro = "New intro"
    chart.share_buttons = not chart.share_buttons
    chart.logo = True
    chart.logo_id = "red"

    metadata = chart.serialize_model()["metadata"]

    assert metadata["describe"]["intro"] == "New intro"
    assert metadata["visualize"]["sharing"]["enabled"] is chart.share_buttons
    assert metadata["publish"]["blocks"]["logo"] == {"id": "red", "enabled": True}


def test_new_chart_still_serializes_section_defaults():
    """Charts built from scratch keep emitting the documented section defaults."""
    metadata = BaseChart(chart_type="d3-pies", title="New").serialize_model()[
        "metadata"
    ]

    assert metadata["describe"]["number-format"] == "-"
    assert metadata["describe"]["number-divisor"] == 0
    assert metadata["visualize"]["sharing"] == {
        "enabled": False,
        "url": "",
        "auto": False,
    }

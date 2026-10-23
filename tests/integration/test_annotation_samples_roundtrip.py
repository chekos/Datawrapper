"""Real samples whose annotations store numbers as strings or floats.

The Datawrapper editor saves some annotation numbers as strings
("opacity": "10", "dx": "3") or with decimals ("dy": -29.5). These charts
must serialize again after being fetched, or get() then update() fails.
"""

import json
from pathlib import Path

import pytest

from datawrapper import AreaChart, LineChart

SAMPLES_DIR = Path(__file__).parent.parent / "samples"


def load_sample(folder: str, name: str) -> dict:
    """Load the chart metadata stored in a sample file."""
    with open(SAMPLES_DIR / folder / f"{name}.json", encoding="utf-8") as f:
        return json.load(f)["chart"]["crdt"]["data"]


def source_annotations(api_response: dict, key: str) -> list[dict]:
    """Annotations from an API response, which keys them by id."""
    annotations = api_response["metadata"]["visualize"].get(key) or {}
    return list(annotations.values()) if isinstance(annotations, dict) else annotations


@pytest.mark.parametrize(
    ("chart_class", "folder", "name"),
    [
        (AreaChart, "area", "migration"),
        (AreaChart, "area", "plastic"),
        (AreaChart, "area", "population"),
        (LineChart, "line", "covid"),
        (LineChart, "line", "crypto"),
    ],
)
def test_fetched_chart_with_annotations_serializes(chart_class, folder, name):
    api_response = load_sample(folder, name)
    chart = chart_class(**chart_class.deserialize_model(api_response))

    visualize = chart.serialize_model()["metadata"]["visualize"]

    for key in ("text-annotations", "range-annotations"):
        assert len(visualize[key]) == len(source_annotations(api_response, key))


def test_annotation_numbers_keep_their_values():
    covid = load_sample("line", "covid")
    chart = LineChart(**LineChart.deserialize_model(covid))
    source_dys = sorted(a["dy"] for a in source_annotations(covid, "text-annotations"))

    text_annotations = chart.serialize_model()["metadata"]["visualize"][
        "text-annotations"
    ]

    assert sorted(a["dy"] for a in text_annotations) == source_dys
    assert -29.5 in source_dys

    migration = load_sample("area", "migration")
    chart = AreaChart(**AreaChart.deserialize_model(migration))
    source_opacities = sorted(
        int(a["opacity"]) for a in source_annotations(migration, "range-annotations")
    )

    range_annotations = chart.serialize_model()["metadata"]["visualize"][
        "range-annotations"
    ]

    assert sorted(a["opacity"] for a in range_annotations) == source_opacities

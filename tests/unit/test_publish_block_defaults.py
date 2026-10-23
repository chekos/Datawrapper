"""Publish blocks that weren't set are left out, so team and theme defaults apply."""

import pandas as pd

from datawrapper import BarChart, BaseChart

DATA = pd.DataFrame({"x": ["a", "b"], "y": [1, 2]})


def blocks(chart: BaseChart) -> dict:
    return chart.serialize_model()["metadata"]["publish"]["blocks"]


def test_new_chart_sends_no_blocks():
    """A theme that shows a logo by default keeps it on a chart made from code."""
    assert blocks(BaseChart(**{"chart-type": "d3-bars", "data": DATA})) == {}


def test_typed_chart_sends_no_blocks():
    assert blocks(BarChart(title="Bars", data=DATA)) == {}


def test_logo_is_sent_when_set():
    chart = BaseChart(**{"chart-type": "d3-bars", "data": DATA, "logo": True})
    assert blocks(chart) == {"logo": {"enabled": True}}

    chart = BaseChart(
        **{"chart-type": "d3-bars", "data": DATA, "logo": True, "logo_id": "red"}
    )
    assert blocks(chart) == {"logo": {"id": "red", "enabled": True}}


def test_turning_the_logo_off_is_sent():
    chart = BaseChart(**{"chart-type": "d3-bars", "data": DATA, "logo": False})
    assert blocks(chart) == {"logo": {"enabled": False}}


def test_only_the_set_footer_blocks_are_sent():
    chart = BaseChart(**{"chart-type": "d3-bars", "data": DATA, "get_the_data": True})
    assert blocks(chart) == {"get-the-data": True}


def test_blocks_read_from_the_api_are_sent_back():
    api_response = {
        "id": "abc12",
        "type": "d3-bars",
        "title": "From the API",
        "metadata": {
            "publish": {
                "blocks": {
                    "logo": {"id": "red", "enabled": True},
                    "embed": False,
                    "get-the-data": True,
                }
            }
        },
    }
    chart = BaseChart(**BaseChart.deserialize_model(api_response), data=DATA)

    assert blocks(chart) == {
        "logo": {"id": "red", "enabled": True},
        "embed": False,
        "get-the-data": True,
    }

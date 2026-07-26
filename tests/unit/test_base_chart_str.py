"""Tests for the safe string representation of chart objects."""

import pandas as pd

import datawrapper


def test_base_chart_str_is_compact_and_identifying():
    chart = datawrapper.BaseChart.model_validate(
        {
            "chart-type": "d3-lines",
            "title": "Monthly revenue",
        }
    )
    chart.chart_id = "abc123"

    assert str(chart) == (
        "BaseChart(title='Monthly revenue', chart_type='d3-lines', chart_id='abc123')"
    )


def test_base_chart_str_omits_data_and_custom_metadata():
    chart = datawrapper.BarChart(
        title="Sensitive chart",
        data=pd.DataFrame(
            {
                "api_token": ["do-not-leak"],
                "value": [1],
            }
        ),
        custom={"internal_payload": {"secret": "also-do-not-leak"}},
    )

    rendered = str(chart)

    assert rendered == (
        "BarChart(title='Sensitive chart', chart_type='d3-bars', chart_id=None)"
    )
    assert "api_token" not in rendered
    assert "do-not-leak" not in rendered
    assert "internal_payload" not in rendered
    assert "also-do-not-leak" not in rendered


def test_base_chart_str_uses_subclass_name_and_type():
    chart = datawrapper.LineChart(title="Trend over time")

    assert str(chart) == (
        "LineChart(title='Trend over time', chart_type='d3-lines', chart_id=None)"
    )

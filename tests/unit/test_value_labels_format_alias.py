import pytest
from pydantic import ValidationError

import datawrapper as dw
from datawrapper.charts.serializers import ValueLabels


def test_canonical_plural_spelling_is_accepted_for_bar_chart():
    chart = dw.BarChart(value_labels_format="0.0%")

    assert chart.value_labels_format == "0.0%"
    assert chart.value_label_format == "0.0%"
    assert (
        chart.serialize_model()["metadata"]["visualize"]["value-label-format"] == "0.0%"
    )


def test_singular_spelling_remains_backward_compatible_for_bar_chart():
    chart = dw.BarChart(value_label_format="0,0")

    assert chart.value_labels_format == "0,0"
    assert chart.value_label_format == "0,0"
    assert chart.model_dump()["value_labels_format"] == "0,0"


def test_assignment_through_singular_alias_updates_canonical_field():
    chart = dw.ArrowChart(value_labels_format="0.0")

    chart.value_label_format = "0.00"

    assert chart.value_labels_format == "0.00"
    assert (
        chart.serialize_model()["metadata"]["visualize"]["value-label-format"] == "0.00"
    )


def test_equivalent_dual_input_is_accepted():
    chart = dw.StackedBarChart(value_labels_format="0%", value_label_format="0%")

    assert chart.value_labels_format == "0%"
    assert chart.value_label_format == "0%"


def test_conflicting_dual_input_raises_clear_error():
    with pytest.raises(ValidationError, match="Conflicting value labels format"):
        dw.BarChart(value_labels_format="0%", value_label_format="0.0%")


def test_wire_alias_inputs_are_accepted_when_equivalent():
    chart = dw.LineChart(
        **{"value-labels-format": "0.0a", "value-label-format": "0.0a"}
    )

    assert chart.value_labels_format == "0.0a"
    assert chart.value_label_format == "0.0a"
    assert (
        chart.serialize_model()["metadata"]["visualize"]["value-labels-format"]
        == "0.0a"
    )


def test_deserialize_accepts_either_api_spelling_and_serializes_chart_wire_key():
    init_data = dw.BarChart.deserialize_model(
        {
            "type": "d3-bars",
            "metadata": {"visualize": {"value-labels-format": "0.[0]%"}},
        }
    )

    chart = dw.BarChart(**init_data)

    assert chart.value_labels_format == "0.[0]%"
    assert (
        chart.serialize_model()["metadata"]["visualize"]["value-label-format"]
        == "0.[0]%"
    )


def test_deserialize_rejects_conflicting_api_spellings():
    with pytest.raises(ValueError, match="Conflicting value labels format"):
        dw.LineChart.deserialize_model(
            {
                "type": "d3-lines",
                "metadata": {
                    "visualize": {
                        "value-labels-format": "0%",
                        "value-label-format": "0.0%",
                    }
                },
            }
        )


def test_value_labels_serializer_accepts_matching_api_mirrors():
    assert (
        ValueLabels.deserialize(
            {
                "valueLabels": {
                    "show": "always",
                    "format": "0,0",
                    "enabled": True,
                    "placement": "inside",
                },
                "value-label-format": "0,0",
            },
            chart_type="column",
        )["value_labels_format"]
        == "0,0"
    )


def test_value_labels_serializer_rejects_conflicting_api_mirrors():
    with pytest.raises(ValueError, match="Conflicting value labels format"):
        ValueLabels.deserialize(
            {
                "valueLabels": {
                    "show": "always",
                    "format": "0,0",
                    "enabled": True,
                    "placement": "inside",
                },
                "value-label-format": "0.0",
            },
            chart_type="column",
        )


def test_value_labels_serializer_bar_accepts_either_api_spelling():
    assert ValueLabels.deserialize(
        {
            "show-value-labels": True,
            "value-labels-format": "0.[0]%",
            "value-label-alignment": "right",
        },
        chart_type="bar",
    ) == {
        "show_value_labels": True,
        "value_labels_format": "0.[0]%",
        "value_labels_alignment": "right",
    }


def test_value_labels_serializer_bar_rejects_conflicting_api_spellings():
    with pytest.raises(ValueError, match="Conflicting value labels format"):
        ValueLabels.deserialize(
            {
                "value-labels-format": "0%",
                "value-label-format": "0.0%",
            },
            chart_type="bar",
        )

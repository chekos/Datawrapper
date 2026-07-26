"""Tests for Line.color convenience color mapping."""

import pytest

from datawrapper.charts.line import Line, LineChart


def test_line_accepts_color_convenience_value():
    """Line.color stores a color without serializing it into line config."""
    line = Line(column="sales", color="#ff0000")

    assert line.color == "#ff0000"
    assert "color" not in Line.serialize_model(line)


def test_line_color_deserialization_preserves_unexpected_line_color():
    """If API line config ever contains color, keep it rather than dropping data."""
    line_dict = Line.deserialize_model("sales", {"color": "#ff0000"})

    assert line_dict["color"] == "#ff0000"
    assert Line(**line_dict).color == "#ff0000"


def test_line_color_merges_into_color_category_serialization():
    """Line.color is serialized through Datawrapper's color-category map."""
    chart = LineChart(
        title="Line colors",
        lines=[Line(column="sales", color="#ff0000")],
    )

    visualize = chart.serialize_model()["metadata"]["visualize"]

    assert visualize["color-category"] == {"map": {"sales": "#ff0000"}}
    assert "color" not in visualize["lines"]["sales"]


def test_dict_line_color_is_validated_once_during_serialization(monkeypatch):
    """Serialization reuses validated line configs for color and line output."""
    call_count = 0
    original_model_validate = Line.model_validate.__func__

    def counting_model_validate(cls, obj):
        nonlocal call_count
        call_count += 1
        return original_model_validate(cls, obj)

    monkeypatch.setattr(Line, "model_validate", classmethod(counting_model_validate))

    chart = LineChart(title="Dict line colors")
    chart.lines.append({"column": "sales", "color": "#ff0000", "width": "style2"})

    visualize = chart.serialize_model()["metadata"]["visualize"]

    assert call_count == 1
    assert visualize["color-category"] == {"map": {"sales": "#ff0000"}}
    assert visualize["lines"]["sales"]["width"] == "style2"


def test_legacy_color_category_serialization_is_unchanged():
    """Existing color_category callers keep the same serialized API shape."""
    chart = LineChart(
        title="Legacy line colors",
        color_category={"sales": "#ff0000", "profit": "#00ff00"},
    )

    visualize = chart.serialize_model()["metadata"]["visualize"]

    assert visualize["color-category"] == {
        "map": {"sales": "#ff0000", "profit": "#00ff00"}
    }


def test_matching_line_color_and_color_category_are_allowed():
    """Callers may use both interfaces if overlapping values agree."""
    chart = LineChart(
        title="Matching colors",
        color_category={"sales": "#ff0000", "profit": "#00ff00"},
        lines=[Line(column="sales", color="#ff0000")],
    )

    visualize = chart.serialize_model()["metadata"]["visualize"]

    assert visualize["color-category"] == {
        "map": {"sales": "#ff0000", "profit": "#00ff00"}
    }


def test_conflicting_line_color_and_color_category_raise():
    """Ambiguous colors should fail rather than silently picking a winner."""
    chart = LineChart(
        title="Conflicting colors",
        color_category={"sales": "#ff0000"},
        lines=[Line(column="sales", color="#00ff00")],
    )

    with pytest.raises(ValueError, match="Conflicting colors for line 'sales'"):
        chart.serialize_model()


def test_line_color_does_not_mutate_color_category_attribute():
    """The convenience merge is serialization-only and leaves public state intact."""
    chart = LineChart(
        title="No mutation",
        color_category={"profit": "#00ff00"},
        lines=[Line(column="sales", color="#ff0000")],
    )

    chart.serialize_model()

    assert chart.color_category == {"profit": "#00ff00"}


def test_deserialization_keeps_colors_on_legacy_color_category():
    """Color-category remains the canonical read-back location."""
    init_data = LineChart.deserialize_model(
        {
            "type": "d3-lines",
            "metadata": {
                "visualize": {
                    "color-category": {"map": {"sales": "#ff0000"}},
                    "lines": {"sales": {"width": "style2"}},
                }
            },
        }
    )

    assert init_data["color_category"] == {"sales": "#ff0000"}
    assert init_data["lines"][0]["column"] == "sales"
    assert "color" not in init_data["lines"][0]

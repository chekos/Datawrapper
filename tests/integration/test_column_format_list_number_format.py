"""Integration tests for ColumnFormatList with the number_format field."""

import json
from pathlib import Path

import pytest

from datawrapper import AreaChart, ArrowChart, ScatterPlot, StackedBarChart
from datawrapper.charts import ColumnFormat, ColumnFormatList, DateFormat

SAMPLES_DIR = Path(__file__).parent.parent / "samples"


class TestColumnFormatListNumberFormat:
    """Test ColumnFormatList serialization with number_format."""

    def test_serialize_number_format(self):
        """A column's number format is sent to the API."""
        formats = ColumnFormatList(
            formats=[ColumnFormat(column="share", type="number", number_format="0.0%")]
        )

        serialized = formats.serialize_to_dict()
        assert serialized["share"] == {"type": "number", "number-format": "0.0%"}

    def test_serialize_date_format_enum(self):
        """A DateFormat enum is sent as its format string."""
        formats = ColumnFormatList(
            formats=[
                ColumnFormat(
                    column="date", type="date", number_format=DateFormat.YEAR_FULL
                )
            ]
        )

        assert formats.serialize_to_dict()["date"]["number-format"] == "YYYY"

    @pytest.mark.parametrize("default", ["-", "auto"])
    def test_default_number_format_is_left_out(self, default):
        """The model default and the API default are not sent."""
        formats = ColumnFormatList.model_validate(
            {"share": {"type": "auto", "number-format": default}}
        )

        assert formats.serialize_to_dict() == {"share": {}}


def load_sample(folder: str, name: str) -> dict:
    """Load the chart metadata stored in a sample file."""
    with open(SAMPLES_DIR / folder / f"{name}.json", encoding="utf-8") as f:
        return json.load(f)["chart"]["crdt"]["data"]


@pytest.mark.parametrize(
    ("chart_class", "folder", "name"),
    [
        (AreaChart, "area", "tate"),
        (ArrowChart, "arrow", "inequality"),
        (ScatterPlot, "scatter", "german-students"),
        (StackedBarChart, "stacked_bar", "sugar"),
    ],
)
def test_fetched_column_number_formats_survive_serialization(chart_class, folder, name):
    """Column number formats survive get() then update()."""
    api_response = load_sample(folder, name)
    source = api_response["metadata"]["data"]["column-format"]
    expected = {
        column: config["number-format"]
        for column, config in source.items()
        if config.get("number-format") not in (None, "-", "auto")
    }
    assert expected

    chart = chart_class(**chart_class.deserialize_model(api_response))
    serialized = chart.serialize_model()["metadata"]["data"]["column-format"]

    assert {
        column: serialized[column].get("number-format") for column in expected
    } == expected

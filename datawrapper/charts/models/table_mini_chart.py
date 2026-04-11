from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from ..enums import NumberFormat


class TableMiniChart(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        strict=True,
        json_schema_extra={
            "sparkline": {
                "area": False,
                "type": "columns",
                "color": 0,
                "title": "Words in here",
                "format": "0.[0]a",
                "height": 20,
                "stroke": 2,
                "dotLast": True,
                "enabled": True,
                "colorNeg": 0,
                "dotFirst": True,
                "rangeMax": "",
                "rangeMin": "",
                "labelDiff": False,
            }
        },
    )
    type: str = Field(alias="type", description="The type of mini chart")

    title: str | None = Field(
        default=None,
        alias="title",
        description="The title that appears in the column header for the mini chart",
    )
    enabled: bool = Field(
        default=True,
        alias="enabled",
        description="Whether the mini chart should be enabled",
    )
    range_min: float | None = Field(
        default=None, alias="rangeMin", description="The range minimum"
    )
    range_max: float | None = Field(
        default=None, alias="rangeMax", description="The range maximum"
    )
    height: int | None = Field(
        default=None, alias="height", description="The height of the mini chart"
    )
    color: int | str | None = Field(
        default=None, alias="color", description="The colour of the column or line"
    )
    columns: list[str] = Field(
        alias="columns", description="A list of the columns the chart will include"
    )

    def serialize_model(self) -> dict:
        model = self.model_dump(by_alias=True, exclude_none=True, exclude={"columns"})
        return model

    @classmethod
    def deserialize(cls, data: dict) -> dict:
        """
        Convert a raw dict (with alias keys) into kwargs for constructing the model.
        """
        kwargs = {}

        for field_name, field in cls.model_fields.items():
            alias = field.alias
            if alias in data:
                value = data[alias]

                # Normalize empty strings → None for numeric fields
                if value == "":
                    value = None
                kwargs[field_name] = value
        return kwargs


class MiniColumn(TableMiniChart):
    type: Literal["columns"] = Field(
        default="columns", alias="type", description="The type of mini chart"
    )
    color_neg: int | str | None = Field(
        default=None, alias="colorNeg", description="The color of negative values"
    )


class MiniLine(TableMiniChart):
    type: Literal["line"] = Field(
        default="line", alias="type", description="The type of mini chart"
    )
    area: bool | None = Field(
        default=None,
        alias="area",
        description="Whether to fill the area under the line",
    )
    format: NumberFormat | str | None = Field(
        default=None,
        alias="format",
        description="The number format for the chart labels",
    )
    stroke: float | None = Field(
        default=None,
        alias="stroke",
        description="The weight of the line in the chart in pixels, from 0.5 to 4",
    )
    dot_last: bool | None = Field(
        default=None,
        alias="dotLast",
        description="Whether the last value in the line should show a dot and label",
    )
    dot_first: bool | None = Field(
        default=None,
        alias="dotFirst",
        description="Whether the first value in the line should show a dot and label",
    )

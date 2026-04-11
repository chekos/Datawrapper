from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from ..enums import BorderWidth, NumberFormat
from ..models import TableTextStyle


class TableRow(BaseModel):
    """Represents a row in the table"""

    model_config = ConfigDict(populate_by_name=True, validate_assignment=True)

    style: TableTextStyle | None = Field(
        default=None, alias="style", description="The text styles"
    )

    border_top: BorderWidth | str | None = Field(
        default=None,
        alias="borderTop",
        description="The weight of the top border for the row",
    )
    border_top_color: str | None = Field(
        default=None,
        alias="borderTopColor",
        description="The color of the top border for the  row",
    )
    border_bottom: BorderWidth | str | None = Field(
        default=None,
        alias="borderBottom",
        description="The weight of the bottom border for the row",
    )
    border_bottom_color: str | None = Field(
        default=None,
        alias="borderBottomColor",
        description="The color of the bottom border for the row",
    )

    @field_validator("border_bottom", "border_top", mode="before")
    def validate_border_width(cls, v):  # noqa: N805
        if v is None:
            v = "none"
        # Case 1: already an enum → OK
        if isinstance(v, BorderWidth):
            return v

        # Case 2: string that matches an enum value → convert to enum
        if isinstance(v, str):
            try:
                return BorderWidth(v)
            except ValueError as err:
                allowed = [bw.value for bw in BorderWidth]
                raise ValueError(
                    f"Invalid border width '{v}'. Must be one of: {allowed}"
                ) from err

        # Case 3: anything else → reject
        raise TypeError("Border width must be a string or BorderWidth enum")


class TableBodyRow(TableRow):
    row_index: int = Field(description="The row index")

    sticky: bool = Field(
        default=False,
        alias="sticky",
        description="Whether the row should show on every page of the table",
    )
    move_row: bool = Field(
        default=False, alias="moveRow", description="Whether to move the row"
    )
    move_row_to: Literal["top", "bottom"] = Field(
        default="top", alias="moveTo", description="Where to move the row to"
    )
    format: NumberFormat | str | None = Field(
        default=None, alias="format", description="The format for values in the row"
    )
    override_format: bool = Field(
        default=False,
        alias="overrideFormat",
        description="Whether the format for the row should override the format of the column",
    )

    @staticmethod
    def extract_row_index(row_name: str) -> int:
        import re

        match = re.search(r"(\d+)$", row_name)
        if not match:
            raise ValueError(f"Invalid row name: {row_name}")
        return int(match.group(1))

    def serialize_model(self):
        # Start with ALL fields from TableRow + TableBodyRow
        model = self.model_dump(by_alias=True)

        # Remove row_index because Datawrapper does not want it in the row JSON
        model.pop("row_index", None)

        # If format is None, remove it (DW only wants it when set)
        if self.format is None:
            model.pop("format", None)
            model.pop("overrideFormat", None)

        return model

    @classmethod
    def deserialize_model(cls, row_index: int, data: dict):
        return {"row_index": row_index, **data}

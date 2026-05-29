from pydantic import BaseModel, ConfigDict, Field, field_validator


class TableTextStyle(BaseModel):
    model_config = ConfigDict(populate_by_name=True, validate_assignment=True)

    bold: bool | None = Field(
        default=None, alias="bold", description="Whether the text should be bold"
    )
    italic: bool | None = Field(
        default=None, alias="italic", description="Whether the text should be italic"
    )
    color: str | None | bool = Field(
        default=None, alias="color", description="The color of the text"
    )
    background: str | bool | None = Field(
        default=None, alias="background", description="The background color of the text"
    )
    font_size: float | None = Field(
        default=None, alias="fontSize", description="The size of the text"
    )


color: str | None | bool = Field(...)


@field_validator("color", mode="before")
def only_false_bool(cls, v):
    if v is True:
        raise ValueError("color cannot be True")
    return v

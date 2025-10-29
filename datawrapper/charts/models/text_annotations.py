"""Text annotation models for Datawrapper charts."""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator

from ..enums import ArrowHead, ConnectorLineType, StrokeType, StrokeWidth, TextAlign


class ConnectorLine(BaseModel):
    """A base class for the Datawrapper API's 'connector-line' attribute.

    Note: The presence of this object implies the connector line is enabled. The enabled field
    is automatically set to True and should not be set to False.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        strict=True,
        json_schema_extra={"examples": [{"type": "straight", "enabled": True}]},
    )

    #: Whether or not to show the connector line (automatically set to True when object exists)
    enabled: bool = Field(
        default=True,
        description="Whether or not to show the connector line (automatically set to True when object exists)",
    )

    @field_validator("enabled")
    @classmethod
    def validate_enabled(cls, v: bool) -> bool:
        """Validate that enabled is not explicitly set to False."""
        if v is False:
            raise ValueError(
                "ConnectorLine.enabled cannot be False. To disable connector lines, omit the connector_line field entirely."
            )
        return v

    #: The type of connector line
    type: ConnectorLineType | str = Field(
        default="straight", description="The type of connector line"
    )

    @field_validator("type")
    @classmethod
    def validate_type(cls, v: ConnectorLineType | str) -> ConnectorLineType | str:
        """Validate that type is a valid ConnectorLineType value."""
        if isinstance(v, str):
            valid_values = [e.value for e in ConnectorLineType]
            if v not in valid_values:
                raise ValueError(
                    f"Invalid connector line type: {v}. Must be one of {valid_values}"
                )
        return v

    #: Whether or not to show a circle at the end of the connector line
    circle: bool = Field(
        default=False,
        description="Whether or not to show a circle at the end of the connector line",
    )

    #: The stroke width of the connector line
    stroke: StrokeWidth | int = Field(
        default=1, description="The stroke width of the connector line"
    )

    @field_validator("stroke")
    @classmethod
    def validate_stroke(cls, v: StrokeWidth | int) -> StrokeWidth | int:
        """Validate that stroke is a valid StrokeWidth value."""
        if isinstance(v, int):
            valid_values = [e.value for e in StrokeWidth]
            if v not in valid_values:
                raise ValueError(
                    f"Invalid stroke width: {v}. Must be one of {valid_values}"
                )
        return v

    #: The arrow head of the connector line
    arrow_head: ArrowHead | str | bool = Field(
        default="lines",
        alias="arrowHead",
        description="The arrow head of the connector line",
    )

    #: The style of the circle at the end of the connector line
    circle_style: StrokeType | str = Field(
        default="solid",
        alias="circleStyle",
        description="The style of the circle at the end of the connector line",
    )

    @field_validator("circle_style")
    @classmethod
    def validate_circle_style(cls, v: StrokeType | str) -> StrokeType | str:
        """Validate that circle_style is either solid or dashed (not dotted).

        Handles both string and enum inputs. DOTTED is not allowed.
        """
        # Handle enum inputs
        if isinstance(v, StrokeType):
            if v not in [StrokeType.SOLID, StrokeType.DASHED]:
                raise ValueError(
                    f"Invalid circle style: {v.value}. Must be either 'solid' or 'dashed'"
                )
        # Handle string inputs
        elif isinstance(v, str):
            if v not in ["solid", "dashed"]:
                raise ValueError(
                    f"Invalid circle style: {v}. Must be either 'solid' or 'dashed'"
                )
        return v

    #: The radius of the circle at the end of the connector line
    circle_radius: int = Field(
        default=15,
        alias="circleRadius",
        description="The radius of the circle at the end of the connector line",
    )

    #: Whether or not to inherit the color of the annotation
    inherit_color: bool = Field(
        default=False,
        alias="inheritColor",
        description="Whether or not to inherit the color of the annotation",
    )

    #: The padding between the target and the connector line
    target_padding: int = Field(
        default=4,
        alias="targetPadding",
        description="The padding between the target and the connector line",
    )


class TextAnnotation(BaseModel):
    """A base class for the Datawrapper API's 'text-annotations' attribute."""

    model_config = ConfigDict(
        populate_by_name=True,
        strict=True,
        json_schema_extra={
            "examples": [
                {
                    "text": "Hello World",
                    "x": 0,
                    "y": 0,
                }
            ]
        },
    )

    #: The unique ID for this annotation (preserved during deserialization, auto-generated during serialization)
    id: str | None = Field(
        default=None,
        description="The unique ID for this annotation (used as dict key, not included in serialized output)",
    )

    #: Whether or not to show a text outline
    outline: bool = Field(
        default=True, alias="bg", description="Whether or not to show a text outline"
    )

    #: The x offset of the annotation relative to its position
    dx: int = Field(
        default=0, description="The x offset of the annotation relative to its position"
    )

    #: The y offset of the annotation relative to its position
    dy: int = Field(
        default=0, description="The y offset of the annotation relative to its position"
    )

    #: Whether or not to bold the text
    bold: bool = Field(default=False, description="Whether or not to bold the text")

    #: The size of the text
    size: int = Field(default=14, description="The size of the text")

    #: The text to display
    text: str = Field(min_length=1, description="The text to display")

    #: The alignment of the text
    align: TextAlign | str = Field(
        default="tl", description="The alignment of the text"
    )

    @field_validator("align")
    @classmethod
    def validate_align(cls, v: TextAlign | str) -> TextAlign | str:
        """Validate that align is a valid TextAlign value."""
        if isinstance(v, str):
            valid_values = [e.value for e in TextAlign]
            if v not in valid_values:
                raise ValueError(
                    f"Invalid text alignment: {v}. Must be one of {valid_values}"
                )
        return v

    #: The color of the text
    color: str | bool = Field(
        default=False,  # If you don't set a color, it will default to the Datawrapper standard
        description="The color of the text",
    )

    #: The width of the text as a percentage of the chart width
    width: float = Field(
        default=33.3,
        description="The width of the text as a percentage of the chart width",
    )

    @field_validator("width")
    @classmethod
    def validate_width(cls, v: float) -> float:
        """Validate that width is between 0.0 and 100.0."""
        if not 0.0 <= v <= 100.0:
            raise ValueError(
                f"Invalid width: {v}. Must be between 0.0 and 100.0 (inclusive)"
            )
        return v

    #: Whether or not to italicize the text
    italic: bool = Field(
        default=False, description="Whether or not to italicize the text"
    )

    #: The x position of the annotation
    x: Any = Field(description="The x position of the annotation")

    #: The y position of the annotation
    y: Any = Field(description="The y position of the annotation")

    #: Whether or not to underline the text
    underline: bool = Field(
        default=False, description="Whether or not to underline the text"
    )

    #: Whether or not to show the annotation on mobile
    show_mobile: bool = Field(
        default=True,
        alias="showMobile",
        description="Whether or not to show the annotation on mobile",
    )

    #: Whether or not to show the annotation on desktop
    show_desktop: bool = Field(
        default=True,
        alias="showDesktop",
        description="Whether or not to show the annotation on desktop",
    )

    #: The connector line for the annotation (None = disabled, object = enabled)
    connector_line: ConnectorLine | dict[Any, Any] | None = Field(
        default=None,
        alias="connectorLine",
        description="The connector line for the annotation (None = disabled, object = enabled)",
    )

    #: Whether or not to show a mobile fallback
    mobile_fallback: bool = Field(
        default=False,
        alias="mobileFallback",
        description="Whether or not to show a mobile fallback",
    )

    def serialize_model(self) -> dict:
        """Serialize the model to a dictionary for the Datawrapper API.

        Note: The 'id' field is not included in the output as it's used as the dict key.
        """
        model = {
            "bg": self.outline,
            "dx": self.dx,
            "dy": self.dy,
            "bold": self.bold,
            "size": self.size,
            "text": self.text,
            "align": self.align,
            "color": self.color,
            "width": self.width,
            "italic": self.italic,
            "position": {"x": self.x, "y": self.y},
            "underline": self.underline,
            "showMobile": self.show_mobile,
            "showDesktop": self.show_desktop,
            "mobileFallback": self.mobile_fallback,
        }

        # Add connector line if configured (None = disabled)
        if self.connector_line is not None:
            if isinstance(self.connector_line, dict):
                model["connectorLine"] = ConnectorLine.model_validate(
                    self.connector_line
                ).model_dump(by_alias=True)
            else:
                model["connectorLine"] = self.connector_line.model_dump(by_alias=True)
        else:
            model["connectorLine"] = {"enabled": False}

        return model

    @classmethod
    def deserialize_model(cls, api_data: dict[str, dict] | None) -> list[dict]:
        """Deserialize annotations from API response format.

        Args:
            api_data: Dictionary mapping UUID keys to annotation data, or None

        Returns:
            List of annotation dicts with 'id' field preserved
        """
        if not api_data:
            return []

        result = []
        for anno_id, anno_data in api_data.items():
            # Create a copy to avoid modifying the original
            anno_dict = {**anno_data, "id": anno_id}

            # Handle connector line deserialization (enabled by presence pattern)
            if "connectorLine" in anno_dict:
                connector = anno_dict["connectorLine"]
                if isinstance(connector, dict):
                    # If enabled is False or missing, set to None (disabled)
                    if not connector.get("enabled", False):
                        anno_dict["connectorLine"] = None
                    # Otherwise keep the connector line object (enabled)

            result.append(anno_dict)
        return result

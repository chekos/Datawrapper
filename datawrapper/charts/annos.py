from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class ConnectorLine(BaseModel):
    """A base class for the Datawrapper API's 'connector-line' attribute."""

    model_config = ConfigDict(
        populate_by_name=True,
        strict=True,
        json_schema_extra={"examples": [{"type": "straight", "enabled": True}]},
    )

    #: The type of connector line
    type: Literal["straight", "curveRight", "curveLeft"] = Field(
        default="straight", description="The type of connector line"
    )

    #: Whether or not to show a circle at the end of the connector line
    circle: bool = Field(
        default=False,
        description="Whether or not to show a circle at the end of the connector line",
    )

    #: The stroke width of the connector line
    stroke: Literal[1, 2, 3] = Field(
        default=1, description="The stroke width of the connector line"
    )

    #: Whether or not to show the connector line
    enabled: bool = Field(
        default=False, description="Whether or not to show the connector line"
    )

    #: The arrow head of the connector line
    arrow_head: Literal["lines", "triangle", False] = Field(
        default="lines",
        alias="arrowHead",
        description="The arrow head of the connector line",
    )

    #: The style of the circle at the end of the connector line
    circle_style: Literal["solid", "dashed"] = Field(
        default="solid",
        alias="circleStyle",
        description="The style of the circle at the end of the connector line",
    )

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
                    "text": "Hello Wor;d",
                    "x": 0,
                    "y": 0,
                }
            ]
        },
    )

    #: Whether or not to show a text outline
    bg: bool = Field(default=True, description="Whether or not to show a text outline")

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
    align: Literal["tl", "tc", "tr", "ml", "mc", "mr", "bl", "bc", "br"] = Field(
        default="tl", description="The alignment of the text"
    )

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

    #: The connector line for the annotation
    connector_line: ConnectorLine | dict[Any, Any] = Field(
        default_factory=ConnectorLine,
        alias="connectorLine",
        description="The connector line for the annotation",
    )

    #: Whether or not to show a mobile fallback
    mobile_fallback: bool = Field(
        default=False,
        alias="mobileFallback",
        description="Whether or not to show a mobile fallback",
    )

    def serialize_model(self) -> dict:
        """Serialize the model to a dictionary for the Datawrapper API."""
        model = {
            "bg": self.bg,
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
            "connectorLine": {},
            "mobileFallback": self.mobile_fallback,
        }

        # Add any connector line
        if isinstance(self.connector_line, dict):
            model["connectorLine"] = ConnectorLine.model_validate(
                self.connector_line
            ).model_dump(by_alias=True)
        elif isinstance(self.connector_line, ConnectorLine):
            model["connectorLine"] = self.connector_line.model_dump(by_alias=True)

        return model


class RangeAnnotation(BaseModel):
    """A base class for the Datawrapper API's 'range-annotations' attribute."""

    model_config = ConfigDict(
        populate_by_name=True,
        strict=True,
        json_schema_extra={
            "examples": [
                {
                    "type": "x",
                    "x0": 0,
                    "x1": 0,
                    "y0": 0,
                    "y1": 0,
                }
            ]
        },
    )

    #: The axis of the annotation
    type: Literal["x", "y"] = Field(
        default="x", description="The axis of the annotation"
    )

    #: The color of the annotation
    color: str = Field(default="#989898", description="The color of the annotation")

    #: The display style of the annotation
    display: Literal["line", "range"] = Field(
        default="range", description="The display style of the annotation"
    )

    #: The opacity of the annotation
    opacity: int = Field(default=50, description="The opacity of the annotation")

    #: The first x position
    x0: Any = Field(description="The first x position")

    #: The second x position
    x1: Any = Field(description="The second x position")

    #: The first y position
    y0: Any = Field(description="The first y position")

    #: The second y position
    y1: Any = Field(description="The second y position")

    #: The stroke type of the annotation, if the display style is a line
    stroke_type: Literal["solid", "dashed", "dotted"] = Field(
        default="solid",
        alias="strokeType",
        description=" The stroke type of the annotation, if the display style is a line",
    )

    #: The stroke width of the annotation, if the display style is a line
    stroke_width: Literal[1, 2, 3] = Field(
        default=2,
        alias="strokeWidth",
        description="The stroke width of the annotation, if the display style is a line",
    )

    def serialize_model(self) -> dict:
        """Serialize the model to a dictionary for the Datawrapper API."""
        return {
            "type": self.type,
            "color": self.color,
            "display": self.display,
            "opacity": self.opacity,
            "position": {
                "x0": self.x0,
                "x1": self.x1,
                "y0": self.y0,
                "y1": self.y1,
            },
            "strokeType": self.stroke_type,
            "strokeWidth": self.stroke_width,
        }

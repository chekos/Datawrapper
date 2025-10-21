from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from .enums import ArrowHead, ConnectorLineType, LineInterpolation, StrokeWidth


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
    def deserialize_model(cls, api_data: dict[str, dict] | list | None) -> list[dict]:
        """Deserialize annotations from API response format.

        Args:
            api_data: Dictionary mapping UUID keys to annotation data,
                      or a list, or None

        Returns:
            List of annotation dicts with 'id' field preserved
        """
        if not api_data:
            return []

        # Handle dict format (UUID keys -> annotation data)
        if isinstance(api_data, dict):
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

        # Handle list format (already deserialized or legacy)
        return list(api_data)


class AreaFill(BaseModel):
    """A base class for the Datawrapper API's 'custom-area-fills' attribute."""

    model_config = ConfigDict(
        populate_by_name=True,
        strict=True,
        json_schema_extra={
            "examples": [
                {
                    "from_column": "baseline",
                    "to_column": "new",
                    "color": "#15607a",
                    "opacity": 0.3,
                }
            ]
        },
    )

    #: The unique ID for this area fill (preserved during deserialization, auto-generated during serialization)
    id: str | None = Field(
        default=None,
        description="The unique ID for this area fill (used as dict key, not included in serialized output)",
    )

    #: The line to fill upwards from
    from_column: str = Field(alias="from", description="The line to fill upwards from")

    #: The line to fill upwards to
    to_column: str = Field(alias="to", description="The line to fill upwards to")

    #: The color of the fill (hex string or palette index)
    color: str | int = Field(
        default=0, description="The color of the fill (hex string or palette index)"
    )

    #: The opacity of the fill
    opacity: float = Field(default=0.3, description="The opacity of the fill")

    #: Whether to use different colors when there are negative values
    use_mixed_colors: bool = Field(
        default=False,
        alias="useMixedColors",
        description="Whether to use different colors when there are negative values",
    )

    #: The color of the fill when it is negative (hex string or palette index, None = disabled)
    color_negative: str | int | None = Field(
        default=None,
        alias="colorNegative",
        description="The color of the fill when it is negative (hex string or palette index, None = disabled)",
    )

    #: The interpolation method to use when drawing lines
    interpolation: LineInterpolation | str = Field(
        default="linear", description="The interpolation method to use"
    )

    @field_validator("interpolation")
    @classmethod
    def validate_interpolation(
        cls, v: LineInterpolation | str
    ) -> LineInterpolation | str:
        """Validate that interpolation is a valid LineInterpolation value."""
        if isinstance(v, str):
            valid_values = [e.value for e in LineInterpolation]
            if v not in valid_values:
                raise ValueError(
                    f"Invalid interpolation: {v}. Must be one of {valid_values}"
                )
        return v

    @model_validator(mode="after")
    def auto_enable_mixed_colors(self) -> "AreaFill":
        """Auto-enable use_mixed_colors when color_negative is provided.

        If a user provides a color_negative value (not None),
        automatically enable use_mixed_colors to make the feature work as expected.
        """
        # Only auto-enable if color_negative is provided and use_mixed_colors is False
        if self.color_negative is not None and not self.use_mixed_colors:
            self.use_mixed_colors = True
        return self

    def serialize_model(self) -> dict:
        """Serialize the model to a dictionary for the Datawrapper API.

        Note: The 'id' field is not included in the output as it's used as the dict key.
        Only includes colorNegative if it's not None.
        """
        result = {
            "from": self.from_column,
            "to": self.to_column,
            "color": self.color,
            "opacity": self.opacity,
            "useMixedColors": self.use_mixed_colors,
            "interpolation": self.interpolation,
        }

        # Only include colorNegative if it's provided (not None)
        if self.color_negative is not None:
            result["colorNegative"] = self.color_negative

        return result

    @classmethod
    def deserialize_model(cls, api_data: dict[str, dict] | list | None) -> list[dict]:
        """Deserialize area fills from API response format.

        Args:
            api_data: Dictionary mapping UUID keys to area fill data,
                      or a list, or None

        Returns:
            List of area fill dicts with 'id' field preserved
        """
        if not api_data:
            return []

        # Handle dict format (UUID keys -> area fill data)
        if isinstance(api_data, dict):
            return [
                {**fill_data, "id": fill_id} for fill_id, fill_data in api_data.items()
            ]

        # Handle list format (already deserialized or legacy)
        return list(api_data)


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

    #: The unique ID for this annotation (preserved during deserialization, auto-generated during serialization)
    id: str | None = Field(
        default=None,
        description="The unique ID for this annotation (used as dict key, not included in serialized output)",
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

    #: The first x position (required for type="x" annotations)
    x0: Any | None = Field(
        default=None,
        description="The first x position (required for type='x' annotations)",
    )

    #: The second x position (required for type="x" range annotations)
    x1: Any | None = Field(
        default=None,
        description="The second x position (required for type='x' range annotations)",
    )

    #: The first y position (required for type="y" annotations)
    y0: Any | None = Field(
        default=None,
        description="The first y position (required for type='y' annotations)",
    )

    #: The second y position (required for type="y" range annotations)
    y1: Any | None = Field(
        default=None,
        description="The second y position (required for type='y' range annotations)",
    )

    #: The stroke type of the annotation, if the display style is a line
    stroke_type: Literal["solid", "dashed", "dotted"] = Field(
        default="solid",
        alias="strokeType",
        description=" The stroke type of the annotation, if the display style is a line",
    )

    #: The stroke width of the annotation, if the display style is a line
    stroke_width: StrokeWidth | int = Field(
        default=2,
        alias="strokeWidth",
        description="The stroke width of the annotation, if the display style is a line",
    )

    @field_validator("stroke_width")
    @classmethod
    def validate_stroke_width(cls, v: StrokeWidth | int) -> StrokeWidth | int:
        """Validate that stroke_width is a valid StrokeWidth value."""
        if isinstance(v, int):
            valid_values = [e.value for e in StrokeWidth]
            if v not in valid_values:
                raise ValueError(
                    f"Invalid stroke width: {v}. Must be one of {valid_values}"
                )
        return v

    def serialize_model(self) -> dict:
        """Serialize the model to a dictionary for the Datawrapper API.

        Note: The 'id' field is not included in the output as it's used as the dict key.
        Only includes position values that are not None.
        """
        # Build position dict with only non-None values
        position = {}
        if self.x0 is not None:
            position["x0"] = self.x0
        if self.x1 is not None:
            position["x1"] = self.x1
        if self.y0 is not None:
            position["y0"] = self.y0
        if self.y1 is not None:
            position["y1"] = self.y1

        return {
            "type": self.type,
            "color": self.color,
            "display": self.display,
            "opacity": self.opacity,
            "position": position,
            "strokeType": self.stroke_type,
            "strokeWidth": self.stroke_width,
        }

    @classmethod
    def deserialize_model(cls, api_data: dict[str, dict] | list | None) -> list[dict]:
        """Deserialize annotations from API response format.

        Args:
            api_data: Dictionary mapping UUID keys to annotation data,
                      or a list, or None

        Returns:
            List of annotation dicts with 'id' field preserved
        """
        if not api_data:
            return []

        # Handle dict format (UUID keys -> annotation data)
        if isinstance(api_data, dict):
            return [
                {**anno_data, "id": anno_id} for anno_id, anno_data in api_data.items()
            ]

        # Handle list format (already deserialized or legacy)
        return list(api_data)

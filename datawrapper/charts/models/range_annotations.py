"""Range and line annotation models for Datawrapper charts."""

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from ..enums import StrokeType, StrokeWidth


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

    @field_validator("type")
    @classmethod
    def validate_type(cls, v: str) -> str:
        """Validate that type is either 'x' or 'y'."""
        if v not in ["x", "y"]:
            raise ValueError(f"Invalid type: {v}. Must be either 'x' or 'y'")
        return v

    #: The color of the annotation
    color: str = Field(default="#989898", description="The color of the annotation")

    #: The display style of the annotation
    display: Literal["line", "range"] = Field(
        default="range", description="The display style of the annotation"
    )

    @field_validator("display")
    @classmethod
    def validate_display(cls, v: str) -> str:
        """Validate that display is either 'line' or 'range'."""
        if v not in ["line", "range"]:
            raise ValueError(f"Invalid display: {v}. Must be either 'line' or 'range'")
        return v

    #: The opacity of the annotation
    opacity: int = Field(default=50, description="The opacity of the annotation")

    @field_validator("opacity")
    @classmethod
    def validate_opacity(cls, v: int) -> int:
        """Validate that opacity is between 0 and 100."""
        if not 0 <= v <= 100:
            raise ValueError(f"Invalid opacity: {v}. Must be between 0 and 100")
        return v

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
    stroke_type: StrokeType | str = Field(
        default="solid",
        alias="strokeType",
        description=" The stroke type of the annotation, if the display style is a line",
    )

    @field_validator("stroke_type")
    @classmethod
    def validate_stroke_type(cls, v: StrokeType | str) -> StrokeType | str:
        """Validate that stroke_type is a valid StrokeType value."""
        if isinstance(v, str):
            valid_values = [e.value for e in StrokeType]
            if v not in valid_values:
                raise ValueError(
                    f"Invalid stroke type: {v}. Must be one of {valid_values}"
                )
        return v

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
    def deserialize_model(cls, api_data: dict[str, dict] | None) -> list[dict]:
        """Deserialize annotations from API response format.

        Args:
            api_data: Dictionary mapping UUID keys to annotation data, or None

        Returns:
            List of annotation dicts with 'id' field preserved
        """
        if not api_data:
            return []

        return [{**anno_data, "id": anno_id} for anno_id, anno_data in api_data.items()]


class XRangeAnnotation(RangeAnnotation):
    """A horizontal range annotation (shaded area between two x positions).

    Automatically sets type="x" and display="range".
    Requires both x0 and x1 to be provided.
    """

    def __init__(self, **data):
        """Initialize with type="x" and display="range" automatically set."""
        data.setdefault("type", "x")
        data.setdefault("display", "range")
        super().__init__(**data)

    @model_validator(mode="after")
    def validate_x_positions_required(self) -> "XRangeAnnotation":
        """Validate that both x0 and x1 are provided."""
        if self.x0 is None or self.x1 is None:
            raise ValueError("XRangeAnnotation requires both x0 and x1 to be set")
        return self


class YRangeAnnotation(RangeAnnotation):
    """A vertical range annotation (shaded area between two y positions).

    Automatically sets type="y" and display="range".
    Requires both y0 and y1 to be provided.
    """

    def __init__(self, **data):
        """Initialize with type="y" and display="range" automatically set."""
        data.setdefault("type", "y")
        data.setdefault("display", "range")
        super().__init__(**data)

    @model_validator(mode="after")
    def validate_y_positions_required(self) -> "YRangeAnnotation":
        """Validate that both y0 and y1 are provided."""
        if self.y0 is None or self.y1 is None:
            raise ValueError("YRangeAnnotation requires both y0 and y1 to be set")
        return self


class XLineAnnotation(RangeAnnotation):
    """A vertical line annotation at a specific x position.

    Automatically sets type="x" and display="line".
    Requires x0 to be provided.
    """

    def __init__(self, **data):
        """Initialize with type="x" and display="line" automatically set."""
        data.setdefault("type", "x")
        data.setdefault("display", "line")
        super().__init__(**data)

    @model_validator(mode="after")
    def validate_x0_required(self) -> "XLineAnnotation":
        """Validate that x0 is provided."""
        if self.x0 is None:
            raise ValueError("XLineAnnotation requires x0 to be set")
        return self


class YLineAnnotation(RangeAnnotation):
    """A horizontal line annotation at a specific y position.

    Automatically sets type="y" and display="line".
    Requires y0 to be provided.
    """

    def __init__(self, **data):
        """Initialize with type="y" and display="line" automatically set."""
        data.setdefault("type", "y")
        data.setdefault("display", "line")
        super().__init__(**data)

    @model_validator(mode="after")
    def validate_y0_required(self) -> "YLineAnnotation":
        """Validate that y0 is provided."""
        if self.y0 is None:
            raise ValueError("YLineAnnotation requires y0 to be set")
        return self

from typing import Any, Literal

import pandas as pd
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_serializer,
    model_validator,
)

from .base import BaseChart
from .enums import (
    DateFormat,
    GridLabelAlign,
    GridLabelPosition,
    LineDash,
    LineInterpolation,
    LineWidth,
    NumberFormat,
    PlotHeightMode,
    SymbolDisplay,
    SymbolShape,
    SymbolStyle,
)
from .models import (
    AnnotationsMixin,
    CustomRangeMixin,
    CustomTicksMixin,
    GridDisplayMixin,
    GridFormatMixin,
)
from .serializers import (
    ColorCategory,
    ModelListSerializer,
    PlotHeight,
)


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

    @field_validator("opacity")
    @classmethod
    def validate_opacity(cls, v: float) -> float:
        """Validate that opacity is between 0.0 and 1.0."""
        if not 0.0 <= v <= 1.0:
            raise ValueError(
                f"Invalid opacity: {v}. Must be between 0.0 and 1.0 (inclusive)"
            )
        return v

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
    def deserialize_model(cls, api_data: dict[str, dict] | None) -> list[dict]:
        """Deserialize area fills from API response format.

        Args:
            api_data: Dictionary mapping UUID keys to area fill data, or None

        Returns:
            List of area fill dicts with 'id' field preserved
        """
        if not api_data:
            return []

        return [{**fill_data, "id": fill_id} for fill_id, fill_data in api_data.items()]


class LineSymbol(BaseModel):
    """Configure the symbols for an individual line on a Datawrapper line chart.

    Note: The presence of this object implies symbols are enabled. The enabled field
    is automatically set to True and should not be set to False.
    """

    model_config = ConfigDict(populate_by_name=True, strict=True)

    #: Whether or not to show symbols (automatically set to True when object exists)
    enabled: bool = Field(
        default=True,
        description="Whether or not to show symbols (automatically set to True when object exists)",
    )

    @field_validator("enabled")
    @classmethod
    def validate_enabled(cls, v: bool) -> bool:
        """Validate that enabled is not explicitly set to False."""
        if v is False:
            raise ValueError(
                "LineSymbol.enabled cannot be False. To disable symbols, omit the symbols field entirely."
            )
        return v

    #: The shape of the symbol
    shape: SymbolShape | str = Field(
        default="circle",
        description="The shape of the symbol",
    )

    #: The style of the symbol
    style: SymbolStyle | str = Field(
        default="fill",
        description="The style of the symbol",
    )

    #: Where to show the symbols
    on: SymbolDisplay | str = Field(
        default="last",
        description="Where to show the symbols",
    )

    #: The size of the symbols
    size: int | float = Field(
        default=6,
        description="The size of the symbols",
    )

    #: The opacity of the symbols between 0 and 1
    opacity: int | float = Field(
        default=1.0,
        description="The opacity of the symbols between 0 and 1",
    )


class LineValueLabel(BaseModel):
    """Configure the value labels for an individual line on a Datawrapper line chart.

    Note: The presence of this object implies value labels are enabled. The enabled field
    is automatically set to True and should not be set to False.
    """

    model_config = ConfigDict(populate_by_name=True, strict=True)

    #: Whether to show the value labels (automatically set to True when object exists)
    enabled: bool = Field(
        default=True,
        description="Whether to show the value labels (automatically set to True when object exists)",
    )

    @field_validator("enabled")
    @classmethod
    def validate_enabled(cls, v: bool) -> bool:
        """Validate that enabled is not explicitly set to False."""
        if v is False:
            raise ValueError(
                "LineValueLabel.enabled cannot be False. To disable value labels, omit the value_labels field entirely."
            )
        return v

    #: Whether to show the last value label
    last: bool = Field(
        default=False,
        description="Whether to show the last value label",
    )

    #: Whether to show the first value label
    first: bool = Field(
        default=False,
        description="Whether to show the first value label",
    )

    #: Whether to show circles at automatically drawn inner value labels
    show_circles: bool = Field(
        default=False,
        alias="showCircles",
        description="Whether to show circles at automatically drawn inner value labels",
    )

    #: The maximum number of inner value labels to show
    max_inner_labels: int = Field(
        default=0,
        alias="maxInnerLabels",
        description="The maximum number of inner value labels to show",
    )


class Line(BaseModel):
    """Configure a line on a Datawrapper line chart."""

    model_config = ConfigDict(populate_by_name=True, strict=True)

    #: The name of the data column for the line
    column: str = Field(
        description="The name of the data column for the line",
    )

    #: The title to display in tooltips and legends
    title: str = Field(
        default="",
        description="The title to display in tooltips and legends",
    )

    #: The interpolation method to use when drawing lines
    interpolation: LineInterpolation | str = Field(
        default="linear",
        description="The interpolation method to use when drawing lines",
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

    #: The width of the line (use LineWidth enum or raw API values)
    width: LineWidth | str = Field(
        default="style1",
        description=(
            "The width of the line. Use LineWidth enum for readability or raw API values "
            "(style0, style1, style2, style3, invisible).\n\n"
            "Examples:\n"
            "  Line(column='sales', width=LineWidth.THICK)  # style2 = 4px\n"
            "  Line(column='sales', width='style2')  # Also 4px\n"
            "  Line(column='sales', width=LineWidth.THINNEST)  # style3 = 1px\n\n"
            "⚠️ Note: style numbers don't increase with thickness! "
            "style0=2px (thin), style1=3px (medium), style2=4px (thick), style3=1px (thinnest)"
        ),
    )

    #: The dashing of the line (use LineDash enum or raw API values)
    dash: LineDash | str | None = Field(
        default=None,
        description="The dashing of the line. Use LineDash enum for readability or raw API values (style1, style2, style3, style4).",
    )

    @field_validator("width")
    @classmethod
    def validate_width(cls, v: LineWidth | str) -> LineWidth | str:
        """Validate width is a valid value.

        Accepts LineWidth enum values or raw API string values.
        """
        # If it's already a LineWidth enum, it's valid
        if isinstance(v, LineWidth):
            return v

        # Define valid raw string values
        valid_values = {"style0", "style1", "style2", "style3", "invisible"}

        if v not in valid_values:
            raise ValueError(
                f"Invalid width: {v}. Use LineWidth enum or valid API values: "
                f"style0, style1, style2, style3, invisible"
            )
        return v

    @field_validator("dash")
    @classmethod
    def validate_dash(cls, v: LineDash | str | None) -> LineDash | str | None:
        """Validate dash is a valid value.

        Accepts LineDash enum values, raw API string values, or None.
        """
        # None is valid (no dashing)
        if v is None:
            return v

        # If it's already a LineDash enum, it's valid
        if isinstance(v, LineDash):
            return v

        # Define valid raw string values
        valid_values = {"style0", "style1", "style2", "style3"}

        if v not in valid_values:
            raise ValueError(
                f"Invalid dash: {v}. Use LineDash enum or valid API values: "
                f"style0, style1, style2, style3"
            )
        return v

    #: Whether or not to show in the color key
    color_key: bool = Field(
        default=False,
        alias="colorKey",
        description="Whether or not to show in the color key",
    )

    #: Whether or not to show a direct label for the line in the right hand margin
    direct_label: bool = Field(
        default=False,
        alias="directLabel",
        description="Whether or not to show a direct label for the line in the right hand margin",
    )

    #: Line outline
    outline: bool = Field(
        default=False,
        alias="bgStroke",
        description="Line outline",
    )

    #: Symbols to display on the line (None = disabled, object = enabled)
    symbols: LineSymbol | None = Field(
        default=None,
        description="Symbols to display on the line (None = disabled, object = enabled)",
    )

    #: The value labels for the line (None = disabled, object = enabled)
    value_labels: LineValueLabel | None = Field(
        default=None,
        alias="valueLabels",
        description="The value labels for the line (None = disabled, object = enabled)",
    )

    #: Whether or not to connect missing points
    connect_missing_points: bool = Field(
        default=False,
        alias="connectMissingPoints",
        description="Whether or not to connect missing points",
    )

    @staticmethod
    def serialize_model(line: "Line") -> dict[str, Any]:
        """Serialize a Line instance to API format.

        Args:
            line: The Line instance to serialize

        Returns:
            Dictionary in the API's expected format
        """
        # Convert enum values to their string representations
        width_value = (
            line.width.value if isinstance(line.width, LineWidth) else line.width
        )
        dash_value = None
        if line.dash is not None:
            dash_value = (
                line.dash.value if isinstance(line.dash, LineDash) else line.dash
            )

        line_dict = {
            "title": line.title,
            "interpolation": line.interpolation,
            "width": width_value,
            "colorKey": line.color_key,
            "directLabel": line.direct_label,
            "bgStroke": line.outline,
            "connectMissingPoints": line.connect_missing_points,
        }

        # Add symbols if configured (None = disabled)
        if line.symbols is not None:
            line_dict["symbols"] = {
                "enabled": line.symbols.enabled,
                "shape": line.symbols.shape,
                "style": line.symbols.style,
                "on": line.symbols.on,
                "size": line.symbols.size,
                "opacity": line.symbols.opacity,
            }
        else:
            line_dict["symbols"] = {"enabled": False}

        # Add value labels if configured (None = disabled)
        if line.value_labels is not None:
            line_dict["valueLabels"] = {
                "enabled": line.value_labels.enabled,
                "last": line.value_labels.last,
                "first": line.value_labels.first,
                "showCircles": line.value_labels.show_circles,
                "maxInnerLabels": line.value_labels.max_inner_labels,
            }
        else:
            line_dict["valueLabels"] = {"enabled": False}

        # Add dash if set
        if dash_value is not None:
            line_dict["dash"] = dash_value

        return line_dict

    @classmethod
    def deserialize_model(cls, line_name: str, line_config: dict) -> dict[str, Any]:
        """Deserialize API line config to Line initialization dict.

        Args:
            line_name: The column name for this line
            line_config: The line configuration from the API

        Returns:
            Dictionary that can be used to initialize a Line instance
        """
        # Parse symbols - only create object if enabled in API
        symbols_obj = line_config.get("symbols", {})
        symbols = None
        if symbols_obj.get("enabled", False):
            symbols = LineSymbol.model_validate(symbols_obj)

        # Parse value labels - only create object if enabled in API
        value_labels_obj = line_config.get("valueLabels", {})
        value_labels = None
        if value_labels_obj.get("enabled", False):
            value_labels = LineValueLabel.model_validate(value_labels_obj)

        # Build the initialization dict, only including values present in API response
        init_dict = {
            "column": line_name,
            "symbols": symbols,
            "value_labels": value_labels,
        }

        # Add optional fields only if present in API response
        if "title" in line_config:
            init_dict["title"] = line_config["title"]
        if "interpolation" in line_config:
            init_dict["interpolation"] = line_config["interpolation"]
        if "width" in line_config:
            init_dict["width"] = line_config["width"]

        # Always include dash field (None if not present in API response)
        init_dict["dash"] = line_config.get("dash")

        if "colorKey" in line_config:
            init_dict["color_key"] = line_config["colorKey"]
        if "directLabel" in line_config:
            init_dict["direct_label"] = line_config["directLabel"]
        if "bgStroke" in line_config:
            init_dict["outline"] = line_config["bgStroke"]
        if "connectMissingPoints" in line_config:
            init_dict["connect_missing_points"] = line_config["connectMissingPoints"]

        return init_dict


class LineChart(
    AnnotationsMixin,
    GridDisplayMixin,
    GridFormatMixin,
    CustomRangeMixin,
    CustomTicksMixin,
    BaseChart,
):
    """A base class for the Datawrapper API's line chart."""

    model_config = ConfigDict(
        populate_by_name=True,
        strict=True,
        validate_assignment=True,
        validate_default=True,
        use_enum_values=True,
        json_schema_extra={
            "examples": [
                {
                    "chart-type": "d3-lines",
                    "title": "Temperature Over Time",
                    "source_name": "Weather Station",
                    "data": pd.DataFrame(
                        {
                            "date": ["2020/01", "2020/02", "2020/03"],
                            "Temperature": [15.0, 18.0, 22.0],
                        }
                    ),
                    "y_grid": "on",
                    "interpolation": "monotone-x",
                }
            ]
        },
    )

    #: The type of datawrapper chart to create
    chart_type: Literal["d3-lines"] = Field(
        default="d3-lines",
        alias="chart-type",
        description="The type of datawrapper chart to create",
    )

    #: The column to use for the x-axis
    x_column: str | None = Field(
        default=None,
        alias="x-column",
        description="The column to use for the x-axis",
    )

    #
    # Horizontal axis (X-axis)
    #
    # Note: x_grid, x_grid_format, custom_range_x, custom_ticks_x inherited from mixins

    #
    # Vertical axis (Y-axis)
    #
    # Note: y_grid, y_grid_format, custom_range_y, custom_ticks_y inherited from mixins

    #: The labeling of the y grid labels
    y_grid_labels: GridLabelPosition | str = Field(
        default="auto",
        alias="y-grid-labels",
        description="The labeling of the y grid labels",
    )

    #: Which side to put the y-axis labels on
    y_grid_label_align: GridLabelAlign | str = Field(
        default="left",
        alias="y-grid-label-align",
        description="Which side to put the y-axis labels on",
    )

    #: How to scale the y-axis
    scale_y: Literal["linear", "log"] = Field(
        default="linear",
        alias="scale-y",
        description="How to scale the y-axis",
    )

    #: Whether or not to subdivide a log scale
    y_grid_subdivide: bool = Field(
        default=True,
        alias="y-grid-subdivide",
        description="Whether or not to subdivide a log scale",
    )

    #
    # Customize lines
    #

    #: The base color for lines (palette index or hex string)
    base_color: str | int = Field(
        default=0,
        alias="base-color",
        description="The base color for lines (palette index or hex string)",
    )

    #: The interpolation method to use when drawing lines
    interpolation: LineInterpolation | str = Field(
        default="linear",
        description="The interpolation method to use when drawing lines",
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

    #: Whether or not to draw a connector line between lines and labels
    connector_lines: bool = Field(
        default=False,
        alias="connector-lines",
        description="Whether or not to draw a connector line between lines and labels",
    )

    #: A mapping of layer names to colors
    color_category: dict[str, str] = Field(
        default_factory=dict,
        alias="color-category",
        description="A mapping of layer names to colors",
    )

    #: Custom configuration for individual lines
    lines: list[Line | dict[str, Any]] = Field(
        default_factory=list,
        description="Custom configuration for individual lines",
    )

    #: Custom area fills
    area_fills: list[AreaFill | dict[str, Any]] = Field(
        default_factory=list,
        alias="area-fills",
        description="Custom area fills",
    )

    #
    # Labels
    #

    #: Whether or not to stack the color legend
    stack_color_legend: bool = Field(
        default=False,
        alias="stack-color-legend",
        description="Whether or not to stack the color legend",
    )

    #: Whether or not to color line category labels the same as the line
    label_colors: bool = Field(
        default=False,
        alias="label-colors",
        description="Whether or not to color line category labels the same as the line",
    )

    #: The amount of margin to leave for the right hand side for labels
    label_margin: int = Field(
        default=0,
        alias="label-margin",
        description="The amount of margin to leave for the right hand side for labels. Zero is automatically calculated.",
    )

    #: The number format for value labels (use DateFormat or NumberFormat enum or custom format strings)
    value_labels_format: DateFormat | NumberFormat | str = Field(
        default="",
        alias="value-labels-format",
        description="The number format for value labels. Use DateFormat for temporal data, NumberFormat for numeric data, or provide custom format strings.",
    )

    #: Whether to color number values labels the same as the line
    value_label_colors: bool = Field(
        default=False,
        alias="value-label-colors",
        description="Whether to color number values labels the same as the line",
    )

    #
    # Tooltips
    #

    #: Whether or not to show tooltips on hover
    show_tooltips: bool = Field(
        default=True,
        alias="show-tooltips",
        description="Whether or not to show tooltips on hover",
    )

    #: The format for the x-axis tooltips (use DateFormat or NumberFormat enum or custom format strings)
    tooltip_x_format: DateFormat | NumberFormat | str = Field(
        default="",
        alias="tooltip-x-format",
        description="The format for the x-axis tooltips. Use DateFormat for temporal data, NumberFormat for numeric data, or provide custom format strings.",
    )

    #: The format of the number tooltip (use DateFormat or NumberFormat enum or custom format strings)
    tooltip_number_format: DateFormat | NumberFormat | str = Field(
        default="",
        alias="tooltip-number-format",
        description="The format of the number tooltip. Use DateFormat for temporal data, NumberFormat for numeric data, or provide custom format strings.",
    )

    #
    # Appearance
    #

    #: How to set the plot height (managed by PlotHeight serializer, not directly serialized)
    plot_height_mode: PlotHeightMode | str = Field(
        default="fixed",
        alias="plot-height-mode",
        description="How to set the plot height (managed by PlotHeight serializer)",
    )

    #: The fixed height of the plot
    plot_height_fixed: int | float = Field(
        default=300,
        alias="plot-height-fixed",
        description="The fixed height of the plot",
    )

    #: The ratio of the plot height
    plot_height_ratio: float = Field(
        default=0.5,
        alias="plot-height-ratio",
        description="The ratio of the plot height",
    )

    @field_validator("plot_height_mode")
    @classmethod
    def validate_plot_height_mode(cls, v: PlotHeightMode | str) -> PlotHeightMode | str:
        """Validate that plot_height_mode is a valid PlotHeightMode value."""
        if isinstance(v, str):
            valid_values = [e.value for e in PlotHeightMode]
            if v not in valid_values:
                raise ValueError(f"Invalid value: {v}. Must be one of {valid_values}")
        return v

    @model_serializer
    def serialize_model(self) -> dict:
        """Serialize the model to a dictionary."""
        # Call the parent class's serialize_model method
        model = super().serialize_model()

        # Set the axes setting if x_column is provided
        if self.x_column:
            model["metadata"]["axes"] = {"x": self.x_column}

        # Add chart specific properties
        visualize_data = {
            # Horizontal axis (from mixins)
            **self._serialize_grid_config(),
            **self._serialize_grid_format(),
            **self._serialize_custom_range(),
            **self._serialize_custom_ticks(),
            # Vertical axis (chart-specific)
            "y-grid-labels": self.y_grid_labels,
            "y-grid-label-align": self.y_grid_label_align,
            "scale-y": self.scale_y,
            "y-grid-subdivide": self.y_grid_subdivide,
            # Customize lines
            "base-color": self.base_color,
            "interpolation": self.interpolation,
            "connector-lines": self.connector_lines,
            "color-category": ColorCategory.serialize(self.color_category),
            # Labels
            "stack-color-legend": self.stack_color_legend,
            "label-colors": self.label_colors,
            "label-margin": self.label_margin,
            "value-labels-format": self.value_labels_format,
            "value-label-colors": self.value_label_colors,
            # Tooltips
            "show-tooltips": self.show_tooltips,
            "tooltip-x-format": self.tooltip_x_format,
            "tooltip-number-format": self.tooltip_number_format,
            # Appearance
            **PlotHeight.serialize(
                self.plot_height_mode,
                self.plot_height_fixed,
                self.plot_height_ratio,
            ),
            # Initialize empty structures
            "lines": {},
            "custom-area-fills": ModelListSerializer.serialize(
                self.area_fills, AreaFill
            ),
        }

        model["metadata"]["visualize"].update(visualize_data)
        model["metadata"]["visualize"].update(self._serialize_annotations())

        # Add line configurations
        for line_obj in self.lines:
            if isinstance(line_obj, dict):
                line_config = Line.model_validate(line_obj)
            else:
                line_config = line_obj

            line_name = line_config.column
            model["metadata"]["visualize"]["lines"][line_name] = Line.serialize_model(
                line_config
            )

        # Return the serialized data
        return model

    @classmethod
    def deserialize_model(cls, api_response: dict[str, Any]) -> dict[str, Any]:
        """Parse Datawrapper API response including line chart specific fields.

        Args:
            api_response: The JSON response from the chart metadata endpoint
            chart_data: The CSV data from the chart data endpoint

        Returns:
            Dictionary that can be used to initialize the LineChart model
        """
        # Call parent to get base fields
        init_data = super().deserialize_model(api_response)

        # Extract line-specific sections
        metadata = api_response.get("metadata", {})
        visualize = metadata.get("visualize", {})

        # Parse axes columns
        axes = metadata.get("axes", {})
        if "x" in axes:
            init_data["x_column"] = axes["x"]

        # Horizontal and vertical axis (from mixins)
        init_data.update(cls._deserialize_grid_config(visualize))
        init_data.update(cls._deserialize_grid_format(visualize))
        init_data.update(cls._deserialize_custom_range(visualize))
        init_data.update(cls._deserialize_custom_ticks(visualize))

        # Vertical axis (chart-specific)
        if "y-grid-labels" in visualize:
            init_data["y_grid_labels"] = visualize["y-grid-labels"]
        if "y-grid-label-align" in visualize:
            init_data["y_grid_label_align"] = visualize["y-grid-label-align"]
        if "scale-y" in visualize:
            init_data["scale_y"] = visualize["scale-y"]
        if "y-grid-subdivide" in visualize:
            init_data["y_grid_subdivide"] = visualize["y-grid-subdivide"]

        # Customize lines
        if "base-color" in visualize:
            init_data["base_color"] = visualize["base-color"]
        if "interpolation" in visualize:
            init_data["interpolation"] = visualize["interpolation"]
        if "connector-lines" in visualize:
            init_data["connector_lines"] = visualize["connector-lines"]

        # Parse color-category using utility
        color_data = ColorCategory.deserialize(visualize.get("color-category"))
        init_data["color_category"] = color_data["color_category"]

        # Parse lines configuration
        lines_obj = visualize.get("lines", {})
        init_data["lines"] = []
        if isinstance(lines_obj, dict):
            for line_name, line_config in lines_obj.items():
                if isinstance(line_config, dict):
                    init_data["lines"].append(
                        Line.deserialize_model(line_name, line_config)
                    )

        # Parse area fills using AreaFill.deserialize_model
        area_fills_data = AreaFill.deserialize_model(visualize.get("custom-area-fills"))

        # Convert dicts to AreaFill objects
        init_data["area_fills"] = [
            AreaFill.model_validate(fill_dict) for fill_dict in area_fills_data
        ]

        # Labels
        if "stack-color-legend" in visualize:
            init_data["stack_color_legend"] = visualize["stack-color-legend"]
        if "label-colors" in visualize:
            init_data["label_colors"] = visualize["label-colors"]
        if "label-margin" in visualize:
            init_data["label_margin"] = visualize["label-margin"]
        if "value-labels-format" in visualize:
            init_data["value_labels_format"] = visualize["value-labels-format"]
        if "value-label-colors" in visualize:
            init_data["value_label_colors"] = visualize["value-label-colors"]

        # Tooltips
        if "show-tooltips" in visualize:
            init_data["show_tooltips"] = visualize["show-tooltips"]
        if "tooltip-x-format" in visualize:
            init_data["tooltip_x_format"] = visualize["tooltip-x-format"]
        if "tooltip-number-format" in visualize:
            init_data["tooltip_number_format"] = visualize["tooltip-number-format"]

        # Appearance
        init_data.update(PlotHeight.deserialize(visualize))

        # Annotations
        init_data.update(cls._deserialize_annotations(visualize))

        return init_data

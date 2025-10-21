from typing import Any, Literal

import pandas as pd
from pydantic import ConfigDict, Field, field_validator, model_serializer

from .annos import RangeAnnotation, TextAnnotation
from .base import BaseChart
from .enums import (
    DateFormat,
    NumberFormat,
    PlotHeightMode,
    RegressionMethod,
    ScatterAxisPosition,
    ScatterGridLines,
    ScatterShape,
    ScatterSize,
)
from .serializers import ModelListSerializer, PlotHeight


class ScatterPlot(BaseChart):
    """A base class for the Datawrapper API's scatter plot chart."""

    model_config = ConfigDict(
        populate_by_name=True,
        strict=True,
        validate_assignment=True,
        validate_default=True,
        use_enum_values=True,
        json_schema_extra={
            "examples": [
                {
                    "chart-type": "d3-scatter-plot",
                    "title": "GDP vs Life Expectancy",
                    "data": pd.DataFrame(
                        {
                            "Country": ["USA", "China", "India"],
                            "GDP": [60000, 15000, 7000],
                            "Life Expectancy": [79, 76, 69],
                            "Population": [330, 1400, 1380],
                        }
                    ),
                    "x_column": "GDP",
                    "y_column": "Life Expectancy",
                    "size_column": "Population",
                }
            ]
        },
    )

    #: The type of datawrapper chart to create
    chart_type: Literal["d3-scatter-plot"] = Field(
        default="d3-scatter-plot",
        alias="chart-type",
        description="The type of datawrapper chart to create",
    )

    #
    # Horizontal axis
    #

    #: The column to use for the x-axis
    x_column: str | None = Field(
        default=None,
        alias="x-column",
        description="The column to use for the x-axis",
    )

    #: The range for the x-axis
    x_range: tuple[Any, Any] | list[Any] = Field(
        default=("", ""),
        alias="x-range",
        description="The range for the x-axis",
    )

    #: Custom ticks for the x-axis
    x_ticks: list[Any] = Field(
        default_factory=list,
        alias="x-ticks",
        description="Custom ticks for the x-axis",
    )

    #: Set the x-axis on a Logarithmic scale
    x_log: bool = Field(
        default=False,
        alias="x-log",
        description="Set the x-axis on a Logarithmic scale",
    )

    #: Format of the x-axis ticks (use DateFormat or NumberFormat enum or custom format strings)
    x_format: DateFormat | NumberFormat | str = Field(
        default="",
        alias="x-format",
        description="Format of the x-axis ticks. Use DateFormat for temporal data, NumberFormat for numeric data, or provide custom format strings.",
    )

    #: The position of the x-axis ticks and labels
    x_position: ScatterAxisPosition | str = Field(
        default="bottom",
        alias="x-position",
        description="The position of the x-axis ticks and labels",
    )

    #: How to display x-axis grid lines
    x_grid_lines: ScatterGridLines | str = Field(
        default="on",
        alias="x-grid-lines",
        description="How to display x-axis grid lines",
    )

    #
    # Vertical axis
    #

    #: The column to use for the y-axis
    y_column: str | None = Field(
        default=None,
        alias="y-column",
        description="The column to use for the y-axis",
    )

    #: The range for the y-axis
    y_range: tuple[Any, Any] | list[Any] = Field(
        default=("", ""),
        alias="y-range",
        description="The range for the y-axis",
    )

    #: Custom ticks for the y-axis
    y_ticks: list[Any] = Field(
        default_factory=list,
        alias="y-ticks",
        description="Custom ticks for the y-axis",
    )

    #: Set the y-axis on a Logarithmic scale
    y_log: bool = Field(
        default=False,
        alias="y-log",
        description="Set the y-axis on a Logarithmic scale",
    )

    #: Format of the y-axis ticks (use DateFormat or NumberFormat enum or custom format strings)
    y_format: DateFormat | NumberFormat | str = Field(
        default="",
        alias="y-format",
        description="Format of the y-axis ticks. Use DateFormat for temporal data, NumberFormat for numeric data, or provide custom format strings.",
    )

    #: The position of the y-axis ticks and labels
    y_position: ScatterAxisPosition | str = Field(
        default="bottom",
        alias="y-position",
        description="The position of the y-axis ticks and labels",
    )

    #: How to display y-axis grid lines
    y_grid_lines: ScatterGridLines | str = Field(
        default="on",
        alias="y-grid-lines",
        description="How to display y-axis grid lines",
    )

    #
    # Color
    #

    #: The default color (palette index or hex string)
    base_color: str | int = Field(
        default=0,
        alias="base-color",
        description="The default color (palette index or hex string)",
    )

    #: The opacity of the points
    opacity: float = Field(
        default=1.0,
        description="The opacity of the points",
    )

    #: Whether to show an outline stroke on points
    outlines: bool = Field(
        default=False,
        description="Whether to show an outline stroke on points",
    )

    #: The color of the outline stroke
    color_outline: str = Field(
        default="#000000",
        alias="color-outline",
        description="The color of the outline stroke",
    )

    #: Whether to show the color key
    show_color_key: bool = Field(
        default=False,
        alias="show-color-key",
        description="Whether to show the color key",
    )

    #
    # Size
    #

    #: How the size is set
    size: ScatterSize | str = Field(
        default="fixed",
        description="How the size is set",
    )

    #: The fixed size, if it's set that way
    fixed_size: int | float = Field(
        default=5,
        alias="fixed-size",
        description="The fixed size, if it's set that way",
    )

    #: The dynamic column to size with
    size_column: str | None = Field(
        default=None,
        alias="size-column",
        description="The dynamic column to size with",
    )

    #: The maximum size of a dynamic setting
    max_size: int | float = Field(
        default=25,
        alias="max-size",
        description="The maximum size of a dynamic setting",
    )

    #: Whether to reduce the size on mobile phones
    responsive_symbol_size: bool = Field(
        default=False,
        alias="responsive-symbol-size",
        description="Whether to reduce the size on mobile phones",
    )

    #: Whether to show the size legend
    show_size_legend: bool = Field(
        default=False,
        alias="show-size-legend",
        description="Whether to show the size legend",
    )

    #: Where to show the size legend
    size_legend_position: Literal[
        "above",
        "below",
        "inside-left-top",
        "inside-center-top",
        "inside-right-top",
        "inside-left-bottom",
        "inside-center-bottom",
        "inside-right-bottom",
    ] = Field(
        default="above",
        alias="size-legend-position",
        description="Where to show the size legend",
    )

    #: The percentage offset of the size legend on the x-axis
    legend_offset_x: int = Field(
        default=0,
        alias="legend-offset-x",
        description="The percentage offset of the size legend on the x-axis",
    )

    #: The percentage offset of the size legend on the y-axis
    legend_offset_y: int = Field(
        default=0,
        alias="legend-offset-y",
        description="The percentage offset of the size legend on the y-axis",
    )

    #: How to format the values of the size legend
    size_legend_values_format: Literal["auto", "custom"] = Field(
        default="auto",
        alias="size-legend-values-format",
        description="How to format the values of the size legend",
    )

    #: The list of values to include in the size legend
    size_legend_values: list[int | float] = Field(
        default_factory=list,
        alias="size-legend-values",
        description="The list of values to include in the size legend",
    )

    #: Where to put the value labels on the size legend
    size_legend_label_position: Literal["below", "right"] = Field(
        default="below",
        alias="size-legend-label-position",
        description="Where to put the value labels on the size legend",
    )

    #: How to format the size legend label values (use DateFormat or NumberFormat enum or custom format strings)
    size_legend_label_format: DateFormat | NumberFormat | str = Field(
        default="",
        alias="size-legend-label-format",
        description="How to format the size legend label values. Use DateFormat for temporal data, NumberFormat for numeric data, or provide custom format strings.",
    )

    #: Whether to show a size legend title
    size_legend_title_enabled: bool = Field(
        default=False,
        alias="size-legend-title-enabled",
        description="Whether to show a size legend title",
    )

    #: What to put in the size legend title
    size_legend_title: str = Field(
        default="",
        alias="size-legend-title",
        description="What to put in the size legend title",
    )

    #: Where to put the size legend title
    size_legend_title_position: Literal["left", "right", "above", "below"] = Field(
        default="left",
        alias="size-legend-title-position",
        description="Where to put the size legend title",
    )

    #: The maximum width of the size legend title in pixels
    size_legend_title_width: int | float = Field(
        default=200,
        alias="size-legend-title-width",
        description="The maximum width of the size legend title in pixels",
    )

    #
    # Shape
    #

    #: How to set the shape
    shape: ScatterShape | str = Field(
        default="fixed",
        description="How to set the shape",
    )

    #: Options for the shape
    fixed_shape: ScatterShape | str = Field(
        default="symbolCircle",
        alias="fixed-shape",
        description="Options for the shape",
    )

    #: The columns to get the variable shapes for
    shape_column: str | None = Field(
        default=None,
        alias="shape-column",
        description="The columns to get the variable shapes for",
    )

    #
    # Trend line
    #

    #: Whether or not to show a regression line
    regression: bool = Field(
        default=False,
        description="Whether or not to show a regression line",
    )

    #: The regression method to use
    regression_method: RegressionMethod | str = Field(
        default="linear",
        alias="regression-method",
        description="The regression method to use",
    )

    #
    # Appearance
    #

    #: How to set the plot height
    plot_height_mode: PlotHeightMode | str = Field(
        default="fixed",
        alias="plot-height-mode",
        description="How to set the plot height",
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

    #
    # Annotations
    #

    #: A list of text annotations to display on the chart
    text_annotations: list[dict[Any, Any]] = Field(
        default_factory=list,
        alias="text-annotations",
        description="A list of text annotations to display on the chart",
    )

    #: A list of range annotations to display on the chart
    range_annotations: list[dict[Any, Any]] = Field(
        default_factory=list,
        alias="range-annotations",
        description="A list of range annotations to display on the chart",
    )

    #: Add custom lines on the chart
    custom_lines: str = Field(
        default="",
        alias="custom-lines",
        description="Add custom lines on the chart",
    )

    #
    # Labeling
    #

    #: The column to use for the labels
    label_column: str | None = Field(
        default=None,
        alias="label-column",
        description="The column to use for the labels",
    )

    #: Whether to automatically label symbols
    auto_labels: bool = Field(
        default=True,
        alias="auto-labels",
        description="Whether to automatically label symbols",
    )

    #: Values to add labels for
    add_labels: list[Any] = Field(
        default_factory=list,
        alias="add-labels",
        description="Values to add labels for",
    )

    #: Whether to highlight labeled symbols
    highlight_labeled: bool = Field(
        default=True,
        alias="highlight-labeled",
        description="Whether to highlight labeled symbols",
    )

    #
    # Tooltips
    #

    #: Whether to show tooltips
    tooltip_enabled: bool = Field(
        default=True,
        alias="tooltip-enabled",
        description="Whether to show tooltips",
    )

    #: Tooltip title format
    tooltip_title: str = Field(
        default="",
        alias="tooltip-title",
        description="Tooltip title format",
    )

    #: Tooltip body format
    tooltip_body: str = Field(
        default="",
        alias="tooltip-body",
        description="Tooltip body format",
    )

    #: Whether the tooltip is sticky on click
    tooltip_sticky: bool = Field(
        default=False,
        alias="tooltip-sticky",
        description="Whether the tooltip is sticky on click",
    )

    @model_serializer
    def serialize_model(self) -> dict:
        """Serialize the model to a dictionary."""
        # Call the parent class's serialize_model method
        model = super().serialize_model()

        # Set the axes setting
        axes = {}
        if self.x_column:
            axes["x"] = self.x_column
        if self.y_column:
            axes["y"] = self.y_column
        if self.size_column:
            axes["size"] = self.size_column
        if self.shape_column:
            axes["shape"] = self.shape_column
        if self.label_column:
            axes["labels"] = self.label_column

        # Add axes to metadata
        model["metadata"]["axes"] = axes

        # Add chart specific properties to visualize section
        model["metadata"]["visualize"].update(
            {
                # Horizontal axis
                "x-axis": {
                    "log": self.x_log,
                    "range": self.x_range,
                    "ticks": self.x_ticks,
                },
                "x-format": self.x_format,
                "x-pos": self.x_position,
                "x-grid-lines": self.x_grid_lines,
                # Vertical axis
                "y-axis": {
                    "log": self.y_log,
                    "range": self.y_range,
                    "ticks": self.y_ticks,
                },
                "y-format": self.y_format,
                "y-pos": self.y_position,
                "y-grid-lines": self.y_grid_lines,
                # Colors
                "base-color": self.base_color,
                "opacity": self.opacity,
                "outlines": self.outlines,
                "color-outline": self.color_outline,
                "show-color-key": self.show_color_key,
                # Size
                "size": self.size,
                "fixed-size": self.fixed_size,
                "max-size": self.max_size,
                "responsive-symbol-size": self.responsive_symbol_size,
                "show-size-legend": self.show_size_legend,
                "size-legend-position": self.size_legend_position,
                "legend-offset-x": self.legend_offset_x,
                "legend-offset-y": self.legend_offset_y,
                "size-legend-values-setting": self.size_legend_values_format,
                "size-legend-values": self.size_legend_values,
                "size-legend-label-position": self.size_legend_label_position,
                "size-legend-label-format": self.size_legend_label_format,
                "size-legend-title-enabled": self.size_legend_title_enabled,
                "size-legend-title": self.size_legend_title,
                "size-legend-title-position": self.size_legend_title_position,
                "size-legend-title-width": self.size_legend_title_width,
                # Shapes
                "shape": self.shape,
                "fixed-shape": self.fixed_shape,
                # Trend line
                "regression": self.regression,
                "regression-method": self.regression_method,
                # Appearance
                **PlotHeight.serialize(
                    self.plot_height_mode,
                    self.plot_height_fixed,
                    self.plot_height_ratio,
                ),
                # Annotations
                "text-annotations": ModelListSerializer.serialize(
                    self.text_annotations, TextAnnotation
                ),
                "range-annotations": ModelListSerializer.serialize(
                    self.range_annotations, RangeAnnotation
                ),
                "custom-lines": self.custom_lines,
                # Labeling
                "auto-labels": self.auto_labels,
                "add-labels": self.add_labels,
                "highlight-labeled": self.highlight_labeled,
                # Tooltips
                "tooltip": {
                    "body": self.tooltip_body,
                    "title": self.tooltip_title,
                    "sticky": self.tooltip_sticky,
                    "enabled": self.tooltip_enabled,
                    "migrated": True,
                },
            }
        )

        # Return the serialized data
        return model

    @classmethod
    def deserialize_model(cls, api_response: dict[str, Any]) -> dict[str, Any]:
        """Parse Datawrapper API response including scatter plot specific fields.

        Args:
            api_response: The JSON response from the chart metadata endpoint
            chart_data: The CSV data from the chart data endpoint

        Returns:
            Dictionary that can be used to initialize the ScatterPlot model
        """
        # Call parent to get base fields
        init_data = super().deserialize_model(api_response)

        # Extract scatter-specific sections
        metadata = api_response.get("metadata", {})
        visualize = metadata.get("visualize", {})
        axes = metadata.get("axes", {})

        # Parse axes columns
        init_data["x_column"] = axes.get("x")
        init_data["y_column"] = axes.get("y")
        init_data["size_column"] = axes.get("size")
        init_data["shape_column"] = axes.get("shape")
        init_data["label_column"] = axes.get("labels")

        # Parse x-axis
        x_axis = visualize.get("x-axis", {})
        if isinstance(x_axis, dict):
            init_data["x_log"] = x_axis.get("log", False)
            init_data["x_range"] = x_axis.get("range", ["", ""])
            init_data["x_ticks"] = x_axis.get("ticks", [])
        else:
            init_data["x_log"] = False
            init_data["x_range"] = ["", ""]
            init_data["x_ticks"] = []

        if "x-format" in visualize:
            init_data["x_format"] = visualize["x-format"]
        if "x-pos" in visualize:
            init_data["x_position"] = visualize["x-pos"]
        if "x-grid-lines" in visualize:
            init_data["x_grid_lines"] = visualize["x-grid-lines"]

        # Parse y-axis
        y_axis = visualize.get("y-axis", {})
        if isinstance(y_axis, dict):
            init_data["y_log"] = y_axis.get("log", False)
            init_data["y_range"] = y_axis.get("range", ["", ""])
            init_data["y_ticks"] = y_axis.get("ticks", [])
        else:
            init_data["y_log"] = False
            init_data["y_range"] = ["", ""]
            init_data["y_ticks"] = []

        if "y-format" in visualize:
            init_data["y_format"] = visualize["y-format"]
        if "y-pos" in visualize:
            init_data["y_position"] = visualize["y-pos"]
        if "y-grid-lines" in visualize:
            init_data["y_grid_lines"] = visualize["y-grid-lines"]

        # Colors
        if "base-color" in visualize:
            init_data["base_color"] = visualize["base-color"]
        if "opacity" in visualize:
            init_data["opacity"] = visualize["opacity"]
        if "outlines" in visualize:
            init_data["outlines"] = visualize["outlines"]
        if "color-outline" in visualize:
            init_data["color_outline"] = visualize["color-outline"]
        if "show-color-key" in visualize:
            init_data["show_color_key"] = visualize["show-color-key"]

        # Size
        if "size" in visualize:
            init_data["size"] = visualize["size"]
        if "fixed-size" in visualize:
            init_data["fixed_size"] = visualize["fixed-size"]
        if "max-size" in visualize:
            init_data["max_size"] = visualize["max-size"]
        if "responsive-symbol-size" in visualize:
            init_data["responsive_symbol_size"] = visualize["responsive-symbol-size"]
        if "show-size-legend" in visualize:
            init_data["show_size_legend"] = visualize["show-size-legend"]
        if "size-legend-position" in visualize:
            init_data["size_legend_position"] = visualize["size-legend-position"]
        if "legend-offset-x" in visualize:
            init_data["legend_offset_x"] = visualize["legend-offset-x"]
        if "legend-offset-y" in visualize:
            init_data["legend_offset_y"] = visualize["legend-offset-y"]
        if "size-legend-values-setting" in visualize:
            init_data["size_legend_values_format"] = visualize[
                "size-legend-values-setting"
            ]
        if "size-legend-values" in visualize:
            init_data["size_legend_values"] = visualize["size-legend-values"]
        if "size-legend-label-position" in visualize:
            init_data["size_legend_label_position"] = visualize[
                "size-legend-label-position"
            ]
        if "size-legend-label-format" in visualize:
            init_data["size_legend_label_format"] = visualize[
                "size-legend-label-format"
            ]
        if "size-legend-title-enabled" in visualize:
            init_data["size_legend_title_enabled"] = visualize[
                "size-legend-title-enabled"
            ]
        if "size-legend-title" in visualize:
            init_data["size_legend_title"] = visualize["size-legend-title"]
        if "size-legend-title-position" in visualize:
            init_data["size_legend_title_position"] = visualize[
                "size-legend-title-position"
            ]
        if "size-legend-title-width" in visualize:
            init_data["size_legend_title_width"] = visualize["size-legend-title-width"]

        # Shape
        if "shape" in visualize:
            init_data["shape"] = visualize["shape"]
        if "fixed-shape" in visualize:
            init_data["fixed_shape"] = visualize["fixed-shape"]

        # Trend line
        if "regression" in visualize:
            init_data["regression"] = visualize["regression"]
        if "regression-method" in visualize:
            init_data["regression_method"] = visualize["regression-method"]

        # Appearance
        init_data.update(PlotHeight.deserialize(visualize))

        # Annotations
        init_data["text_annotations"] = TextAnnotation.deserialize_model(
            visualize.get("text-annotations")
        )
        init_data["range_annotations"] = RangeAnnotation.deserialize_model(
            visualize.get("range-annotations")
        )

        if "custom-lines" in visualize:
            init_data["custom_lines"] = visualize["custom-lines"]

        # Labeling
        if "auto-labels" in visualize:
            init_data["auto_labels"] = visualize["auto-labels"]
        if "add-labels" in visualize:
            init_data["add_labels"] = visualize["add-labels"]
        if "highlight-labeled" in visualize:
            init_data["highlight_labeled"] = visualize["highlight-labeled"]

        # Tooltips
        tooltip = visualize.get("tooltip", {})
        if isinstance(tooltip, dict):
            init_data["tooltip_enabled"] = tooltip.get("enabled", True)
            init_data["tooltip_title"] = tooltip.get("title", "")
            init_data["tooltip_body"] = tooltip.get("body", "")
            init_data["tooltip_sticky"] = tooltip.get("sticky", False)
        else:
            init_data["tooltip_enabled"] = True
            init_data["tooltip_title"] = ""
            init_data["tooltip_body"] = ""
            init_data["tooltip_sticky"] = False

        return init_data

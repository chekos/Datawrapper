from typing import Any, Literal

import pandas as pd
from pydantic import ConfigDict, Field, model_serializer

from .annos import RangeAnnotation, TextAnnotation
from .base import BaseChart


class ScatterPlot(BaseChart):
    """A base class for the Datawrapper API's scatter plot chart."""

    model_config = ConfigDict(
        populate_by_name=True,
        strict=True,
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

    #: Format of the x-axis ticks
    x_format: str = Field(
        default="",
        alias="x-format",
        description="Format of the x-axis ticks",
    )

    #: The position of the x-axis ticks and labels
    x_position: Literal["bottom", "top", "zero", "off"] = Field(
        default="bottom",
        alias="x-position",
        description="The position of the x-axis ticks and labels",
    )

    #: How to display x-axis grid lines
    x_grid_lines: Literal["on", "off", "no-labels", "just-labels"] = Field(
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

    #: Format of the y-axis ticks
    y_format: str = Field(
        default="",
        alias="y-format",
        description="Format of the y-axis ticks",
    )

    #: The position of the y-axis ticks and labels
    y_position: Literal["bottom", "top", "zero", "off", "left", "right"] = Field(
        default="bottom",
        alias="y-position",
        description="The position of the y-axis ticks and labels",
    )

    #: How to display y-axis grid lines
    y_grid_lines: Literal["on", "off", "no-labels", "just-labels"] = Field(
        default="on",
        alias="y-grid-lines",
        description="How to display y-axis grid lines",
    )

    #
    # Color
    #

    #: The default color (can be hex string or palette index)
    base_color: str | int = Field(
        default="#3182bd",
        alias="base-color",
        description="The default color (can be hex string or palette index)",
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
    size: Literal["fixed", "dynamic"] = Field(
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

    #: How to format the size legend label values
    size_legend_label_format: str = Field(
        default="",
        alias="size-legend-label-format",
        description="How to format the size legend label values",
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
    shape: Literal["fixed", "dynamic"] = Field(
        default="fixed",
        description="How to set the shape",
    )

    #: Options for the shape
    fixed_shape: Literal[
        "symbolCircle",
        "symbolCross",
        "symbolDiamond",
        "symbolSquare",
        "symbolStar",
        "symbolTriangle",
        "symbolTriangleDown",
        "symbolWye",
    ] = Field(
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
    regression_method: Literal[
        "linear",
        "quadratic",
        "cubic",
        "power",
        "logarithmic",
        "exponential",
    ] = Field(
        default="linear",
        alias="regression-method",
        description="The regression method to use",
    )

    #
    # Appearance
    #

    #: How to set the plot height
    plot_height_mode: Literal["ratio", "fixed"] = Field(
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
    labels_column: str | None = Field(
        default=None,
        alias="labels-column",
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
        if self.labels_column:
            axes["labels"] = self.labels_column

        # Add axes to metadata
        model["axes"] = axes

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
                "plotHeightMode": self.plot_height_mode,
                "plotHeightFixed": self.plot_height_fixed,
                "plotHeightRatio": self.plot_height_ratio,
                # Annotations
                "text-annotations": [
                    TextAnnotation(**anno).model_dump(by_alias=True)
                    for anno in self.text_annotations
                ],
                "range-annotations": [
                    RangeAnnotation(**anno).model_dump(by_alias=True)
                    for anno in self.range_annotations
                ],
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
        # Axes can be at top level or in metadata
        axes = api_response.get("axes", metadata.get("axes", {}))

        # Parse axes columns
        init_data["x_column"] = axes.get("x")
        init_data["y_column"] = axes.get("y")
        init_data["size_column"] = axes.get("size")
        init_data["shape_column"] = axes.get("shape")
        init_data["labels_column"] = axes.get("labels")

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

        init_data["x_format"] = visualize.get("x-format", "")
        init_data["x_position"] = visualize.get("x-pos", "bottom")
        init_data["x_grid_lines"] = visualize.get("x-grid-lines", "on")

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

        init_data["y_format"] = visualize.get("y-format", "")
        init_data["y_position"] = visualize.get("y-pos", "bottom")
        init_data["y_grid_lines"] = visualize.get("y-grid-lines", "on")

        # Colors
        init_data["base_color"] = visualize.get("base-color", "#3182bd")
        init_data["opacity"] = visualize.get("opacity", 1.0)
        init_data["outlines"] = visualize.get("outlines", False)
        init_data["color_outline"] = visualize.get("color-outline", "#000000")
        init_data["show_color_key"] = visualize.get("show-color-key", False)

        # Size
        init_data["size"] = visualize.get("size", "fixed")
        init_data["fixed_size"] = visualize.get("fixed-size", 5)
        init_data["max_size"] = visualize.get("max-size", 25)
        init_data["responsive_symbol_size"] = visualize.get(
            "responsive-symbol-size", False
        )
        init_data["show_size_legend"] = visualize.get("show-size-legend", False)
        init_data["size_legend_position"] = visualize.get(
            "size-legend-position", "above"
        )
        init_data["legend_offset_x"] = visualize.get("legend-offset-x", 0)
        init_data["legend_offset_y"] = visualize.get("legend-offset-y", 0)
        init_data["size_legend_values_format"] = visualize.get(
            "size-legend-values-setting", "auto"
        )
        init_data["size_legend_values"] = visualize.get("size-legend-values", [])
        init_data["size_legend_label_position"] = visualize.get(
            "size-legend-label-position", "below"
        )
        init_data["size_legend_label_format"] = visualize.get(
            "size-legend-label-format", ""
        )
        init_data["size_legend_title_enabled"] = visualize.get(
            "size-legend-title-enabled", False
        )
        init_data["size_legend_title"] = visualize.get("size-legend-title", "")
        init_data["size_legend_title_position"] = visualize.get(
            "size-legend-title-position", "left"
        )
        init_data["size_legend_title_width"] = visualize.get(
            "size-legend-title-width", 200
        )

        # Shape
        init_data["shape"] = visualize.get("shape", "fixed")
        init_data["fixed_shape"] = visualize.get("fixed-shape", "symbolCircle")

        # Trend line
        init_data["regression"] = visualize.get("regression", False)
        init_data["regression_method"] = visualize.get("regression-method", "linear")

        # Appearance
        init_data["plot_height_mode"] = visualize.get("plotHeightMode", "fixed")
        init_data["plot_height_fixed"] = visualize.get("plotHeightFixed", 300)
        init_data["plot_height_ratio"] = visualize.get("plotHeightRatio", 0.5)

        # Annotations
        text_annos = visualize.get("text-annotations", {})
        if isinstance(text_annos, dict):
            init_data["text_annotations"] = list(text_annos.values())
        elif isinstance(text_annos, list):
            init_data["text_annotations"] = text_annos
        else:
            init_data["text_annotations"] = []

        range_annos = visualize.get("range-annotations", {})
        if isinstance(range_annos, dict):
            init_data["range_annotations"] = list(range_annos.values())
        elif isinstance(range_annos, list):
            init_data["range_annotations"] = range_annos
        else:
            init_data["range_annotations"] = []

        init_data["custom_lines"] = visualize.get("custom-lines", "")

        # Labeling
        init_data["auto_labels"] = visualize.get("auto-labels", True)
        init_data["add_labels"] = visualize.get("add-labels", [])
        init_data["highlight_labeled"] = visualize.get("highlight-labeled", True)

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

    @classmethod
    def from_api(cls, api_response: dict[str, Any]) -> "ScatterPlot":
        """Create a ScatterPlot instance from API response data.

        Args:
            api_response: The JSON response from the chart metadata endpoint
            chart_data: The CSV data from the chart data endpoint

        Returns:
            A ScatterPlot instance populated with the API data
        """
        init_data = cls.deserialize_model(api_response)
        return cls(**init_data)

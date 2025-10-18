from typing import Any, Literal

import pandas as pd
from pydantic import ConfigDict, Field, field_validator, model_serializer

from .annos import RangeAnnotation, TextAnnotation
from .base import BaseChart
from .enums import (
    DateFormat,
    GridDisplay,
    GridLabelAlign,
    GridLabelPosition,
    NumberFormat,
    PlotHeightMode,
    ValueLabelDisplay,
    ValueLabelPlacement,
)
from .serializers import (
    ColorCategory,
    CustomRange,
    CustomTicks,
    ModelListSerializer,
    NegativeColor,
    PlotHeight,
    ValueLabels,
)


class ColumnChart(BaseChart):
    """A base class for the Datawrapper API's column chart."""

    model_config = ConfigDict(
        populate_by_name=True,
        strict=True,
        validate_assignment=True,
        validate_default=True,
        use_enum_values=True,
        json_schema_extra={
            "examples": [
                {
                    "chart-type": "column-chart",
                    "title": "Unemployment Rate Over Time",
                    "source_name": "Bureau of Labor Statistics",
                    "data": pd.DataFrame(
                        {
                            "date": ["2020/01", "2020/02", "2020/03"],
                            "Value": [4.0, 3.8, 4.5],
                        }
                    ),
                    "y_grid": True,
                    "value_labels": "always",
                }
            ]
        },
    )

    #: The type of datawrapper chart to create
    chart_type: Literal["column-chart"] = Field(
        default="column-chart",
        alias="chart-type",
        description="The type of datawrapper chart to create",
    )

    #
    # Horizontal axis (X-axis)
    #

    #: The custom range for the x axis
    custom_range_x: list[Any] | tuple[Any, Any] = Field(
        default_factory=lambda: ["", ""],
        alias="custom-range-x",
        description="The custom range for the x axis",
    )

    #: The custom ticks for the x axis
    custom_ticks_x: list[Any] = Field(
        default_factory=list,
        alias="custom-ticks-x",
        description="The custom ticks for the x axis",
    )

    #: The formatting for the x grid labels (use DateFormat or NumberFormat enum or custom format strings)
    x_grid_format: DateFormat | NumberFormat | str = Field(
        default="auto",
        alias="x-grid-format",
        description="The formatting for the x grid labels. Use DateFormat for temporal data, NumberFormat for numeric data, or provide custom format strings.",
    )

    #: Whether to show the x grid
    x_grid: GridDisplay | str = Field(
        default="off",
        alias="x-grid",
        description="Whether to show the x grid",
    )

    #
    # Vertical axis (Y-axis)
    #

    #: The custom range for the y axis
    custom_range_y: list[Any] | tuple[Any, Any] = Field(
        default_factory=lambda: ["", ""],
        alias="custom-range-y",
        description="The custom range for the y axis",
    )

    #: The custom ticks for the y axis
    custom_ticks_y: list[Any] = Field(
        default_factory=list,
        alias="custom-ticks-y",
        description="The custom ticks for the y axis",
    )

    #: The formatting for the y grid labels (use DateFormat or NumberFormat enum or custom format strings)
    y_grid_format: DateFormat | NumberFormat | str = Field(
        default="",
        alias="y-grid-format",
        description="The formatting for the y grid labels. Use DateFormat for temporal data, NumberFormat for numeric data, or provide custom format strings.",
    )

    #: Whether to show the y grid lines
    y_grid: bool = Field(
        default=True,
        alias="y-grid",
        description="Whether to show the y grid lines",
    )

    #: The labeling of the y grid labels
    y_grid_labels: GridLabelPosition | str = Field(
        default="outside",
        alias="y-grid-labels",
        description="The labeling of the y grid labels",
    )

    #: Which side to put the y-axis labels on
    y_grid_label_align: GridLabelAlign | str = Field(
        default="left",
        alias="y-grid-label-align",
        description="Which side to put the y-axis labels on",
    )

    #
    # Appearance
    #

    #: The base color for the chart (palette index or hex string)
    base_color: str | int = Field(
        default=0,
        alias="base-color",
        description="The base color for the chart (palette index or hex string)",
    )

    #: The negative color to use, if you want one
    negative_color: str | None = Field(
        default=None,
        alias="negative-color",
        description="The negative color to use, if you want one",
    )

    #: A mapping of layer names to colors
    color_category: dict[str, str] = Field(
        default_factory=dict,
        alias="color-category",
        description="A mapping of layer names to colors",
    )

    #: Dictionary mapping category names to their display labels in the color legend
    category_labels: dict[str, str] = Field(
        default_factory=dict,
        alias="category-labels",
        description="Dictionary mapping category names to their display labels in the color legend",
    )

    #: List defining the order in which categories appear in the chart and legend
    category_order: list[str] = Field(
        default_factory=list,
        alias="category-order",
        description="List defining the order in which categories appear in the chart and legend",
    )

    #: The padding between bars as a percentage of the bar width
    bar_padding: int = Field(
        default=30,
        alias="bar-padding",
        description="The padding between bars as a percentage of the bar width",
    )

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

    #
    # Labels
    #

    #: Whether or not to show the color key above the chart
    show_color_key: bool = Field(
        default=False,
        alias="show-color-key",
        description="Whether or not to show the color key above the chart",
    )

    #: Whether or not to show value labels
    show_value_labels: ValueLabelDisplay | str = Field(
        default="hover",
        alias="show-value-labels",
        description="Whether or not to show value labels",
    )

    #: How to format the value labels (use DateFormat or NumberFormat enum or custom format strings)
    value_labels_format: DateFormat | NumberFormat | str = Field(
        default="",
        alias="value-labels-format",
        description="How to format the value labels. Use DateFormat for temporal data, NumberFormat for numeric data, or provide custom format strings.",
    )

    #: Where to place the value labels
    value_labels_placement: ValueLabelPlacement | str = Field(
        default="outside",
        alias="value-labels-placement",
        description="Where to place the value labels",
    )

    #
    # Annotations
    #

    #: A list of text annotations to display on the chart
    text_annotations: list[TextAnnotation | dict[Any, Any]] = Field(
        default_factory=list,
        alias="text-annotations",
        description="A list of text annotations to display on the chart",
    )

    #: A list of range annotations to display on the chart
    range_annotations: list[RangeAnnotation | dict[Any, Any]] = Field(
        default_factory=list,
        alias="range-annotations",
        description="A list of range annotations to display on the chart",
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

        # Add chart specific properties
        model["metadata"]["visualize"].update(
            {
                # Horizontal axis
                "custom-range-x": CustomRange.serialize(self.custom_range_x),
                "custom-ticks-x": CustomTicks.serialize(self.custom_ticks_x),
                "x-grid-format": self.x_grid_format,
                "grid-lines-x": {
                    "type": "" if self.x_grid == "off" else self.x_grid,
                    "enabled": self.x_grid != "off",
                },
                # Vertical axis
                "custom-range": CustomRange.serialize(self.custom_range_y),
                "custom-ticks": CustomTicks.serialize(self.custom_ticks_y),
                "y-grid-format": self.y_grid_format,
                "grid-lines": self.y_grid,
                "yAxisLabels": {
                    "enabled": self.y_grid_labels != "off",
                    "alignment": self.y_grid_label_align,
                    "placement": ""
                    if self.y_grid_labels == "off"
                    else self.y_grid_labels,
                },
                # Appearance
                "base-color": self.base_color,
                "negativeColor": NegativeColor.serialize(self.negative_color),
                "bar-padding": self.bar_padding,
                "color-category": ColorCategory.serialize(
                    self.color_category,
                    self.category_labels,
                    self.category_order,
                ),
                "color-by-column": bool(self.color_category),
                **PlotHeight.serialize(
                    self.plot_height_mode,
                    self.plot_height_fixed,
                    self.plot_height_ratio,
                ),
                # Labels
                "show-color-key": self.show_color_key,
                **ValueLabels.serialize(
                    show=self.show_value_labels,
                    format_str=self.value_labels_format,
                    placement=self.value_labels_placement,
                    chart_type="column",
                ),
                # Annotations
                "text-annotations": ModelListSerializer.serialize(
                    self.text_annotations, TextAnnotation
                ),
                "range-annotations": ModelListSerializer.serialize(
                    self.range_annotations, RangeAnnotation
                ),
            }
        )

        # Return the serialized data
        return model

    @classmethod
    def deserialize_model(cls, api_response: dict[str, Any]) -> dict[str, Any]:
        """Parse Datawrapper API response including column chart specific fields.

        Args:
            api_response: The JSON response from the chart metadata endpoint
            chart_data: The CSV data from the chart data endpoint

        Returns:
            Dictionary that can be used to initialize the ColumnChart model
        """
        # Call parent to get base fields
        init_data = super().deserialize_model(api_response)

        # Extract column-specific sections
        metadata = api_response.get("metadata", {})
        visualize = metadata.get("visualize", {})

        # Horizontal axis (X-axis)
        init_data["custom_range_x"] = CustomRange.deserialize(
            visualize.get("custom-range-x")
        )
        init_data["custom_ticks_x"] = CustomTicks.deserialize(
            visualize.get("custom-ticks-x", "")
        )
        if "x-grid-format" in visualize:
            init_data["x_grid_format"] = visualize["x-grid-format"]

        # Parse grid-lines-x
        if "grid-lines-x" in visualize:
            grid_lines_x = visualize["grid-lines-x"]
            if isinstance(grid_lines_x, dict):
                enabled = grid_lines_x.get("enabled", False)
                grid_type = grid_lines_x.get("type", "")
                init_data["x_grid"] = grid_type if enabled else "off"

        # Vertical axis (Y-axis)
        init_data["custom_range_y"] = CustomRange.deserialize(
            visualize.get("custom-range")
        )
        init_data["custom_ticks_y"] = CustomTicks.deserialize(
            visualize.get("custom-ticks", "")
        )
        if "y-grid-format" in visualize:
            init_data["y_grid_format"] = visualize["y-grid-format"]
        if "grid-lines" in visualize:
            init_data["y_grid"] = visualize["grid-lines"]

        # Parse yAxisLabels
        if "yAxisLabels" in visualize:
            y_axis_labels = visualize["yAxisLabels"]
            if isinstance(y_axis_labels, dict):
                enabled = y_axis_labels.get("enabled", True)
                placement = y_axis_labels.get("placement", "outside")
                init_data["y_grid_labels"] = placement if enabled else "off"
                if "alignment" in y_axis_labels:
                    init_data["y_grid_label_align"] = y_axis_labels["alignment"]

        # Appearance
        if "base-color" in visualize:
            init_data["base_color"] = visualize["base-color"]

        # Parse negativeColor
        if "negativeColor" in visualize:
            init_data["negative_color"] = NegativeColor.deserialize(
                visualize["negativeColor"]
            )

        # Parse color-category using utility
        init_data.update(ColorCategory.deserialize(visualize.get("color-category")))

        if "bar-padding" in visualize:
            init_data["bar_padding"] = visualize["bar-padding"]

        # Plot height
        init_data.update(PlotHeight.deserialize(visualize))

        # Labels
        if "show-color-key" in visualize:
            init_data["show_color_key"] = visualize["show-color-key"]

        # Parse valueLabels using utility
        init_data.update(ValueLabels.deserialize(visualize, chart_type="column"))

        # Annotations
        init_data["text_annotations"] = TextAnnotation.deserialize_model(
            visualize.get("text-annotations")
        )
        init_data["range_annotations"] = RangeAnnotation.deserialize_model(
            visualize.get("range-annotations")
        )

        return init_data

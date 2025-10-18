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
    LineInterpolation,
    NumberFormat,
    PlotHeightMode,
)
from .serializers import (
    ColorCategory,
    CustomRange,
    CustomTicks,
    ModelListSerializer,
    PlotHeight,
)


class AreaChart(BaseChart):
    """A base class for the Datawrapper API's area chart."""

    model_config = ConfigDict(
        populate_by_name=True,
        strict=True,
        validate_assignment=True,
        validate_default=True,
        use_enum_values=True,
        json_schema_extra={
            "examples": [
                {
                    "chart-type": "d3-area",
                    "title": "Population Growth Over Time",
                    "source_name": "Census Bureau",
                    "data": pd.DataFrame(
                        {
                            "year": ["2020", "2021", "2022"],
                            "Region A": [100, 120, 140],
                            "Region B": [80, 90, 100],
                        }
                    ),
                    "stack_areas": True,
                    "area_opacity": 0.8,
                }
            ]
        },
    )

    #: The type of datawrapper chart to create
    chart_type: Literal["d3-area"] = Field(
        default="d3-area",
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
        description="Whether to show the x grid. The 'on' setting shows lines.",
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

    #: Whether to show the y grid
    y_grid: GridDisplay | str = Field(
        default="on",
        alias="y-grid",
        description="Whether to show the y grid. The 'on' setting shows lines.",
    )

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

    #
    # Customize areas
    #

    #: The base color for layers (palette index or hex string)
    base_color: str | int = Field(
        default=0,
        alias="base-color",
        description="The base color for layers (palette index or hex string)",
    )

    #: The opacity of the areas
    area_opacity: float = Field(
        default=0.8,
        alias="area-opacity",
        description="The opacity of the areas",
    )

    #: The interpolation method to use when drawing lines
    interpolation: LineInterpolation | str = Field(
        default="linear",
        description="The interpolation method to use when drawing lines",
    )

    #: How to sort area layers
    sort_areas: Literal["keep", "asc", "desc"] = Field(
        default="keep",
        alias="sort-areas",
        description="How to sort area layers",
    )

    #: Whether or not to stack areas
    stack_areas: bool = Field(
        default=False,
        alias="stack-areas",
        description="Whether or not to stack areas",
    )

    #: Whether or not to stack areas to 100%
    stack_to_100: bool = Field(
        default=False,
        alias="stack-to-100",
        description="Whether or not to stack areas to 100%",
    )

    #: Whether or not to show separator lines between areas
    area_separator_lines: bool = Field(
        default=False,
        alias="area-separator-lines",
        description="Whether or not to show separator lines between areas",
    )

    #: The color of the separator lines between areas
    area_separator_color: str | int = Field(
        default="#4682b4",
        alias="area-separator-color",
        description="The color of the separator lines between areas",
    )

    #: A mapping of layer names to colors
    color_category: dict[str, str] = Field(
        default_factory=dict,
        alias="color-category",
        description="A mapping of layer names to colors",
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
                "x-grid": self.x_grid,
                # Vertical axis
                "custom-range-y": CustomRange.serialize(self.custom_range_y),
                "custom-ticks-y": CustomTicks.serialize(self.custom_ticks_y),
                "y-grid-format": self.y_grid_format,
                "y-grid": self.y_grid,
                "y-grid-labels": self.y_grid_labels,
                "y-grid-label-align": self.y_grid_label_align,
                # Customize areas
                "area-opacity": self.area_opacity,
                "base-color": self.base_color,
                "interpolation": self.interpolation,
                "sort-areas": self.sort_areas,
                "stack-areas": self.stack_areas,
                "stack-to-100": self.stack_to_100,
                "area-separator-lines": self.area_separator_lines,
                "area-separator-color": self.area_separator_color,
                # Customize specific layers
                "color-category": ColorCategory.serialize(self.color_category),
                # Labels
                "show-color-key": self.show_color_key,
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
        """Parse Datawrapper API response including area chart specific fields.

        Args:
            api_response: The JSON response from the chart metadata endpoint

        Returns:
            Dictionary that can be used to initialize the AreaChart model
        """
        # Call parent to get base fields
        init_data = super().deserialize_model(api_response)

        # Extract area-specific sections
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
        if "x-grid" in visualize:
            init_data["x_grid"] = visualize["x-grid"]

        # Vertical axis (Y-axis)
        init_data["custom_range_y"] = CustomRange.deserialize(
            visualize.get("custom-range-y")
        )
        init_data["custom_ticks_y"] = CustomTicks.deserialize(
            visualize.get("custom-ticks-y", "")
        )

        if "y-grid-format" in visualize:
            init_data["y_grid_format"] = visualize["y-grid-format"]
        if "y-grid" in visualize:
            init_data["y_grid"] = visualize["y-grid"]
        if "y-grid-labels" in visualize:
            init_data["y_grid_labels"] = visualize["y-grid-labels"]
        if "y-grid-label-align" in visualize:
            init_data["y_grid_label_align"] = visualize["y-grid-label-align"]

        # Customize areas
        if "base-color" in visualize:
            init_data["base_color"] = visualize["base-color"]

        # Parse area_opacity (may come as string or float)
        if "area-opacity" in visualize:
            area_opacity_val = visualize["area-opacity"]
            init_data["area_opacity"] = (
                float(area_opacity_val) if area_opacity_val else 0.8
            )

        if "interpolation" in visualize:
            init_data["interpolation"] = visualize["interpolation"]
        if "sort-areas" in visualize:
            init_data["sort_areas"] = visualize["sort-areas"]
        if "stack-areas" in visualize:
            init_data["stack_areas"] = visualize["stack-areas"]
        if "stack-to-100" in visualize:
            init_data["stack_to_100"] = visualize["stack-to-100"]
        if "area-separator-lines" in visualize:
            init_data["area_separator_lines"] = visualize["area-separator-lines"]
        if "area-separator-color" in visualize:
            init_data["area_separator_color"] = visualize["area-separator-color"]

        # Parse color-category using utility
        color_data = ColorCategory.deserialize(visualize.get("color-category"))
        init_data["color_category"] = color_data["color_category"]

        # Labels
        if "show-color-key" in visualize:
            init_data["show_color_key"] = visualize["show-color-key"]

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
        init_data["text_annotations"] = TextAnnotation.deserialize_model(
            visualize.get("text-annotations")
        )
        init_data["range_annotations"] = RangeAnnotation.deserialize_model(
            visualize.get("range-annotations")
        )

        return init_data

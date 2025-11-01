from typing import Any, Literal

import pandas as pd
from pydantic import ConfigDict, Field, field_validator, model_serializer

from .base import BaseChart
from .enums import (
    DateFormat,
    GridLabelAlign,
    GridLabelPosition,
    NumberFormat,
    PlotHeightMode,
    ValueLabelDisplay,
    ValueLabelPlacement,
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
    NegativeColor,
    PlotHeight,
    ValueLabels,
)


class ColumnChart(
    AnnotationsMixin,
    GridDisplayMixin,
    GridFormatMixin,
    CustomRangeMixin,
    CustomTicksMixin,
    BaseChart,
):
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
    # Vertical axis (Y-axis) - chart-specific fields
    #

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

    #: A list of columns to exclude from the color key
    exclude_from_color_key: list[str] = Field(
        default_factory=list,
        alias="exclude-from-color-key",
        description="A list of columns to exclude from the color key",
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

    @field_validator("plot_height_mode")
    @classmethod
    def validate_plot_height_mode(cls, v: PlotHeightMode | str) -> PlotHeightMode | str:
        """Validate that plot_height_mode is a valid PlotHeightMode value."""
        if isinstance(v, str):
            valid_values = [e.value for e in PlotHeightMode]
            if v not in valid_values:
                raise ValueError(f"Invalid value: {v}. Must be one of {valid_values}")
        return v

    @classmethod
    def _deserialize_grid_config(cls, visualize: dict) -> dict:
        """Override to handle ColumnChart-specific grid fields.

        ColumnChart uses different API fields than other charts:
        - x_grid: Parsed from 'grid-lines-x' dict (not 'x-grid' string)
        - y_grid: Parsed from 'grid-lines' boolean (not 'y-grid' string)
        """
        result = {}

        # Parse grid-lines-x (dict with type/enabled)
        if "grid-lines-x" in visualize:
            grid_lines_x = visualize["grid-lines-x"]
            if isinstance(grid_lines_x, dict):
                enabled = grid_lines_x.get("enabled", False)
                grid_type = grid_lines_x.get("type", "")
                result["x_grid"] = grid_type if enabled else "off"

        # Parse grid-lines (boolean)
        if "grid-lines" in visualize:
            result["y_grid"] = visualize["grid-lines"]

        return result

    def _serialize_grid_config(self) -> dict:
        """Override to add ColumnChart-specific grid-lines field.

        ColumnChart uses both the standard y-grid field (from mixin) and an
        additional grid-lines boolean field that mirrors the y-grid on/off state.
        """
        # Get the standard grid config from the mixin
        result = super()._serialize_grid_config()

        # Add the ColumnChart-specific grid-lines boolean field
        # This mirrors the y_grid on/off state
        if self.y_grid is not None:
            from .enums import GridDisplay

            # Convert to boolean: "on" or True -> True, "off" or False -> False
            if isinstance(self.y_grid, GridDisplay):
                result["grid-lines"] = self.y_grid == GridDisplay.ON
            elif isinstance(self.y_grid, bool):
                result["grid-lines"] = self.y_grid
            elif isinstance(self.y_grid, str):
                result["grid-lines"] = self.y_grid.lower() == "on"

        return result

    def _serialize_custom_range(self) -> dict:
        """Override to handle ColumnChart-specific field naming.

        ColumnChart uses 'custom-range' (not 'custom-range-y') for Y-axis custom range.
        """
        # Get the standard custom range config from the mixin
        result = super()._serialize_custom_range()

        # Rename custom-range-y to custom-range for ColumnChart
        if "custom-range-y" in result:
            result["custom-range"] = result.pop("custom-range-y")

        return result

    @classmethod
    def _deserialize_custom_range(cls, visualize: dict) -> dict:
        """Override to handle ColumnChart-specific field naming.

        ColumnChart uses 'custom-range' (not 'custom-range-y') for Y-axis custom range.
        """
        # Create a modified visualize dict with renamed field
        modified_visualize = visualize.copy()
        if "custom-range" in modified_visualize:
            modified_visualize["custom-range-y"] = modified_visualize.pop(
                "custom-range"
            )

        # Call the parent deserializer with the modified dict
        return super()._deserialize_custom_range(modified_visualize)

    def _serialize_custom_ticks(self) -> dict:
        """Override to handle ColumnChart-specific field naming.

        ColumnChart uses 'custom-ticks' (not 'custom-ticks-y') for Y-axis custom ticks.
        """
        # Get the standard custom ticks config from the mixin
        result = super()._serialize_custom_ticks()

        # Rename custom-ticks-y to custom-ticks for ColumnChart
        if "custom-ticks-y" in result:
            result["custom-ticks"] = result.pop("custom-ticks-y")

        return result

    @classmethod
    def _deserialize_custom_ticks(cls, visualize: dict) -> dict:
        """Override to handle ColumnChart-specific field naming.

        ColumnChart uses 'custom-ticks' (not 'custom-ticks-y') for Y-axis custom ticks.
        """
        # Create a modified visualize dict with renamed field
        modified_visualize = visualize.copy()
        if "custom-ticks" in modified_visualize:
            modified_visualize["custom-ticks-y"] = modified_visualize.pop(
                "custom-ticks"
            )

        # Call the parent deserializer with the modified dict
        return super()._deserialize_custom_ticks(modified_visualize)

    @model_serializer
    def serialize_model(self) -> dict:
        """Serialize the model to a dictionary."""
        # Call the parent class's serialize_model method
        model = super().serialize_model()

        # Add chart specific properties
        visualize_data = {
            # Horizontal and vertical axis (from mixins)
            **self._serialize_grid_config(),
            **self._serialize_grid_format(),
            **self._serialize_custom_range(),
            **self._serialize_custom_ticks(),
            # Vertical axis (chart-specific)
            "yAxisLabels": {
                "enabled": self.y_grid_labels != "off",
                "alignment": self.y_grid_label_align,
                "placement": "" if self.y_grid_labels == "off" else self.y_grid_labels,
            },
            # Appearance
            "base-color": self.base_color,
            "negativeColor": NegativeColor.serialize(self.negative_color),
            "bar-padding": self.bar_padding,
            "color-category": ColorCategory.serialize(
                self.color_category,
                self.category_labels,
                self.category_order,
                self.exclude_from_color_key,
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
        }

        model["metadata"]["visualize"].update(visualize_data)
        model["metadata"]["visualize"].update(self._serialize_annotations())

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

        # Horizontal and vertical axis (from mixins)
        init_data.update(cls._deserialize_grid_config(visualize))
        init_data.update(cls._deserialize_grid_format(visualize))
        init_data.update(cls._deserialize_custom_range(visualize))
        init_data.update(cls._deserialize_custom_ticks(visualize))

        # Vertical axis (chart-specific) - Parse yAxisLabels
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
        init_data.update(cls._deserialize_annotations(visualize))

        return init_data

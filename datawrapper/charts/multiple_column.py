from typing import Any, Literal

import pandas as pd
from pydantic import ConfigDict, Field, model_serializer

from .annos import RangeAnnotation, TextAnnotation
from .base import BaseChart


class MultipleColumnChart(BaseChart):
    """A base class for the Datawrapper API's multiple column chart."""

    model_config = ConfigDict(
        populate_by_name=True,
        strict=True,
        json_schema_extra={
            "examples": [
                {
                    "chart-type": "multiple-columns",
                    "title": "Regional Sales Comparison",
                    "data": pd.DataFrame(
                        {
                            "Year": [2020, 2021, 2022, 2023],
                            "North": [100, 110, 120, 130],
                            "South": [90, 95, 100, 105],
                            "East": [80, 85, 90, 95],
                        }
                    ),
                    "grid_column": 3,
                    "grid_row_height": 140,
                }
            ]
        },
    )

    #: The type of datawrapper chart to create
    chart_type: Literal["multiple-columns"] = Field(
        default="multiple-columns",
        alias="chart-type",
        description="The type of datawrapper chart to create",
    )

    #: Panels configuration
    panels: list[dict[str, Any]] = Field(
        default_factory=list,
        description="Panel configurations for the chart",
    )

    #
    # Layout
    #

    #: Fixed vs auto layout. If minimumWidth is selected it's auto layout
    grid_layout: Literal["fixedCount", "minimumWidth"] = Field(
        default="fixedCount",
        alias="grid-layout",
        description="Fixed vs auto layout",
    )

    #: How the panels are laid out on desktop
    grid_column: int = Field(
        default=2,
        alias="grid-column",
        description="How the panels are laid out on desktop",
    )

    #: How the panels are laid out on mobile
    grid_column_mobile: int = Field(
        default=2,
        alias="grid-column-mobile",
        description="How the panels are laid out on mobile",
    )

    #: How the panels are laid out - only changed if layout is not fixedCount
    grid_column_width: int = Field(
        default=200,
        alias="grid-column-width",
        description="Minimum width for auto layout",
    )

    #: Height of rows
    grid_row_height: int = Field(
        default=140,
        alias="grid-row-height",
        description="Height of rows",
    )

    #: Sort of the panels
    sort: bool = Field(
        default=False,
        description="Whether to sort the panels",
    )

    #: Whether to sort the panels in reverse order
    sort_reverse: bool = Field(
        default=False,
        alias="sort-reverse",
        description="Whether to sort the panels in reverse order",
    )

    #: How to sort the panels
    sort_by: Literal["start", "end", "range", "diff", "change", "title"] = Field(
        default="end",
        alias="sort-by",
        description="How to sort the panels",
    )

    #
    # Horizontal axis
    #

    #: The custom range for the x axis
    custom_range_x: tuple[Any, Any] | list[Any] = Field(
        default=("", ""),
        alias="custom-range-x",
        description="The custom range for the x axis",
    )

    #: The custom ticks for the x axis
    custom_ticks_x: list[Any] = Field(
        default_factory=list,
        alias="custom-ticks-x",
        description="The custom ticks for the x axis",
    )

    #: The formatting for the x grid labels
    x_grid_format: str = Field(
        default="auto",
        alias="x-grid-format",
        description="The formatting for the x grid labels",
    )

    #: Whether to show the x grid
    x_grid: Literal["off", "ticks", "lines"] = Field(
        default="off",
        alias="x-grid",
        description="Whether to show the x grid",
    )

    #: The labeling of the x axis
    x_grid_labels: Literal["on", "off"] = Field(
        default="on",
        alias="x-grid-labels",
        description="The labeling of the x axis",
    )

    #: x_grid for panels
    x_grid_all: Literal["off", "on", "ticks"] = Field(
        default="off",
        alias="x-grid-all",
        description="x_grid for panels",
    )

    #
    # Vertical axis
    #

    #: The custom range for the y axis
    custom_range_y: tuple[Any, Any] | list[Any] = Field(
        default=("", ""),
        alias="custom-range-y",
        description="The custom range for the y axis",
    )

    #: The custom ticks for the y axis
    custom_ticks_y: list[Any] = Field(
        default_factory=list,
        alias="custom-ticks-y",
        description="The custom ticks for the y axis",
    )

    #: The formatting for the y grid labels
    y_grid_format: str = Field(
        default="",
        alias="y-grid-format",
        description="The formatting for the y grid labels",
    )

    #: Whether to show the y grid lines
    y_grid: bool = Field(
        default=True,
        alias="y-grid",
        description="Whether to show the y grid lines",
    )

    #: The labeling of the y grid labels
    y_grid_labels: Literal["inside", "outside", "off"] = Field(
        default="outside",
        alias="y-grid-labels",
        description="The labeling of the y grid labels",
    )

    #: Which side to put the y-axis labels on
    y_grid_label_align: Literal["left", "right"] = Field(
        default="left",
        alias="y-grid-label-align",
        description="Which side to put the y-axis labels on",
    )

    #
    # Appearance
    #

    #: The base color for the chart
    base_color: str = Field(
        default="#3182bd",
        alias="base-color",
        description="The base color for the chart",
    )

    #: The negative color to use, if you want one
    negative_color: str | None = Field(
        default="#de2d26",
        alias="negative-color",
        description="The negative color to use, if you want one",
    )

    #: A mapping of layer names to colors
    color_category: dict[str, str] = Field(
        default_factory=dict,
        alias="color-category",
        description="A mapping of layer names to colors",
    )

    #: The padding between bars as a percentage of the bar width
    bar_padding: int = Field(
        default=30,
        alias="bar-padding",
        description="The padding between bars as a percentage of the bar width",
    )

    #: How to set the plot height
    plot_height_mode: Literal["ratio", "fixed"] = Field(
        default="fixed",
        alias="plot-height-mode",
        description="How to set the plot height",
    )

    #: The fixed height of the plot
    plot_height_fixed: int = Field(
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

    #: Whether or not to column labels the same as the column
    label_colors: bool = Field(
        default=False,
        alias="label-colors",
        description="Whether or not to column labels the same as the column",
    )

    #: Whether or not to show the color key above the chart
    show_color_key: bool = Field(
        default=False,
        alias="show-color-key",
        description="Whether or not to show the color key above the chart",
    )

    #: How to format the value labels
    value_labels_format: str = Field(
        default="",
        alias="value-labels-format",
        description="How to format the value labels. Customization options can be found at https://academy.datawrapper.de/article/207-custom-number-formats-that-you-can-display-in-datawrapper",
    )

    #: Whether or not to show value labels
    value_labels: Literal["hover", "always", "off"] = Field(
        default="hover",
        alias="value-labels",
        description="Whether or not to show value labels",
    )

    #: Where to place the value labels
    value_labels_placement: Literal["inside", "outside", "below"] = Field(
        default="outside",
        alias="value-labels-placement",
        description="Where to place the value labels",
    )

    #: Whether or not to permanently show the value labels
    value_labels_always: bool = Field(
        default=False,
        alias="value-labels-always",
        description="Whether or not to permanently show the value labels",
    )

    #: The amount of margin to leave for the right hand side for labels
    label_margin: int = Field(
        default=0,
        alias="label-margin",
        description="The amount of margin to leave for the right hand side for labels. Zero is automatically calculated.",
    )

    #: Show label for all panels
    x_grid_label_all: bool = Field(
        default=False,
        alias="x-grid-label-all",
        description="Show label for all panels",
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

    @model_serializer
    def serialize_model(self) -> dict:
        """Serialize the model to a dictionary."""
        # Call the parent class's serialize_model method
        model = super().serialize_model()

        # Add chart specific properties to visualize section
        model["metadata"]["visualize"].update(
            {
                # Layout
                "gridLayout": self.grid_layout,
                "gridColumnCount": self.grid_column,
                "gridColumnCountMobile": self.grid_column_mobile,
                "gridColumnMinWidth": self.grid_column_width,
                "gridRowHeightFixed": self.grid_row_height,
                "sort": {
                    "enabled": self.sort,
                    "reverse": self.sort_reverse,
                    "by": self.sort_by,
                },
                # Horizontal axis
                "custom-range-x": self.custom_range_x,
                "custom-ticks-x": ",".join(str(tick) for tick in self.custom_ticks_x),
                "x-grid-format": self.x_grid_format,
                "x-grid-labels": self.x_grid_labels,
                "x-grid": self.x_grid_all,
                "grid-lines-x": {
                    "type": "" if self.x_grid == "off" else self.x_grid,
                    "enabled": self.x_grid != "off",
                },
                # Vertical axis
                "custom-range-y": self.custom_range_y,
                "custom-ticks-y": ",".join(str(tick) for tick in self.custom_ticks_y),
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
                "negativeColor": {
                    "value": self.negative_color,
                    "enabled": self.negative_color is not None,
                },
                "bar-padding": self.bar_padding,
                "color-category": {"map": self.color_category},
                "color-by-column": bool(self.color_category),
                "plotHeightMode": self.plot_height_mode,
                "plotHeightFixed": self.plot_height_fixed,
                "plotHeightRatio": self.plot_height_ratio,
                "panels": {panel["column"]: panel for panel in self.panels},
                # Labels
                "show-color-key": self.show_color_key,
                "label-colors": self.label_colors,
                "label-margin": self.label_margin,
                "valueLabels": {
                    "show": "" if self.value_labels == "off" else self.value_labels,
                    "format": self.value_labels_format,
                    "enabled": self.value_labels_always,
                    "placement": self.value_labels_placement,
                },
                "xGridLabelAllColumns": self.x_grid_label_all,
                # Annotations
                "text-annotations": self._serialize_annotations(
                    self.text_annotations, TextAnnotation
                ),
                "range-annotations": self._serialize_annotations(
                    self.range_annotations, RangeAnnotation
                ),
            }
        )

        # Return the serialized data
        return model

    @classmethod
    def deserialize_model(cls, api_response: dict[str, Any]) -> dict[str, Any]:
        """Parse Datawrapper API response including multiple column chart specific fields.

        Args:
            api_response: The JSON response from the chart metadata endpoint
            chart_data: The CSV data from the chart data endpoint

        Returns:
            Dictionary that can be used to initialize the MultipleColumnChart model
        """
        # Call parent to get base fields
        init_data = super().deserialize_model(api_response)

        # Extract multiple-column-specific sections
        metadata = api_response.get("metadata", {})
        visualize = metadata.get("visualize", {})

        # Layout
        init_data["grid_layout"] = visualize.get("gridLayout", "fixedCount")
        init_data["grid_column"] = visualize.get("gridColumnCount", 2)
        init_data["grid_column_mobile"] = visualize.get("gridColumnCountMobile", 2)
        init_data["grid_column_width"] = visualize.get("gridColumnMinWidth", 200)
        init_data["grid_row_height"] = visualize.get("gridRowHeightFixed", 140)

        # Parse sort object
        sort_obj = visualize.get("sort", {})
        if isinstance(sort_obj, dict):
            init_data["sort"] = sort_obj.get("enabled", False)
            init_data["sort_reverse"] = sort_obj.get("reverse", False)
            init_data["sort_by"] = sort_obj.get("by", "end")
        else:
            init_data["sort"] = False
            init_data["sort_reverse"] = False
            init_data["sort_by"] = "end"

        # Horizontal axis
        init_data["custom_range_x"] = visualize.get("custom-range-x", ["", ""])

        # Parse custom-ticks-x (comma-separated string to list)
        custom_ticks_x_str = visualize.get("custom-ticks-x", "")
        if custom_ticks_x_str:
            ticks = []
            for tick in custom_ticks_x_str.split(","):
                tick = tick.strip()
                if tick:
                    # Try to convert to number, keep as string if it fails
                    try:
                        ticks.append(
                            int(tick)
                            if tick.isdigit()
                            or (tick.startswith("-") and tick[1:].isdigit())
                            else float(tick)
                        )
                    except ValueError:
                        ticks.append(tick)
            init_data["custom_ticks_x"] = ticks
        else:
            init_data["custom_ticks_x"] = []

        init_data["x_grid_format"] = visualize.get("x-grid-format", "auto")
        init_data["x_grid_labels"] = visualize.get("x-grid-labels", "on")
        init_data["x_grid_all"] = visualize.get("x-grid", "off")

        # Parse grid-lines-x
        grid_lines_x = visualize.get("grid-lines-x", {})
        if isinstance(grid_lines_x, dict):
            if grid_lines_x.get("enabled", False):
                init_data["x_grid"] = grid_lines_x.get("type", "ticks")
            else:
                init_data["x_grid"] = "off"
        else:
            init_data["x_grid"] = "off"

        # Vertical axis
        init_data["custom_range_y"] = visualize.get("custom-range-y", ["", ""])

        # Parse custom-ticks-y (comma-separated string to list)
        custom_ticks_y_str = visualize.get("custom-ticks-y", "")
        if custom_ticks_y_str:
            ticks = []
            for tick in custom_ticks_y_str.split(","):
                tick = tick.strip()
                if tick:
                    # Try to convert to number, keep as string if it fails
                    try:
                        ticks.append(
                            int(tick)
                            if tick.isdigit()
                            or (tick.startswith("-") and tick[1:].isdigit())
                            else float(tick)
                        )
                    except ValueError:
                        ticks.append(tick)
            init_data["custom_ticks_y"] = ticks
        else:
            init_data["custom_ticks_y"] = []

        init_data["y_grid_format"] = visualize.get("y-grid-format", "")

        # Parse grid-lines (can be bool or string "show")
        grid_lines_val = visualize.get("grid-lines", True)
        if isinstance(grid_lines_val, str):
            init_data["y_grid"] = grid_lines_val == "show"
        else:
            init_data["y_grid"] = bool(grid_lines_val)

        # Parse yAxisLabels - check both yAxisLabels object and y-grid-labels field
        y_axis_labels = visualize.get("yAxisLabels", {})
        if isinstance(y_axis_labels, dict) and y_axis_labels:
            # If yAxisLabels object exists, use it
            if y_axis_labels.get("enabled", True):
                init_data["y_grid_labels"] = y_axis_labels.get("placement", "outside")
            else:
                init_data["y_grid_labels"] = "off"
            init_data["y_grid_label_align"] = y_axis_labels.get("alignment", "left")
        else:
            # Fall back to y-grid-labels field
            init_data["y_grid_labels"] = visualize.get("y-grid-labels", "outside")
            init_data["y_grid_label_align"] = visualize.get(
                "y-grid-label-align", "left"
            )

        # Appearance
        base_color_val = visualize.get("base-color", "#809cae")
        # Handle case where base-color is 0 (integer) - convert to default color
        if isinstance(base_color_val, int):
            init_data["base_color"] = "#809cae"
        else:
            init_data["base_color"] = base_color_val

        init_data["bar_padding"] = visualize.get("bar-padding", 30)

        # Parse color-category
        color_category_obj = visualize.get("color-category", {})
        if isinstance(color_category_obj, dict):
            init_data["color_category"] = color_category_obj.get("map", {})
        else:
            init_data["color_category"] = {}

        # Parse negativeColor
        negative_color_obj = visualize.get("negativeColor", {})
        if isinstance(negative_color_obj, dict):
            if negative_color_obj.get("enabled", False):
                init_data["negative_color"] = negative_color_obj.get("value", "#E31A1C")
            else:
                init_data["negative_color"] = None
        else:
            init_data["negative_color"] = "#E31A1C"

        init_data["plot_height_mode"] = visualize.get("plotHeightMode", "fixed")
        init_data["plot_height_fixed"] = visualize.get("plotHeightFixed", 300)
        init_data["plot_height_ratio"] = visualize.get("plotHeightRatio", 0.5)

        # Parse panels (dict to list)
        panels_obj = visualize.get("panels", {})
        if isinstance(panels_obj, dict):
            init_data["panels"] = [
                {"column": col, **config} for col, config in panels_obj.items()
            ]
        else:
            init_data["panels"] = []

        # Labels
        init_data["label_colors"] = visualize.get("label-colors", False)
        init_data["show_color_key"] = visualize.get("show-color-key", False)
        init_data["label_margin"] = visualize.get("label-margin", 0)
        init_data["x_grid_label_all"] = visualize.get("xGridLabelAllColumns", False)

        # Parse valueLabels
        value_labels_obj = visualize.get("valueLabels", {})
        if isinstance(value_labels_obj, dict):
            show_value = value_labels_obj.get("show", "hover")
            init_data["value_labels"] = "off" if show_value == "" else show_value
            init_data["value_labels_format"] = value_labels_obj.get("format", "")
            init_data["value_labels_always"] = value_labels_obj.get("enabled", False)
            init_data["value_labels_placement"] = value_labels_obj.get(
                "placement", "outside"
            )
        else:
            init_data["value_labels"] = "hover"
            init_data["value_labels_format"] = ""
            init_data["value_labels_always"] = False
            init_data["value_labels_placement"] = "outside"

        # Annotations - preserve UUIDs by including them in annotation data
        text_annos = visualize.get("text-annotations", {})
        if isinstance(text_annos, dict):
            init_data["text_annotations"] = (
                []
                if not text_annos
                else [
                    {**anno_data, "id": anno_id}
                    for anno_id, anno_data in text_annos.items()
                ]
            )
        else:
            init_data["text_annotations"] = text_annos if text_annos else []

        range_annos = visualize.get("range-annotations", {})
        if isinstance(range_annos, dict):
            init_data["range_annotations"] = (
                []
                if not range_annos
                else [
                    {**anno_data, "id": anno_id}
                    for anno_id, anno_data in range_annos.items()
                ]
            )
        else:
            init_data["range_annotations"] = range_annos if range_annos else []

        return init_data

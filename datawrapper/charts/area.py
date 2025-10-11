from typing import Any, Literal

import pandas as pd
from pydantic import ConfigDict, Field, model_serializer

from .annos import RangeAnnotation, TextAnnotation
from .base import BaseChart


class AreaChart(BaseChart):
    """A base class for the Datawrapper API's area chart."""

    model_config = ConfigDict(
        populate_by_name=True,
        strict=True,
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
    custom_range_x: list[Any] = Field(
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

    #: The formatting for the x grid labels
    x_grid_format: str = Field(
        default="auto",
        alias="x-grid-format",
        description="The formatting for the x grid labels",
    )

    #: Whether to show the x grid
    x_grid: Literal["off", "on", "ticks"] = Field(
        default="off",
        alias="x-grid",
        description="Whether to show the x grid. The 'on' setting shows lines.",
    )

    #
    # Vertical axis (Y-axis)
    #

    #: The custom range for the y axis
    custom_range_y: list[Any] = Field(
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

    #: The formatting for the y grid labels
    y_grid_format: str = Field(
        default="",
        alias="y-grid-format",
        description="The formatting for the y grid labels. Customization options can be found at https://academy.datawrapper.de/article/207-custom-number-formats-that-you-can-display-in-datawrapper",
    )

    #: Whether to show the y grid
    y_grid: Literal["off", "on", "ticks"] = Field(
        default="on",
        alias="y-grid",
        description="Whether to show the y grid. The 'on' setting shows lines.",
    )

    #: The labeling of the y grid labels
    y_grid_labels: Literal["auto", "inside", "outside", "off"] = Field(
        default="auto",
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
    # Customize areas
    #

    #: The base color for layers
    base_color: str | int = Field(
        default="#4682b4",
        alias="base-color",
        description="The base color for layers",
    )

    #: The opacity of the areas
    area_opacity: float = Field(
        default=0.8,
        alias="area-opacity",
        description="The opacity of the areas",
    )

    #: The interpolation method to use when drawing lines
    interpolation: Literal[
        "linear",
        "step",
        "step-after",
        "step-before",
        "monotone-x",
        "cardinal",
        "natural",
    ] = Field(
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
    area_separator_color: str = Field(
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

    #: The format for the x-axis tooltips
    tooltip_x_format: str = Field(
        default="",
        alias="tooltip-x-format",
        description="The format for the x-axis tooltips. Customization options found at https://academy.datawrapper.de/article/164-date-formats-that-datawrapper-recognizes",
    )

    #: The format of the number tooltip
    tooltip_number_format: str = Field(
        default="",
        alias="tooltip-number-format",
        description="The format of the number tooltip. Customization options found at https://academy.datawrapper.de/article/207-custom-number-formats-that-you-can-display-in-datawrapper#number-formats",
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

    @model_serializer
    def serialize_model(self) -> dict:
        """Serialize the model to a dictionary."""
        # Call the parent class's serialize_model method
        model = super().serialize_model()

        # Add chart specific properties
        model["metadata"]["visualize"].update(
            {
                # Horizontal axis
                "custom-range-x": self.custom_range_x,
                "custom-ticks-x": ",".join(str(tick) for tick in self.custom_ticks_x),
                "x-grid-format": self.x_grid_format,
                "x-grid": self.x_grid,
                # Vertical axis
                "custom-range-y": self.custom_range_y,
                "custom-ticks-y": ",".join(str(tick) for tick in self.custom_ticks_y),
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
                "color-category": {"map": self.color_category},
                # Labels
                "show-color-key": self.show_color_key,
                # Tooltips
                "show-tooltips": self.show_tooltips,
                "tooltip-x-format": self.tooltip_x_format,
                "tooltip-number-format": self.tooltip_number_format,
                # Appearance
                "plotHeightMode": self.plot_height_mode,
                "plotHeightFixed": self.plot_height_fixed,
                "plotHeightRatio": self.plot_height_ratio,
                # Initialize empty structures
                "text-annotations": {},
                "range-annotations": {},
            }
        )

        # Add text annotations
        for ta_obj in self.text_annotations:
            if isinstance(ta_obj, dict):
                ta_dict = TextAnnotation.model_validate(ta_obj).serialize_model()
            elif isinstance(ta_obj, TextAnnotation):
                ta_dict = ta_obj.serialize_model()
            else:
                raise ValueError(
                    "Text annotations must be TextAnnotation objects or dicts"
                )
            # Generate a unique ID for the annotation
            import uuid

            anno_id = str(uuid.uuid4()).replace("-", "")[:10]
            model["metadata"]["visualize"]["text-annotations"][anno_id] = ta_dict

        # Add range annotations
        for ra_obj in self.range_annotations:
            if isinstance(ra_obj, dict):
                ra_dict = RangeAnnotation.model_validate(ra_obj).serialize_model()
            elif isinstance(ra_obj, RangeAnnotation):
                ra_dict = ra_obj.serialize_model()
            else:
                raise ValueError(
                    "Range annotations must be RangeAnnotation objects or dicts"
                )
            # Generate a unique ID for the annotation
            import uuid

            anno_id = str(uuid.uuid4()).replace("-", "")[:10]
            model["metadata"]["visualize"]["range-annotations"][anno_id] = ra_dict

        # Return the serialized data
        return model

    @classmethod
    def _from_api(
        cls, chart_metadata: dict[str, Any], chart_data: str
    ) -> dict[str, Any]:
        """Parse Datawrapper API response including area chart specific fields.

        Args:
            chart_metadata: The JSON response from the chart metadata endpoint
            chart_data: The CSV data from the chart data endpoint

        Returns:
            Dictionary that can be used to initialize the AreaChart model
        """
        # Call parent to get base fields
        init_data = super()._from_api(chart_metadata, chart_data)

        # Extract area-specific sections
        metadata = chart_metadata.get("metadata", {})
        visualize = metadata.get("visualize", {})

        # Horizontal axis (X-axis)
        init_data["custom_range_x"] = visualize.get("custom-range-x", ["", ""])

        # Parse custom ticks X (comes as comma-separated string)
        ticks_x_str = visualize.get("custom-ticks-x", "")
        if ticks_x_str:
            init_data["custom_ticks_x"] = [
                float(x.strip()) if x.strip() else x.strip()
                for x in ticks_x_str.split(",")
            ]
        else:
            init_data["custom_ticks_x"] = []

        init_data["x_grid_format"] = visualize.get("x-grid-format", "auto")
        init_data["x_grid"] = visualize.get("x-grid", "off")

        # Vertical axis (Y-axis)
        init_data["custom_range_y"] = visualize.get("custom-range-y", ["", ""])

        # Parse custom ticks Y (comes as comma-separated string)
        ticks_y_str = visualize.get("custom-ticks-y", "")
        if ticks_y_str:
            init_data["custom_ticks_y"] = [
                float(x.strip()) if x.strip() else x.strip()
                for x in ticks_y_str.split(",")
            ]
        else:
            init_data["custom_ticks_y"] = []

        init_data["y_grid_format"] = visualize.get("y-grid-format", "")
        init_data["y_grid"] = visualize.get("y-grid", "on")
        init_data["y_grid_labels"] = visualize.get("y-grid-labels", "auto")
        init_data["y_grid_label_align"] = visualize.get("y-grid-label-align", "left")

        # Customize areas
        init_data["base_color"] = visualize.get("base-color", "#4682b4")

        # Parse area_opacity (may come as string or float)
        area_opacity_val = visualize.get("area-opacity", 0.8)
        init_data["area_opacity"] = float(area_opacity_val) if area_opacity_val else 0.8

        init_data["interpolation"] = visualize.get("interpolation", "linear")
        init_data["sort_areas"] = visualize.get("sort-areas", "keep")
        init_data["stack_areas"] = visualize.get("stack-areas", False)
        init_data["stack_to_100"] = visualize.get("stack-to-100", False)
        init_data["area_separator_lines"] = visualize.get("area-separator-lines", False)
        init_data["area_separator_color"] = visualize.get(
            "area-separator-color", "#4682b4"
        )

        # Parse color-category
        color_category_obj = visualize.get("color-category", {})
        if isinstance(color_category_obj, dict):
            init_data["color_category"] = color_category_obj.get("map", {})
        else:
            init_data["color_category"] = {}

        # Labels
        init_data["show_color_key"] = visualize.get("show-color-key", False)

        # Tooltips
        init_data["show_tooltips"] = visualize.get("show-tooltips", True)
        init_data["tooltip_x_format"] = visualize.get("tooltip-x-format", "")
        init_data["tooltip_number_format"] = visualize.get("tooltip-number-format", "")

        # Appearance
        init_data["plot_height_mode"] = visualize.get("plotHeightMode", "fixed")
        init_data["plot_height_fixed"] = visualize.get("plotHeightFixed", 300)
        init_data["plot_height_ratio"] = visualize.get("plotHeightRatio", 0.5)

        # Annotations - handle empty dicts → empty lists
        text_annos = visualize.get("text-annotations", {})
        init_data["text_annotations"] = (
            []
            if isinstance(text_annos, dict) and not text_annos
            else list(text_annos.values())
            if isinstance(text_annos, dict)
            else text_annos
        )

        range_annos = visualize.get("range-annotations", {})
        init_data["range_annotations"] = (
            []
            if isinstance(range_annos, dict) and not range_annos
            else list(range_annos.values())
            if isinstance(range_annos, dict)
            else range_annos
        )

        return init_data

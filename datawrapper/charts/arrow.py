from typing import Any, Literal

import pandas as pd
from pydantic import ConfigDict, Field, model_serializer

from .base import BaseChart
from .serializers import ColorCategory, CustomRange, ReplaceFlags


class ArrowChart(BaseChart):
    """A base class for the Datawrapper API's arrow chart."""

    model_config = ConfigDict(
        populate_by_name=True,
        strict=True,
        json_schema_extra={
            "examples": [
                {
                    "chart-type": "d3-arrow-plot",
                    "title": "Population Change by Region",
                    "source_name": "Census Bureau",
                    "data": pd.DataFrame(
                        {
                            "Region": ["North", "South", "East", "West"],
                            "2020": [100, 150, 120, 90],
                            "2023": [110, 160, 115, 95],
                        }
                    ),
                    "axis_start": "2020",
                    "axis_end": "2023",
                    "thick_arrows": True,
                }
            ]
        },
    )

    #: The type of datawrapper chart to create
    chart_type: Literal["d3-arrow-plot"] = Field(
        default="d3-arrow-plot",
        alias="chart-type",
        description="The type of datawrapper chart to create",
    )

    #
    # Customize arrows
    #

    #: A mapping of layer names to colors
    color_category: dict[str, str] = Field(
        default_factory=dict,
        alias="color-category",
        description="A mapping of layer names to colors",
    )

    #: Thicken the arrows
    thick_arrows: bool = Field(
        default=True,
        alias="thick-arrows",
        description="Thicken the arrows",
    )

    #: Show the y-axis grid lines
    y_grid: str = Field(
        default="on",
        alias="y-grid",
        description="Show the y-axis grid lines",
    )

    #: Whether to replace country codes with flags
    replace_flags: Literal["off", "4x3", "1x1", "circle"] = Field(
        default="off",
        alias="replace-flags",
        description="Whether to replace country codes with flags",
    )

    #
    # Sorting & ordering
    #

    #: Whether to sort the ranges
    sort_ranges: bool = Field(
        default=False,
        alias="sort-ranges",
        description="Whether to sort the ranges",
    )

    #: How to sort the ranges
    sort_by: Literal["end", "start", "difference", "change"] = Field(
        default="end",
        alias="sort-by",
        description="How to sort the ranges",
    )

    #: Reverse the order of the ranges
    reverse_order: bool = Field(
        default=False,
        alias="reverse-order",
        description="Reverse the order of the ranges",
    )

    #
    # Labels & formatting
    #

    #: The number format for value labels
    value_label_format: str = Field(
        default="",
        alias="value-label-format",
        description="The number format for value labels. Customization options can be found at https://academy.datawrapper.de/article/207-custom-number-formats-that-you-can-display-in-datawrapper",
    )

    #: The field you want to use for the value labels
    range_value_labels: str = Field(
        default="",
        alias="range-value-labels",
        description="The field you want to use for the value labels",
    )

    #
    # Axes
    #

    #: The custom range for the x axis
    custom_range: list[Any] | tuple[Any, Any] = Field(
        default_factory=lambda: ["", ""],
        alias="custom-range",
        description="The custom range for the x axis",
    )

    #: The type of range on the x-axis
    range_extent: Literal["nice", "custom", "data"] = Field(
        default="nice",
        alias="range-extent",
        description="The type of range on the x-axis",
    )

    #: The column that arrows should start at
    axis_start: str = Field(
        default="",
        alias="axis-start",
        description="The column that arrows should start at",
    )

    #: The column that arrows should end at
    axis_end: str = Field(
        default="",
        alias="axis-end",
        description="The column that arrows should end at",
    )

    #
    # Features
    #

    #: Enables the color-by-column feature
    color_by_column: bool = Field(
        default=False,
        alias="color-by-column",
        description="Enables the color-by-column feature",
    )

    #: Label on the first arrow that shows column names
    arrow_key: bool = Field(
        default=False,
        alias="arrow-key",
        description="Label on the first arrow that shows column names",
    )

    #: Enables the group-by-column feature, works with "Group" field
    group_by_column: bool = Field(
        default=False,
        alias="group-by-column",
        description="Enables the group-by-column feature, works with 'Group' field",
    )

    @model_serializer
    def serialize_model(self) -> dict:
        """Serialize the model to a dictionary."""
        # Call the parent class's serialize_model method
        model = super().serialize_model()

        # Add chart specific properties to visualize section
        model["metadata"]["visualize"].update(
            {
                "y-grid": self.y_grid,
                "reverse-order": self.reverse_order,
                "thick-arrows": self.thick_arrows,
                "color-category": ColorCategory.serialize(self.color_category),
                "range-value-labels": self.range_value_labels,
                "sort-range": {
                    "by": self.sort_by,
                    "enabled": self.sort_ranges,
                },
                "custom-range": CustomRange.serialize(self.custom_range),
                "range-extent": self.range_extent,
                "value-label-format": self.value_label_format,
                "color-by-column": self.color_by_column,
                "group-by-column": self.group_by_column,
                "replace-flags": ReplaceFlags.serialize(self.replace_flags),
                "show-arrow-key": self.arrow_key,
            }
        )

        # Add axes section (separate from visualize)
        model["metadata"]["axes"] = {
            "start": self.axis_start,
            "end": self.axis_end,
        }

        # Return the serialized data
        return model

    @classmethod
    def deserialize_model(cls, api_response: dict[str, Any]) -> dict[str, Any]:
        """Parse Datawrapper API response including arrow chart specific fields.

        Args:
            api_response: The JSON response from the chart metadata endpoint

        Returns:
            Dictionary that can be used to initialize the ArrowChart model
        """
        # Call parent to get base fields
        init_data = super().deserialize_model(api_response)

        # Extract arrow-specific sections
        metadata = api_response.get("metadata", {})
        visualize = metadata.get("visualize", {})
        axes = metadata.get("axes", {})

        # Customize arrows
        if "y-grid" in visualize:
            init_data["y_grid"] = visualize["y-grid"]
        if "reverse-order" in visualize:
            init_data["reverse_order"] = visualize["reverse-order"]
        if "thick-arrows" in visualize:
            init_data["thick_arrows"] = visualize["thick-arrows"]

        # Parse color-category using utility
        color_data = ColorCategory.deserialize(visualize.get("color-category"))
        init_data["color_category"] = color_data["color_category"]

        # Labels & formatting
        if "range-value-labels" in visualize:
            init_data["range_value_labels"] = visualize["range-value-labels"]
        if "value-label-format" in visualize:
            init_data["value_label_format"] = visualize["value-label-format"]

        # Sorting & ordering
        sort_range_obj = visualize.get("sort-range", {})
        if isinstance(sort_range_obj, dict):
            init_data["sort_by"] = sort_range_obj.get("by", "end")
            init_data["sort_ranges"] = sort_range_obj.get("enabled", False)
        else:
            init_data["sort_by"] = "end"
            init_data["sort_ranges"] = False

        # Parse replace-flags using utility
        if "replace-flags" in visualize:
            init_data["replace_flags"] = ReplaceFlags.deserialize(
                visualize["replace-flags"]
            )

        # Axes
        init_data["custom_range"] = CustomRange.deserialize(
            visualize.get("custom-range")
        )
        if "range-extent" in visualize:
            init_data["range_extent"] = visualize["range-extent"]

        # Parse axes section
        if "start" in axes:
            init_data["axis_start"] = axes["start"]
        if "end" in axes:
            init_data["axis_end"] = axes["end"]

        # Features
        if "color-by-column" in visualize:
            init_data["color_by_column"] = visualize["color-by-column"]
        if "group-by-column" in visualize:
            init_data["group_by_column"] = visualize["group-by-column"]
        if "show-arrow-key" in visualize:
            init_data["arrow_key"] = visualize["show-arrow-key"]

        return init_data

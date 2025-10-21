from typing import Any, Literal

import pandas as pd
from pydantic import ConfigDict, Field, field_validator, model_serializer

from .base import BaseChart
from .enums import DateFormat, NumberFormat, ReplaceFlagsType
from .serializers import ColorCategory, CustomRange, ReplaceFlags


class ArrowChart(BaseChart):
    """A base class for the Datawrapper API's arrow chart."""

    model_config = ConfigDict(
        populate_by_name=True,
        strict=True,
        validate_assignment=True,
        validate_default=True,
        use_enum_values=True,
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
                    "start_column": "2020",
                    "end_column": "2023",
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

    #: The base color for the arrows
    base_color: str | int = Field(
        default=0,
        alias="base-color",
        description="The base color for the arrows",
    )

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

    #: Whether to replace country codes with flags (use ReplaceFlagsType enum or raw string)
    replace_flags: ReplaceFlagsType | str = Field(
        default="off",
        alias="replace-flags",
        description="Whether to replace country codes with flags. Use ReplaceFlagsType enum for type safety or provide raw strings.",
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

    #: The number format for value labels (use DateFormat or NumberFormat enum or custom format strings)
    value_label_format: DateFormat | NumberFormat | str = Field(
        default="",
        alias="value-label-format",
        description="The number format for value labels. Use DateFormat for temporal data, NumberFormat for numeric data, or provide custom format strings.",
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
    start_column: str | None = Field(
        default=None,
        description="The column that arrows should start at",
    )

    #: The column that arrows should end at
    end_column: str | None = Field(
        default=None,
        description="The column that arrows should end at",
    )

    #: The column to color by
    color_column: str | None = Field(
        default=None,
        description="The column to color by",
    )

    #: The column to label by
    label_column: str | None = Field(
        default=None,
        description="The column to label by",
    )

    #
    # Features
    #

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

    @field_validator("replace_flags")
    @classmethod
    def validate_replace_flags(
        cls, v: ReplaceFlagsType | str
    ) -> ReplaceFlagsType | str:
        """Validate that replace_flags is a valid ReplaceFlagsType value."""
        if isinstance(v, str):
            valid_values = [e.value for e in ReplaceFlagsType]
            if v not in valid_values:
                raise ValueError(
                    f"Invalid replace_flags: {v}. Must be one of {valid_values}"
                )
        return v

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
                "base-color": self.base_color,
                "color-category": ColorCategory.serialize(self.color_category),
                "range-value-labels": self.range_value_labels,
                "sort-range": {
                    "by": self.sort_by,
                    "enabled": self.sort_ranges,
                },
                "custom-range": CustomRange.serialize(self.custom_range),
                "range-extent": self.range_extent,
                "value-label-format": self.value_label_format,
                "color-by-column": bool(self.color_category),
                "group-by-column": self.group_by_column,
                "replace-flags": ReplaceFlags.serialize(self.replace_flags),
                "show-arrow-key": self.arrow_key,
            }
        )

        # Add axes section (separate from visualize) - only include non-None fields
        axes_dict = {}
        if self.start_column is not None:
            axes_dict["start"] = self.start_column
        if self.end_column is not None:
            axes_dict["end"] = self.end_column
        if self.color_column is not None:
            axes_dict["colors"] = self.color_column
        if self.label_column is not None:
            axes_dict["labels"] = self.label_column

        # Only add axes section if there are fields to include
        if axes_dict:
            model["metadata"]["axes"] = axes_dict

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

        # Base color
        if "base-color" in visualize:
            init_data["base_color"] = visualize["base-color"]

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
            init_data["start_column"] = axes["start"]
        if "end" in axes:
            init_data["end_column"] = axes["end"]
        if "colors" in axes:
            init_data["color_column"] = axes["colors"]
        if "labels" in axes:
            init_data["label_column"] = axes["labels"]

        # Features
        if "group-by-column" in visualize:
            init_data["group_by_column"] = visualize["group-by-column"]
        if "show-arrow-key" in visualize:
            init_data["arrow_key"] = visualize["show-arrow-key"]

        return init_data

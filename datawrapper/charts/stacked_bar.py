"""Stacked bar chart implementation for Datawrapper API."""

from typing import Any, Literal

from pydantic import ConfigDict, Field, model_serializer

from .base import BaseChart


class StackedBarChart(BaseChart):
    """A Pydantic model for the Datawrapper API's stacked bar chart."""

    model_config = ConfigDict(
        populate_by_name=True,
        strict=True,
    )

    #: The type of datawrapper chart to create
    chart_type: Literal["d3-bars-stacked"] = Field(
        default="d3-bars-stacked",
        alias="chart-type",
        description="The type of datawrapper chart to create",
    )

    #: A mapping of layer names to colors
    color_category: dict[str, str] = Field(
        default_factory=dict,
        alias="color-category",
        description="A mapping of layer names to colors",
    )

    #: Whether to replace country codes with flags
    replace_flags: Literal["off", "4x3", "1x1", "circle"] = Field(
        default="off",
        alias="replace-flags",
        description="Whether to replace country codes with flags",
    )

    #: Whether to sort the ranges
    sort_ranges: bool = Field(
        default=False,
        alias="sort-ranges",
        description="Whether to sort the ranges",
    )

    #: Whether to use thick bars
    thick_bars: bool = Field(
        default=False,
        alias="thick-bars",
        description="Whether to use thick bars",
    )

    #: Reverse the order of the ranges
    reverse_order: bool = Field(
        default=False,
        alias="reverse-order",
        description="Reverse the order of the ranges",
    )

    #: The number format for value labels
    value_label_format: str = Field(
        default="",
        alias="value-label-format",
        description="The number format for value labels",
    )

    #: The date format
    date_label_format: str = Field(
        default="",
        alias="date-label-format",
        description="The date format",
    )

    #: The field you want to use for the value labels
    range_value_labels: str = Field(
        default="",
        alias="range-value-labels",
        description="The field you want to use for the value labels",
    )

    #: Enables the color-by-column feature
    color_by_column: bool = Field(
        default=False,
        alias="color-by-column",
        description="Enables the color-by-column feature",
    )

    #: Enables the group-by-column feature, works with "Group" field
    group_by_column: bool = Field(
        default=False,
        alias="group-by-column",
        description="Enables the group-by-column feature",
    )

    #: Enables the legend
    show_color_key: bool = Field(
        default=False,
        alias="show-color-key",
        description="Enables the legend",
    )

    #: How to place the over-bar labels
    value_label_mode: Literal["left", "diverging"] = Field(
        default="left",
        alias="value-label-mode",
        description="How to place the over-bar labels",
    )

    # Additional fields found in sample data

    #: Whether to display values as percentages
    stack_percentages: bool = Field(
        default=False,
        alias="stack-percentages",
        description="Whether to display values as percentages",
    )

    #: Whether to sort bars
    sort_bars: bool = Field(
        default=False,
        alias="sort-bars",
        description="Whether to sort bars",
    )

    #: Which column to sort by
    sort_by: str = Field(
        default="",
        alias="sort-by",
        description="Which column to sort by",
    )

    #: The base color (can be hex string or palette index)
    base_color: str | int = Field(
        default=0,
        alias="base-color",
        description="The base color (can be hex string or palette index)",
    )

    #: Whether to use block labels
    block_labels: bool = Field(
        default=False,
        alias="block-labels",
        description="Whether to use block labels",
    )

    #: Negative color configuration
    negative_color_enabled: bool = Field(
        default=False,
        alias="negative-color-enabled",
        description="Whether negative color is enabled",
    )

    #: The color to use for negative values
    negative_color_value: str = Field(
        default="#E31A1C",
        alias="negative-color-value",
        description="The color to use for negative values",
    )

    #: The column to use for grouping (when group_by_column is enabled)
    groups_column: str | None = Field(
        default=None,
        alias="groups-column",
        description="The column to use for grouping",
    )

    @model_serializer
    def serialize_model(self) -> dict:
        """Serialize the model to a dictionary."""
        # Call the parent class's serialize_model method
        model = super().serialize_model()

        # Add stacked bar specific properties to visualize section
        model["metadata"]["visualize"].update(
            {
                "reverse-order": self.reverse_order,
                "color-category": {"map": self.color_category},
                "range-value-labels": self.range_value_labels,
                "show-color-key": self.show_color_key,
                "value-label-format": self.value_label_format,
                "date-label-format": self.date_label_format,
                "color-by-column": self.color_by_column,
                "group-by-column": self.group_by_column,
                "thick": self.thick_bars,
                "replace-flags": {
                    "enabled": self.replace_flags != "off",
                    "type": self.replace_flags if self.replace_flags != "off" else "",
                    "style": self.replace_flags if self.replace_flags != "off" else "",
                },
                "value-label-mode": self.value_label_mode,
                "stack-percentages": self.stack_percentages,
                "sort-bars": self.sort_bars,
                "sort-by": self.sort_by,
                "base-color": self.base_color,
                "block-labels": self.block_labels,
                "negativeColor": {
                    "enabled": self.negative_color_enabled,
                    "value": self.negative_color_value,
                },
            }
        )

        # Add axes if groups_column is set
        if self.groups_column:
            model["axes"] = {"groups": self.groups_column}

        # Return the serialized data
        return model

    @classmethod
    def deserialize_model(cls, api_response: dict[str, Any]) -> dict[str, Any]:
        """Parse Datawrapper API response including stacked bar specific fields.

        Args:
            api_response: The JSON response from the chart metadata endpoint
            chart_data: The CSV data from the chart data endpoint

        Returns:
            Dictionary that can be used to initialize the StackedBarChart model
        """
        # Call parent to get base fields
        init_data = super().deserialize_model(api_response)

        # Extract stacked bar specific sections
        metadata = api_response.get("metadata", {})
        visualize = metadata.get("visualize", {})
        axes = api_response.get("axes", metadata.get("axes", {}))

        # Parse stacked bar specific fields
        init_data["reverse_order"] = visualize.get("reverse-order", False)

        # Parse color-category
        color_category = visualize.get("color-category", {})
        if isinstance(color_category, dict):
            init_data["color_category"] = color_category.get("map", {})
        else:
            init_data["color_category"] = {}

        init_data["range_value_labels"] = visualize.get("range-value-labels", "")
        init_data["show_color_key"] = visualize.get("show-color-key", False)
        init_data["value_label_format"] = visualize.get("value-label-format", "")
        init_data["date_label_format"] = visualize.get("date-label-format", "")
        init_data["color_by_column"] = visualize.get("color-by-column", False)
        init_data["group_by_column"] = visualize.get("group-by-column", False)
        init_data["thick_bars"] = visualize.get("thick", False)

        # Parse replace-flags
        replace_flags = visualize.get("replace-flags", {})
        if isinstance(replace_flags, dict):
            if replace_flags.get("enabled", False):
                init_data["replace_flags"] = replace_flags.get("style", "4x3")
            else:
                init_data["replace_flags"] = "off"
        else:
            init_data["replace_flags"] = "off"

        init_data["value_label_mode"] = visualize.get("value-label-mode", "left")
        init_data["stack_percentages"] = visualize.get("stack-percentages", False)
        init_data["sort_bars"] = visualize.get("sort-bars", False)
        init_data["sort_by"] = visualize.get("sort-by", "")
        init_data["base_color"] = visualize.get("base-color", 0)
        init_data["block_labels"] = visualize.get("block-labels", False)

        # Parse negativeColor
        negative_color = visualize.get("negativeColor", {})
        if isinstance(negative_color, dict):
            init_data["negative_color_enabled"] = negative_color.get("enabled", False)
            init_data["negative_color_value"] = negative_color.get("value", "#E31A1C")
        else:
            init_data["negative_color_enabled"] = False
            init_data["negative_color_value"] = "#E31A1C"

        # Parse groups column from axes
        if isinstance(axes, dict):
            init_data["groups_column"] = axes.get("groups")
        else:
            init_data["groups_column"] = None

        return init_data

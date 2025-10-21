"""Stacked bar chart implementation for Datawrapper API."""

from typing import Any, Literal

from pydantic import ConfigDict, Field, field_validator, model_serializer

from .base import BaseChart
from .enums import DateFormat, NumberFormat, ReplaceFlagsType, ValueLabelMode
from .serializers import ColorCategory, NegativeColor, ReplaceFlags


class StackedBarChart(BaseChart):
    """A Pydantic model for the Datawrapper API's stacked bar chart."""

    model_config = ConfigDict(
        populate_by_name=True,
        strict=True,
        validate_assignment=True,
        validate_default=True,
        use_enum_values=True,
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

    #: Whether to replace country codes with flags (use ReplaceFlagsType enum or raw string)
    replace_flags: ReplaceFlagsType | str = Field(
        default="off",
        alias="replace-flags",
        description="Whether to replace country codes with flags. Use ReplaceFlagsType enum for type safety or provide raw strings.",
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

    #: The number format for value labels (use DateFormat or NumberFormat enum or custom format strings)
    value_label_format: DateFormat | NumberFormat | str = Field(
        default="",
        alias="value-label-format",
        description="The number format for value labels. Use DateFormat for temporal data, NumberFormat for numeric data, or provide custom format strings.",
    )

    #: The date format (use DateFormat enum or custom format strings)
    date_label_format: DateFormat | str = Field(
        default="",
        alias="date-label-format",
        description="The date format. Use DateFormat enum for common formats or provide custom format strings.",
    )

    #: The field you want to use for the value labels
    range_value_labels: str = Field(
        default="",
        alias="range-value-labels",
        description="The field you want to use for the value labels",
    )

    #: Enables the legend
    show_color_key: bool = Field(
        default=False,
        alias="show-color-key",
        description="Enables the legend",
    )

    #: How to place the over-bar labels (use ValueLabelMode enum or raw string)
    value_label_mode: ValueLabelMode | str = Field(
        default="left",
        alias="value-label-mode",
        description="How to place the over-bar labels. Use ValueLabelMode enum for type safety or provide raw strings.",
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

    #: The negative color to use, if you want one
    negative_color: str | None = Field(
        default=None,
        alias="negative-color",
        description="The negative color to use, if you want one",
    )

    #: The column to use for grouping
    groups_column: str | None = Field(
        default=None,
        alias="groups-column",
        description="The column to use for grouping",
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

    @field_validator("value_label_mode")
    @classmethod
    def validate_value_label_mode(cls, v: ValueLabelMode | str) -> ValueLabelMode | str:
        """Validate that value_label_mode is a valid ValueLabelMode value."""
        if isinstance(v, str):
            valid_values = [e.value for e in ValueLabelMode]
            if v not in valid_values:
                raise ValueError(
                    f"Invalid value_label_mode: {v}. Must be one of {valid_values}"
                )
        return v

    @model_serializer
    def serialize_model(self) -> dict:
        """Serialize the model to a dictionary."""
        # Call the parent class's serialize_model method
        model = super().serialize_model()

        # Add stacked bar specific properties to visualize section
        model["metadata"]["visualize"].update(
            {
                "reverse-order": self.reverse_order,
                "color-category": ColorCategory.serialize(self.color_category),
                "range-value-labels": self.range_value_labels,
                "show-color-key": self.show_color_key,
                "value-label-format": self.value_label_format,
                "date-label-format": self.date_label_format,
                "color-by-column": bool(self.color_category),
                "group-by-column": self.groups_column is not None,
                "thick": self.thick_bars,
                "replace-flags": ReplaceFlags.serialize(self.replace_flags),
                "value-label-mode": self.value_label_mode,
                "stack-percentages": self.stack_percentages,
                "sort-bars": self.sort_bars,
                "sort-by": self.sort_by,
                "base-color": self.base_color,
                "block-labels": self.block_labels,
                "negativeColor": NegativeColor.serialize(self.negative_color),
            }
        )

        # Add axes if groups_column is set
        if self.groups_column:
            model["metadata"]["axes"] = {"groups": self.groups_column}

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
        axes = metadata.get("axes", {})

        # Parse stacked bar specific fields
        if "reverse-order" in visualize:
            init_data["reverse_order"] = visualize["reverse-order"]

        # Parse color-category using utility
        color_data = ColorCategory.deserialize(visualize.get("color-category"))
        init_data["color_category"] = color_data["color_category"]

        if "range-value-labels" in visualize:
            init_data["range_value_labels"] = visualize["range-value-labels"]
        if "show-color-key" in visualize:
            init_data["show_color_key"] = visualize["show-color-key"]
        if "value-label-format" in visualize:
            init_data["value_label_format"] = visualize["value-label-format"]
        if "date-label-format" in visualize:
            init_data["date_label_format"] = visualize["date-label-format"]
        if "thick" in visualize:
            init_data["thick_bars"] = visualize["thick"]

        # Parse replace-flags using utility
        if "replace-flags" in visualize:
            init_data["replace_flags"] = ReplaceFlags.deserialize(
                visualize["replace-flags"]
            )

        if "value-label-mode" in visualize:
            init_data["value_label_mode"] = visualize["value-label-mode"]
        if "stack-percentages" in visualize:
            init_data["stack_percentages"] = visualize["stack-percentages"]
        if "sort-bars" in visualize:
            init_data["sort_bars"] = visualize["sort-bars"]
        if "sort-by" in visualize:
            init_data["sort_by"] = visualize["sort-by"]
        if "base-color" in visualize:
            init_data["base_color"] = visualize["base-color"]
        if "block-labels" in visualize:
            init_data["block_labels"] = visualize["block-labels"]

        # Parse negativeColor
        if "negativeColor" in visualize:
            init_data["negative_color"] = NegativeColor.deserialize(
                visualize["negativeColor"]
            )

        # Parse groups column from axes
        if isinstance(axes, dict) and "groups" in axes:
            init_data["groups_column"] = axes["groups"]

        return init_data

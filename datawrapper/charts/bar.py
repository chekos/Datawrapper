from typing import Any, Literal

import pandas as pd
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_serializer

from .annos import RangeAnnotation, TextAnnotation
from .base import BaseChart
from .enums import DateFormat, NumberFormat, ReplaceFlagsType, ValueLabelAlignment
from .serializers import ColorCategory, CustomRange, ModelListSerializer, ReplaceFlags


class BarOverlay(BaseModel):
    """A base class for the Datawrapper API's 'bar-overlay' attribute."""

    model_config = ConfigDict(
        populate_by_name=True,
        strict=True,
        json_schema_extra={
            "examples": [
                {
                    "to_column": "column",
                }
            ]
        },
    )

    #: The type of overlay
    type: Literal["value", "range"] = Field(
        default="value", description="The type of overlay"
    )

    #: The title of the overlay. Defaults to the column name.
    title: str = Field(
        default="", description="The title of the overlay. Defaults to the column name."
    )

    #: The column to draw ranges to or to label, depending on the type
    to_column: str = Field(
        min_length=1,
        alias="to",
        description="The column to draw ranges to or to label, depending on the type",
    )

    #: The column to draw ranges from
    from_column: str = Field(
        default="--zero-baseline--",  # This is datawrapper's default string value for zero
        alias="from",
        description="The column to draw ranges from",
    )

    #: The color of the overlay
    color: str = Field(default="#4682b4", description="The color of the overlay")

    #: The opacity of the overlay
    opacity: float = Field(default=0.6, description="The opacity of the overlay")

    #: The pattern of the overlay when the type is 'range'
    pattern: Literal["solid", "diagonal-up", "diagonal-down"] = Field(
        default="solid",
        description="The pattern of the overlay when the type is 'range'",
    )

    #: Whether or not to show the overlay in the color key
    show_in_color_key: bool = Field(
        default=True,
        alias="showInColorKey",
        description="Whether or not to show the overlay in the color key",
    )

    #: Whether or not to show the overlay directly on the bar
    label_directly: bool = Field(
        default=True,
        alias="labelDirectly",
        description="Whether or not to show the overlay directly on the bar",
    )


class BarChart(BaseChart):
    """A base class for the Datawrapper API's bar chart."""

    model_config = ConfigDict(
        populate_by_name=True,
        strict=True,
        validate_assignment=True,
        validate_default=True,
        use_enum_values=True,
        json_schema_extra={
            "examples": [
                {
                    "chart-type": "d3-bars",
                    "title": "European countries with lowest &amp; highest voter turnout",
                    "source_name": "Parties & Elections, 2024",
                    "source_url": "https://parties-and-elections.eu/",
                    "highlighted-series": [
                        "Malta (2022)",
                        "Turkey (2023)",
                        "Belgium (2024)",
                        "Romania (2020)",
                        "Bulgaria (2024)",
                        "Albania (2021)",
                    ],
                    "custom-range": [0, 100],
                    "background": True,
                    "sort-bars": True,
                    "tick-position": "top",
                    "data": pd.DataFrame(
                        {
                            "Country": [
                                "Malta (2022)",
                                "Turkey (2023)",
                                "Belgium (2024)",
                                "Romania (2020)",
                                "Bulgaria (2024)",
                                "Albania (2021)",
                                "United Kingdom (2024)",
                                "Germany (2021)",
                                "Sweden (2022)",
                                "Spain (2023)",
                                "France (2024)",
                            ],
                            "turnout": [
                                "85.6",
                                "87.0",
                                "88.5",
                                "33.2",
                                "33.4",
                                "46.3",
                                "60.0",
                                "76.4",
                                "83.8",
                                "66.0",
                                "66.7",
                            ],
                        }
                    ),
                }
            ]
        },
    )

    #: The type of datawrapper chart to create
    chart_type: Literal["d3-bars"] = Field(
        default="d3-bars",
        alias="chart-type",
        description="The type of datawrapper chart to create",
    )

    #
    # Labels
    #

    #: The column with the labels for the bars
    label_column: str = Field(
        default="",
        alias="label-column",
        description="The column with the labels for the bars",
    )

    #: On which side are the labels aligned
    label_alignment: Literal["left", "right"] = Field(
        default="left",
        alias="label-alignment",
        description="On which side are the labels aligned",
    )

    #: Whether to move labels to a separate line
    block_labels: bool = Field(
        default=False,
        alias="block-labels",
        description="Whether to move labels to a separate line",
    )

    #: Whether or not to show value labels with the bars
    show_value_labels: bool = Field(
        default=True,
        alias="show-value-labels",
        description="Whether or not to show value labels with the bars",
    )

    #: The alignment of the value labels
    value_label_alignment: ValueLabelAlignment | str = Field(
        default="left",
        alias="value-label-alignment",
        description="The alignment of the value labels",
    )

    #: The format of the value labels (use DateFormat or NumberFormat enum or custom format strings)
    value_label_format: DateFormat | NumberFormat | str = Field(
        default="",
        alias="value-label-format",
        description="The format of the value labels. Use DateFormat for temporal data, NumberFormat for numeric data, or provide custom format strings.",
    )

    #: Whether to swap labels and values
    swap_labels: bool = Field(
        default=False,
        alias="swap-labels",
        description="Whether to swap labels and values",
    )

    #: Whether to replace country codes with flag
    replace_flags: ReplaceFlagsType | str = Field(
        default="off",
        alias="replace-flags",
        description="Whether to replace country codes with flag",
    )

    #: Whether to show the color key
    show_color_key: bool = Field(
        default=False,
        alias="show-color-key",
        description="Whether to show the color key",
    )

    #: Whether to stack the color key
    stack_color_legend: bool = Field(
        default=False,
        alias="stack-color-legend",
        description="Whether to stack the color key",
    )

    #: A list of column to exclude from the color key
    exclude_from_color_key: list[str] = Field(
        default_factory=list,
        alias="exclude-from-color-key",
        description="A list of column to exclude from the color key",
    )

    #
    # Horizontal axis
    #

    #: The column with the value for the bars
    bar_column: str = Field(
        default="",
        alias="bar-column",
        description="The column with the value for the bars",
    )

    #: The custom range for the x axis
    custom_range: list[Any] | tuple[Any, Any] = Field(
        default_factory=lambda: ["", ""],
        alias="custom-range",
        description="The custom range for the x axis",
    )

    #: Whether or not to show the x grid
    force_grid: bool = Field(
        default=False,
        alias="force-grid",
        description="Whether or not to show the x grid",
    )

    #: Set custom grid lines
    custom_grid_lines: list[Any] = Field(
        default_factory=list,
        alias="custom-grid-lines",
        description="Set custom grid lines",
    )

    #: The position of the ticks
    tick_position: Literal["top", "bottom"] = Field(
        default="top", alias="tick-position", description="The position of the ticks"
    )

    #: The format of the axis labels (use DateFormat or NumberFormat enum or custom format strings)
    axis_label_format: DateFormat | NumberFormat | str = Field(
        default="",
        alias="axis-label-format",
        description="The format of the axis labels. Use DateFormat for temporal data, NumberFormat for numeric data, or provide custom format strings.",
    )

    #
    # Appearance
    #

    #: The default color for the chart (palette index or hex string)
    base_color: str | int = Field(
        default=0,
        alias="base-color",
        description="The default color for the chart (palette index or hex string)",
    )

    #: The column with the color for the bars
    color_column: str = Field(
        default="",
        alias="color-column",
        description="The column with the color for the bars",
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

    #: Draw a separating line between bars
    rules: bool = Field(
        default=False, alias="rules", description="Draw a separating line between bars"
    )

    #: Make the bars thicker
    thick: bool = Field(
        default=False, alias="thick", description="Make the bars thicker"
    )

    #: Fill the background of the bar's full potential with a light color
    background: bool = Field(
        default=False,
        alias="background",
        description="Fill the background of the bar's full potential with a light color",
    )

    #
    # Sorting and grouping
    #

    #: Whether to sort the bars
    sort_bars: bool = Field(
        default=False, alias="sort-bars", description="Whether to sort the bars"
    )

    #: Whether to reverse the sort order
    reverse_order: bool = Field(
        default=False,
        alias="reverse-order",
        description="Whether to reverse the sort order",
    )

    #: The column to use for grouping bars
    groups_column: str | None = Field(
        default=None,
        alias="groups-column",
        description="The column to use for grouping bars",
    )

    #: Whether to show the group labels
    show_group_labels: bool = Field(
        default=True,
        alias="show-group-labels",
        description="Whether to show the group labels",
    )

    #: Whether to show the value labels
    show_category_labels: bool = Field(
        default=True,
        alias="show-category-labels",
        description="Whether to show the value labels",
    )

    #
    # Overlays
    #

    #: A list of bar overlays
    overlays: list[BarOverlay | dict[str, Any]] = Field(
        default_factory=list,
        description="A list of bar overlays",
    )

    #
    # Annotations
    #

    #: A list of the highlighted series
    highlighted_series: list[str] = Field(
        default_factory=list,
        alias="highlighted-series",
        description="A list of the highlighted series",
    )

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

        # Add chart specific properties
        model["metadata"]["visualize"].update(
            {
                # Labels
                "label-alignment": self.label_alignment,
                "block-labels": self.block_labels,
                "show-value-labels": self.show_value_labels,
                "value-label-alignment": self.value_label_alignment,
                "value-label-format": self.value_label_format,
                "swap-labels": self.swap_labels,
                "replace-flags": ReplaceFlags.serialize(self.replace_flags),
                "show-color-key": self.show_color_key,
                "stack-color-legend": self.stack_color_legend,
                # Horizontal axis
                "custom-range": CustomRange.serialize(self.custom_range),
                "force-grid": self.force_grid,
                "custom-grid-lines": ",".join(str(t) for t in self.custom_grid_lines),
                "tick-position": self.tick_position,
                "axis-label-format": self.axis_label_format,
                # Appearance
                "base-color": self.base_color,
                "color-category": ColorCategory.serialize(
                    self.color_category,
                    self.category_labels,
                    self.category_order,
                    self.exclude_from_color_key,
                ),
                "color-by-column": bool(self.color_category),
                "rules": self.rules,
                "thick": self.thick,
                "background": self.background,
                # Sorting and grouping
                "sort-bars": self.sort_bars,
                "reverse-order": self.reverse_order,
                "group-by-column": self.groups_column is not None
                and self.groups_column != "",
                "show-group-labels": self.show_group_labels,
                "show-category-labels": self.show_category_labels,
                # Overlays
                "overlays": [],
                # Annotations
                "highlighted-series": self.highlighted_series,
                "text-annotations": ModelListSerializer.serialize(
                    self.text_annotations, TextAnnotation
                ),
                "range-annotations": ModelListSerializer.serialize(
                    self.range_annotations, RangeAnnotation
                ),
            }
        )

        # Add the overlays, if any
        for overlay_obj in self.overlays:
            # If the overlay is a dictionary, validate it and convert it to a BarOverlay object
            if isinstance(overlay_obj, dict):
                overlay_dict = BarOverlay.model_validate(overlay_obj).model_dump(
                    by_alias=True
                )
            # If the overlay is a BarOverlay object, convert it to a dictionary
            elif isinstance(overlay_obj, BarOverlay):
                overlay_dict = overlay_obj.model_dump(by_alias=True)
            # If the overlay is neither, raise an error
            else:
                raise ValueError("Overlays must be BarOverlay objects or dicts")
            # Add the overlay to the list of overlays
            model["metadata"]["visualize"]["overlays"].append(overlay_dict)

        # Add axes configuration to metadata
        axes_config = {
            "colors": self.color_column or self.label_column,
            "bars": self.bar_column,
            "labels": self.label_column,
        }

        # Only add groups if it's set
        if self.groups_column:
            axes_config["groups"] = self.groups_column

        model["metadata"]["axes"] = axes_config

        # Return the serialized data
        return model

    @classmethod
    def deserialize_model(cls, api_response: dict[str, Any]) -> dict[str, Any]:
        """Parse Datawrapper API response including bar chart specific fields.

        Args:
            api_response: The JSON response from the chart metadata endpoint

        Returns:
            Dictionary that can be used to initialize the BarChart model
        """
        # Call parent to get base fields
        init_data = super().deserialize_model(api_response)

        # Extract bar-specific sections
        metadata = api_response.get("metadata", {})
        visualize = metadata.get("visualize", {})
        axes = metadata.get("axes", {})

        # Labels
        if "labels" in axes:
            init_data["label_column"] = axes["labels"]
        if "label-alignment" in visualize:
            init_data["label_alignment"] = visualize["label-alignment"]
        if "block-labels" in visualize:
            init_data["block_labels"] = visualize["block-labels"]
        if "show-value-labels" in visualize:
            init_data["show_value_labels"] = visualize["show-value-labels"]
        if "value-label-alignment" in visualize:
            init_data["value_label_alignment"] = visualize["value-label-alignment"]
        if "value-label-format" in visualize:
            init_data["value_label_format"] = visualize["value-label-format"]
        if "swap-labels" in visualize:
            init_data["swap_labels"] = visualize["swap-labels"]

        # Replace flags
        if "replace-flags" in visualize:
            init_data["replace_flags"] = ReplaceFlags.deserialize(
                visualize["replace-flags"]
            )

        if "show-color-key" in visualize:
            init_data["show_color_key"] = visualize["show-color-key"]
        if "stack-color-legend" in visualize:
            init_data["stack_color_legend"] = visualize["stack-color-legend"]

        # Horizontal axis
        if "bars" in axes:
            init_data["bar_column"] = axes["bars"]
        init_data["custom_range"] = CustomRange.deserialize(
            visualize.get("custom-range")
        )
        if "force-grid" in visualize:
            init_data["force_grid"] = visualize["force-grid"]

        # Parse custom grid lines (comes as comma-separated string)
        if "custom-grid-lines" in visualize:
            grid_lines_str = visualize["custom-grid-lines"]
            if grid_lines_str:
                init_data["custom_grid_lines"] = [
                    float(x.strip()) if x.strip() else x.strip()
                    for x in grid_lines_str.split(",")
                ]

        if "tick-position" in visualize:
            init_data["tick_position"] = visualize["tick-position"]
        if "axis-label-format" in visualize:
            init_data["axis_label_format"] = visualize["axis-label-format"]

        # Appearance
        if "base-color" in visualize:
            init_data["base_color"] = visualize["base-color"]
        if "colors" in axes:
            init_data["color_column"] = axes["colors"]

        # Parse color-category using utility
        init_data.update(ColorCategory.deserialize(visualize.get("color-category")))

        if "rules" in visualize:
            init_data["rules"] = visualize["rules"]
        if "thick" in visualize:
            init_data["thick"] = visualize["thick"]
        if "background" in visualize:
            init_data["background"] = visualize["background"]

        # Sorting and grouping
        if "sort-bars" in visualize:
            init_data["sort_bars"] = visualize["sort-bars"]
        if "reverse-order" in visualize:
            init_data["reverse_order"] = visualize["reverse-order"]
        if "groups" in axes:
            init_data["groups_column"] = axes["groups"]
        if "show-group-labels" in visualize:
            init_data["show_group_labels"] = visualize["show-group-labels"]
        if "show-category-labels" in visualize:
            init_data["show_category_labels"] = visualize["show-category-labels"]

        # Overlays (list of BarOverlay objects)
        if "overlays" in visualize:
            overlays_list = visualize["overlays"]
            init_data["overlays"] = [
                BarOverlay.model_validate(overlay) for overlay in overlays_list
            ]

        # Annotations
        if "highlighted-series" in visualize:
            init_data["highlighted_series"] = visualize["highlighted-series"]

        # Annotations
        init_data["text_annotations"] = TextAnnotation.deserialize_model(
            visualize.get("text-annotations")
        )
        init_data["range_annotations"] = RangeAnnotation.deserialize_model(
            visualize.get("range-annotations")
        )

        return init_data

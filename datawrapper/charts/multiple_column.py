from collections.abc import Sequence
from typing import Any, Literal

import pandas as pd
from pydantic import (
    ConfigDict,
    Field,
    field_validator,
    model_serializer,
    model_validator,
)

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
from .models import (
    AnnotationsMixin,
    CustomRangeMixin,
    CustomTicksMixin,
    GridDisplayMixin,
    GridFormatMixin,
    RangeAnnotation,
    TextAnnotation,
)
from .serializers import (
    ColorCategory,
    NegativeColor,
    PlotHeight,
    ValueLabels,
)


class MultipleColumnTextAnnotation(TextAnnotation):
    """Text annotation with additional fields specific to MultipleColumnChart.

    This subclass extends TextAnnotation to support multi-panel charts where
    annotations can be associated with specific plots/panels.

    Attributes:
        plot: Which plot/panel this annotation applies to (e.g., "Paris", "London")
        showInAllPlots: Whether to show this annotation in all plots (defaults to False)
    """

    #: Which plot/panel this annotation applies to
    plot: str | None = Field(
        default=None,
        description="Which plot/panel this annotation applies to",
    )

    #: Whether to show this annotation in all plots
    show_in_all_plots: bool = Field(
        default=False,
        alias="showInAllPlots",
        description="Whether to show this annotation in all plots",
    )

    def serialize_model(self) -> dict:
        """Serialize the annotation to API format.

        Extends the base TextAnnotation serialization to include:
        - plot field inside the position object
        - showInAllPlots field at the top level

        Returns:
            Dictionary in Datawrapper API format
        """
        result = super().serialize_model()

        # Add plot to position object if specified
        if self.plot is not None:
            result["position"]["plot"] = self.plot

        # Always include showInAllPlots at top level
        result["showInAllPlots"] = self.show_in_all_plots

        return result

    @classmethod
    def deserialize_model(cls, api_data: dict[str, dict] | None) -> list[dict]:
        """Parse API response to extract MultipleColumnTextAnnotation data.

        Handles the API format where:
        - x, y, and plot are inside the position object
        - showInAllPlots is at the top level

        Args:
            api_data: API response data (dict with UUID keys)

        Returns:
            List of dictionaries that can initialize MultipleColumnTextAnnotation instances
        """
        if not api_data:
            return []

        result = []
        for anno_id, anno_data in api_data.items():
            # Extract position data
            position = anno_data.get("position", {})
            x = position.get("x") if isinstance(position, dict) else None
            y = position.get("y") if isinstance(position, dict) else None
            plot = position.get("plot") if isinstance(position, dict) else None

            # Extract showInAllPlots (defaults to False for text annotations)
            show_in_all = anno_data.get("showInAllPlots", False)

            # Build annotation dict with id
            anno_dict = {**anno_data, "id": anno_id}

            # Add position fields
            if x is not None:
                anno_dict["x"] = x
            if y is not None:
                anno_dict["y"] = y

            # Add MultipleColumnChart-specific fields
            if plot is not None:
                anno_dict["plot"] = plot
            anno_dict["show_in_all_plots"] = show_in_all

            result.append(anno_dict)
        return result


class MultipleColumnRangeAnnotation(RangeAnnotation):
    """Range annotation with additional fields specific to MultipleColumnChart.

    This subclass extends RangeAnnotation to support multi-panel charts where
    annotations can be associated with specific plots/panels.

    Attributes:
        plot: Which plot/panel this annotation applies to (e.g., "Paris", "London")
        showInAllPlots: Whether to show this annotation in all plots (defaults to True)
    """

    #: Which plot/panel this annotation applies to
    plot: str | None = Field(
        default=None,
        description="Which plot/panel this annotation applies to",
    )

    #: Whether to show this annotation in all plots
    show_in_all_plots: bool = Field(
        default=True,
        alias="showInAllPlots",
        description="Whether to show this annotation in all plots",
    )

    def serialize_model(self) -> dict:
        """Serialize the annotation to API format.

        Extends the base RangeAnnotation serialization to include:
        - plot field inside the position object
        - showInAllPlots field at the top level

        Returns:
            Dictionary in Datawrapper API format
        """
        result = super().serialize_model()

        # Add plot to position object if specified
        if self.plot is not None:
            result["position"]["plot"] = self.plot

        # Always include showInAllPlots at top level
        result["showInAllPlots"] = self.show_in_all_plots

        return result

    @classmethod
    def deserialize_model(cls, api_data: dict[str, dict] | None) -> list[dict]:
        """Parse API response to extract MultipleColumnRangeAnnotation data.

        Handles the API format where:
        - plot is inside the position object
        - showInAllPlots is at the top level

        Args:
            api_data: API response data (dict with UUID keys)

        Returns:
            List of dictionaries that can initialize MultipleColumnRangeAnnotation instances
        """
        if not api_data:
            return []

        result = []
        for anno_id, anno_data in api_data.items():
            # Extract position data
            position = anno_data.get("position", {})
            plot = position.get("plot") if isinstance(position, dict) else None

            # Extract showInAllPlots (defaults to True)
            show_in_all = anno_data.get("showInAllPlots", True)

            # Build annotation dict with id
            anno_dict = {**anno_data, "id": anno_id}

            # Add MultipleColumnChart-specific fields
            if plot is not None:
                anno_dict["plot"] = plot
            anno_dict["show_in_all_plots"] = show_in_all

            result.append(anno_dict)
        return result


class MultipleColumnXRangeAnnotation(MultipleColumnRangeAnnotation):
    """A horizontal range annotation for MultipleColumnChart.

    This is a convenience class that automatically sets type="x" and display="range",
    and validates that both x0 and x1 are provided.
    """

    def __init__(self, **data):
        data.setdefault("type", "x")
        data.setdefault("display", "range")
        super().__init__(**data)

    @model_validator(mode="after")
    def validate_x_positions_required(self) -> "MultipleColumnXRangeAnnotation":
        if self.x0 is None or self.x1 is None:
            raise ValueError(
                "MultipleColumnXRangeAnnotation requires both x0 and x1 to be set"
            )
        return self


class MultipleColumnYRangeAnnotation(MultipleColumnRangeAnnotation):
    """A vertical range annotation for MultipleColumnChart.

    This is a convenience class that automatically sets type="y" and display="range",
    and validates that both y0 and y1 are provided.
    """

    def __init__(self, **data):
        data.setdefault("type", "y")
        data.setdefault("display", "range")
        super().__init__(**data)

    @model_validator(mode="after")
    def validate_y_positions_required(self) -> "MultipleColumnYRangeAnnotation":
        if self.y0 is None or self.y1 is None:
            raise ValueError(
                "MultipleColumnYRangeAnnotation requires both y0 and y1 to be set"
            )
        return self


class MultipleColumnXLineAnnotation(MultipleColumnRangeAnnotation):
    """A vertical line annotation for MultipleColumnChart.

    This is a convenience class that automatically sets type="x" and display="line",
    and validates that x0 is provided.
    """

    def __init__(self, **data):
        data.setdefault("type", "x")
        data.setdefault("display", "line")
        super().__init__(**data)

    @model_validator(mode="after")
    def validate_x_position_required(self) -> "MultipleColumnXLineAnnotation":
        if self.x0 is None:
            raise ValueError("MultipleColumnXLineAnnotation requires x0 to be set")
        return self


class MultipleColumnYLineAnnotation(MultipleColumnRangeAnnotation):
    """A horizontal line annotation for MultipleColumnChart.

    This is a convenience class that automatically sets type="y" and display="line",
    and validates that y0 is provided.
    """

    def __init__(self, **data):
        data.setdefault("type", "y")
        data.setdefault("display", "line")
        super().__init__(**data)

    @model_validator(mode="after")
    def validate_y_position_required(self) -> "MultipleColumnYLineAnnotation":
        if self.y0 is None:
            raise ValueError("MultipleColumnYLineAnnotation requires y0 to be set")
        return self


class MultipleColumnChart(
    GridDisplayMixin,
    GridFormatMixin,
    CustomRangeMixin,
    CustomTicksMixin,
    AnnotationsMixin,
    BaseChart,
):
    """A base class for the Datawrapper API's multiple column chart.

    Note: This chart uses MultipleColumnTextAnnotation and MultipleColumnRangeAnnotation
    for annotations, which extend the base annotation classes with plot-specific fields.
    The parent AnnotationsMixin fields accept these subclasses automatically.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        strict=True,
        validate_assignment=True,
        validate_default=True,
        use_enum_values=True,
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

    #: The labeling of the x axis
    x_grid_labels: Literal["on", "off"] = Field(
        default="on",
        alias="x-grid-labels",
        description="The labeling of the x axis",
    )

    #: x_grid for panels
    x_grid_all: GridDisplay | str = Field(
        default="off",
        alias="x-grid-all",
        description="x_grid for panels",
    )

    #
    # Vertical axis
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

    @field_validator("plot_height_mode")
    @classmethod
    def validate_plot_height_mode(cls, v: PlotHeightMode | str) -> PlotHeightMode | str:
        """Validate that plot_height_mode is a valid PlotHeightMode value."""
        if isinstance(v, str):
            valid_values = [e.value for e in PlotHeightMode]
            if v not in valid_values:
                raise ValueError(f"Invalid value: {v}. Must be one of {valid_values}")
        return v

    @field_validator("text_annotations", mode="before")
    @classmethod
    def convert_text_annotations(
        cls, v: Sequence[MultipleColumnTextAnnotation | dict[Any, Any]]
    ) -> list[MultipleColumnTextAnnotation]:
        """Convert dict annotations to MultipleColumnTextAnnotation instances.

        This ensures that when annotations are passed as dicts, they are converted
        to the proper annotation class so that serialize_model() includes the plot field.
        """
        if not v:
            return []

        result = []
        for item in v:
            if isinstance(item, dict):
                # Convert dict to MultipleColumnTextAnnotation instance
                result.append(MultipleColumnTextAnnotation(**item))
            else:
                # Already an instance, keep as is
                result.append(item)
        return result

    @field_validator("range_annotations", mode="before")
    @classmethod
    def convert_range_annotations(
        cls, v: Sequence[MultipleColumnRangeAnnotation | dict[Any, Any]]
    ) -> list[MultipleColumnRangeAnnotation]:
        """Convert dict annotations to MultipleColumnRangeAnnotation instances.

        This ensures that when annotations are passed as dicts, they are converted
        to the proper annotation class so that serialize_model() includes the plot field.
        """
        if not v:
            return []

        result = []
        for item in v:
            if isinstance(item, dict):
                # Convert dict to MultipleColumnRangeAnnotation instance
                result.append(MultipleColumnRangeAnnotation(**item))
            else:
                # Already an instance, keep as is
                result.append(item)
        return result

    #
    # Tooltips
    #

    #: Whether or not to show tooltips on hover
    show_tooltips: bool = Field(
        default=True,
        alias="show-tooltips",
        description="Whether or not to show tooltips on hover",
    )

    #: Whether to show tooltips synchronously across all panels
    sync_multiple_tooltips: bool = Field(
        default=False,
        alias="syncMultipleTooltips",
        description="Whether to show tooltips synchronously across all panels",
    )

    #: The format for the y-axis values in tooltips (use DateFormat or NumberFormat enum or custom format strings)
    tooltip_number_format: DateFormat | NumberFormat | str = Field(
        default="",
        alias="tooltip-number-format",
        description="The format for the y-axis values in tooltips. Use DateFormat for temporal data, NumberFormat for numeric data, or provide custom format strings.",
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

    #: Whether or not to show value labels
    show_value_labels: ValueLabelDisplay | str = Field(
        default="off",
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

    @model_serializer
    def serialize_model(self) -> dict:
        """Serialize the model to a dictionary."""
        # Call the parent class's serialize_model method
        model = super().serialize_model()

        # Add chart specific properties to visualize section
        visualize_data = {
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
            # Horizontal and vertical axis (from mixins)
            **self._serialize_grid_config(),
            **self._serialize_grid_format(),
            **self._serialize_custom_range(),
            **self._serialize_custom_ticks(),
            # Horizontal axis (chart-specific)
            "x-grid-labels": self.x_grid_labels,
            "x-grid": self.x_grid_all,
            "grid-lines-x": {
                "type": "" if self.x_grid == "off" else self.x_grid,
                "enabled": self.x_grid != "off",
            },
            # Vertical axis (chart-specific)
            "grid-lines": self.y_grid,
            "yAxisLabels": {
                "enabled": self.y_grid_labels != "off",
                "alignment": self.y_grid_label_align,
                "placement": "" if self.y_grid_labels == "off" else self.y_grid_labels,
            },
            # Appearance
            "base-color": self.base_color,
            "negativeColor": NegativeColor.serialize(self.negative_color),
            "bar-padding": self.bar_padding,
            "color-category": ColorCategory.serialize(self.color_category),
            "color-by-column": bool(self.color_category),
            **PlotHeight.serialize(
                self.plot_height_mode,
                self.plot_height_fixed,
                self.plot_height_ratio,
            ),
            "panels": {panel["column"]: panel for panel in self.panels},
            # Tooltips
            "show-tooltips": self.show_tooltips,
            "syncMultipleTooltips": self.sync_multiple_tooltips,
            "tooltip-number-format": self.tooltip_number_format,
            # Labels
            "show-color-key": self.show_color_key,
            "label-colors": self.label_colors,
            "label-margin": self.label_margin,
            **ValueLabels.serialize(
                self.show_value_labels,
                self.value_labels_format,
                placement=self.value_labels_placement,
                chart_type="multiple-column",
            ),
            "xGridLabelAllColumns": self.x_grid_label_all,
            # Annotations
            **self._serialize_annotations(
                text_annotation_class=MultipleColumnTextAnnotation,
                range_annotation_class=MultipleColumnRangeAnnotation,
            ),
        }

        model["metadata"]["visualize"].update(visualize_data)

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
        if "gridLayout" in visualize:
            init_data["grid_layout"] = visualize["gridLayout"]
        if "gridColumnCount" in visualize:
            init_data["grid_column"] = visualize["gridColumnCount"]
        if "gridColumnCountMobile" in visualize:
            init_data["grid_column_mobile"] = visualize["gridColumnCountMobile"]
        if "gridColumnMinWidth" in visualize:
            init_data["grid_column_width"] = visualize["gridColumnMinWidth"]
        if "gridRowHeightFixed" in visualize:
            init_data["grid_row_height"] = visualize["gridRowHeightFixed"]

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

        # Horizontal and vertical axis (from mixins)
        init_data.update(cls._deserialize_grid_config(visualize))
        init_data.update(cls._deserialize_grid_format(visualize))
        init_data.update(cls._deserialize_custom_range(visualize))
        init_data.update(cls._deserialize_custom_ticks(visualize))

        # Horizontal axis (chart-specific)
        if "x-grid-labels" in visualize:
            init_data["x_grid_labels"] = visualize["x-grid-labels"]
        if "x-grid" in visualize:
            init_data["x_grid_all"] = visualize["x-grid"]

        # Parse grid-lines-x
        grid_lines_x = visualize.get("grid-lines-x", {})
        if isinstance(grid_lines_x, dict):
            if grid_lines_x.get("enabled", False):
                init_data["x_grid"] = grid_lines_x.get("type", "ticks")
            else:
                init_data["x_grid"] = "off"
        else:
            init_data["x_grid"] = "off"

        # Vertical axis (chart-specific)
        # Parse grid-lines (can be bool or string "show")
        if "grid-lines" in visualize:
            grid_lines_val = visualize["grid-lines"]
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
            if "y-grid-labels" in visualize:
                init_data["y_grid_labels"] = visualize["y-grid-labels"]
            if "y-grid-label-align" in visualize:
                init_data["y_grid_label_align"] = visualize["y-grid-label-align"]

        # Appearance
        if "base-color" in visualize:
            init_data["base_color"] = visualize["base-color"]

        if "bar-padding" in visualize:
            init_data["bar_padding"] = visualize["bar-padding"]

        # Parse color-category using utility
        color_data = ColorCategory.deserialize(visualize.get("color-category"))
        init_data["color_category"] = color_data["color_category"]

        # Parse negativeColor
        if "negativeColor" in visualize:
            init_data["negative_color"] = NegativeColor.deserialize(
                visualize["negativeColor"]
            )

        # Plot height
        init_data.update(PlotHeight.deserialize(visualize))

        # Parse panels (dict to list)
        panels_obj = visualize.get("panels", {})
        if isinstance(panels_obj, dict):
            init_data["panels"] = [
                {"column": col, **config} for col, config in panels_obj.items()
            ]
        else:
            init_data["panels"] = []

        # Tooltips
        if "show-tooltips" in visualize:
            init_data["show_tooltips"] = visualize["show-tooltips"]
        if "syncMultipleTooltips" in visualize:
            init_data["sync_multiple_tooltips"] = visualize["syncMultipleTooltips"]
        if "tooltip-number-format" in visualize:
            init_data["tooltip_number_format"] = visualize["tooltip-number-format"]

        # Labels
        if "label-colors" in visualize:
            init_data["label_colors"] = visualize["label-colors"]
        if "show-color-key" in visualize:
            init_data["show_color_key"] = visualize["show-color-key"]
        if "label-margin" in visualize:
            init_data["label_margin"] = visualize["label-margin"]
        if "xGridLabelAllColumns" in visualize:
            init_data["x_grid_label_all"] = visualize["xGridLabelAllColumns"]

        # Parse valueLabels using utility
        init_data.update(
            ValueLabels.deserialize(visualize, chart_type="multiple-column")
        )

        # Annotations
        init_data.update(
            cls._deserialize_annotations(
                visualize,
                text_annotation_class=MultipleColumnTextAnnotation,
                range_annotation_class=MultipleColumnRangeAnnotation,
            )
        )

        return init_data

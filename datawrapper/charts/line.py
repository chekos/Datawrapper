from typing import Any, Literal

import pandas as pd
from pydantic import BaseModel, ConfigDict, Field, model_serializer

from .annos import RangeAnnotation, TextAnnotation
from .base import BaseChart
from .models import CustomTicks


class LineSymbol(BaseModel):
    """Configure the symbols for an individual line on a Datawrapper line chart."""

    model_config = ConfigDict(populate_by_name=True, strict=True)

    #: Whether or not to show symbols
    enabled: bool = Field(
        default=False,
        description="Whether or not to show symbols",
    )

    #: The shape of the symbol
    shape: Literal[
        "circle",
        "square",
        "diamond",
        "triangleUp",
        "triangleDown",
        "cross",
        "hexagon",
        "star",
        "wye",
    ] = Field(
        default="circle",
        description="The shape of the symbol",
    )

    #: The style of the symbol
    style: Literal["hollow", "fill"] = Field(
        default="fill",
        description="The style of the symbol",
    )

    #: Where to show the symbols
    on: Literal["every", "first", "last", "both"] = Field(
        default="last",
        description="Where to show the symbols",
    )

    #: The size of the symbols
    size: int = Field(
        default=6,
        description="The size of the symbols",
    )

    #: The opacity of the symbols between 0 and 1
    opacity: float = Field(
        default=1.0,
        description="The opacity of the symbols between 0 and 1",
    )


class LineValueLabel(BaseModel):
    """Configure the value labels for an individual line on a Datawrapper line chart."""

    model_config = ConfigDict(populate_by_name=True, strict=True)

    #: Whether to show the value labels
    enabled: bool = Field(
        default=False,
        description="Whether to show the value labels",
    )

    #: Whether to show the last value label
    last: bool = Field(
        default=False,
        description="Whether to show the last value label",
    )

    #: Whether to show the first value label
    first: bool = Field(
        default=False,
        description="Whether to show the first value label",
    )

    #: Whether to show circles at automatically drawn inner value labels
    show_circles: bool = Field(
        default=False,
        alias="showCircles",
        description="Whether to show circles at automatically drawn inner value labels",
    )

    #: The maximum number of inner value labels to show
    max_inner_labels: int = Field(
        default=0,
        alias="maxInnerLabels",
        description="The maximum number of inner value labels to show",
    )


class AreaFill(BaseModel):
    """Configure a fill between two lines on a Datawrapper line chart."""

    model_config = ConfigDict(populate_by_name=True, strict=True)

    #: The line to fill upwards from
    from_column: str = Field(
        alias="from",
        description="The line to fill upwards from",
    )

    #: The line to fill upwards to
    to_column: str = Field(
        alias="to",
        description="The line to fill upwards to",
    )

    #: The color of the fill
    color: str = Field(
        default="#4682b4",
        description="The color of the fill",
    )

    #: The opacity of the fill
    opacity: float = Field(
        default=0.15,
        description="The opacity of the fill",
    )

    #: Whether to use different colors when there are negative values
    use_mixed_colors: bool = Field(
        default=False,
        alias="useMixedColors",
        description="Whether to use different colors when there are negative values",
    )

    #: The color of the fill when it is negative
    color_negative: str = Field(
        default="#E31A1C",
        alias="colorNegative",
        description="The color of the fill when it is negative",
    )

    #: The interpolation method to use when drawing lines
    interpolation: Literal[
        "linear",
        "step",
        "step-after",
        "step-before",
        "monotone-x",
        "cardinal",
    ] = Field(
        default="linear",
        description="The interpolation method to use when drawing lines",
    )


class Line(BaseModel):
    """Configure a line on a Datawrapper line chart."""

    model_config = ConfigDict(populate_by_name=True, strict=True)

    #: The name of the data column for the line
    column: str = Field(
        description="The name of the data column for the line",
    )

    #: The title to display in tooltips and legends
    title: str = Field(
        default="",
        description="The title to display in tooltips and legends",
    )

    #: The interpolation method to use when drawing lines
    interpolation: Literal[
        "linear",
        "step",
        "step-after",
        "step-before",
        "monotone-x",
        "cardinal",
    ] = Field(
        default="linear",
        description="The interpolation method to use when drawing lines",
    )

    #: The width of the line
    width: Literal["style0", "style1", "style2", "style3", "invisible"] = Field(
        default="style1",
        description="The width of the line",
    )

    #: The dashing of the line
    dash: Literal["style1", "style2", "style3"] | None = Field(
        default=None,
        description="The dashing of the line",
    )

    #: Whether or not to show in the color key
    color_key: bool = Field(
        default=False,
        alias="colorKey",
        description="Whether or not to show in the color key",
    )

    #: Whether or not to show a direct label for the line in the right hand margin
    direct_label: bool = Field(
        default=False,
        alias="directLabel",
        description="Whether or not to show a direct label for the line in the right hand margin",
    )

    #: Line outline
    outline: bool = Field(
        default=False,
        alias="bgStroke",
        description="Line outline",
    )

    #: Symbols to display on the line
    symbols: LineSymbol = Field(
        default_factory=LineSymbol,
        description="Symbols to display on the line",
    )

    #: The value labels for the line
    value_labels: LineValueLabel = Field(
        default_factory=LineValueLabel,
        alias="valueLabels",
        description="The value labels for the line",
    )

    #: Whether or not to connect missing points
    connect_missing_points: bool = Field(
        default=False,
        alias="connectMissingPoints",
        description="Whether or not to connect missing points",
    )


class LineChart(BaseChart):
    """A base class for the Datawrapper API's line chart."""

    model_config = ConfigDict(
        populate_by_name=True,
        strict=True,
        json_schema_extra={
            "examples": [
                {
                    "chart-type": "d3-lines",
                    "title": "Temperature Over Time",
                    "source_name": "Weather Station",
                    "data": pd.DataFrame(
                        {
                            "date": ["2020/01", "2020/02", "2020/03"],
                            "Temperature": [15.0, 18.0, 22.0],
                        }
                    ),
                    "y_grid": "on",
                    "interpolation": "monotone-x",
                }
            ]
        },
    )

    #: The type of datawrapper chart to create
    chart_type: Literal["d3-lines"] = Field(
        default="d3-lines",
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
        description="The formatting for the x grid labels. Customization options found at https://academy.datawrapper.de/article/164-date-formats-that-datawrapper-recognizes",
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

    #: How to scale the y-axis
    scale_y: Literal["linear", "log"] = Field(
        default="linear",
        alias="scale-y",
        description="How to scale the y-axis",
    )

    #: Whether or not to subdivide a log scale
    y_grid_subdivide: bool = Field(
        default=True,
        alias="y-grid-subdivide",
        description="Whether or not to subdivide a log scale",
    )

    #
    # Customize lines
    #

    #: The base color for lines
    base_color: str | int = Field(
        default="#4682b4",
        alias="base-color",
        description="The base color for lines",
    )

    #: The interpolation method to use when drawing lines
    interpolation: Literal[
        "linear",
        "step",
        "step-after",
        "step-before",
        "monotone-x",
        "cardinal",
    ] = Field(
        default="linear",
        description="The interpolation method to use when drawing lines",
    )

    #: Whether or not to draw a connector line between lines and labels
    connector_lines: bool = Field(
        default=False,
        alias="connector-lines",
        description="Whether or not to draw a connector line between lines and labels",
    )

    #: A mapping of layer names to colors
    color_category: dict[str, str] = Field(
        default_factory=dict,
        alias="color-category",
        description="A mapping of layer names to colors",
    )

    #: Custom configuration for individual lines
    lines: list[Line | dict[str, Any]] = Field(
        default_factory=list,
        description="Custom configuration for individual lines",
    )

    #: Custom area fills
    area_fills: list[AreaFill | dict[str, Any]] = Field(
        default_factory=list,
        alias="area-fills",
        description="Custom area fills",
    )

    #
    # Labels
    #

    #: Whether or not to stack the color legend
    stack_color_legend: bool = Field(
        default=False,
        alias="stack-color-legend",
        description="Whether or not to stack the color legend",
    )

    #: Whether or not to color line category labels the same as the line
    label_colors: bool = Field(
        default=False,
        alias="label-colors",
        description="Whether or not to color line category labels the same as the line",
    )

    #: The amount of margin to leave for the right hand side for labels
    label_margin: int = Field(
        default=0,
        alias="label-margin",
        description="The amount of margin to leave for the right hand side for labels. Zero is automatically calculated.",
    )

    #: The number format for value labels
    value_labels_format: str = Field(
        default="",
        alias="value-labels-format",
        description="The number format for value labels. Customization options can be found at https://academy.datawrapper.de/article/207-custom-number-formats-that-you-can-display-in-datawrapper",
    )

    #: Whether to color number values labels the same as the line
    value_label_colors: bool = Field(
        default=False,
        alias="value-label-colors",
        description="Whether to color number values labels the same as the line",
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
        description="The format of the number tooltip. Customization options can be found at https://academy.datawrapper.de/article/207-custom-number-formats-that-you-can-display-in-datawrapper",
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
                "custom-ticks-x": CustomTicks.serialize(self.custom_ticks_x),
                "x-grid-format": self.x_grid_format,
                "x-grid": self.x_grid,
                # Vertical axis
                "custom-range-y": self.custom_range_y,
                "custom-ticks-y": CustomTicks.serialize(self.custom_ticks_y),
                "y-grid-format": self.y_grid_format,
                "y-grid": self.y_grid,
                "y-grid-labels": self.y_grid_labels,
                "y-grid-label-align": self.y_grid_label_align,
                "scale-y": self.scale_y,
                "y-grid-subdivide": self.y_grid_subdivide,
                # Customize lines
                "base-color": self.base_color,
                "interpolation": self.interpolation,
                "connector-lines": self.connector_lines,
                "color-category": {"map": self.color_category},
                # Labels
                "stack-color-legend": self.stack_color_legend,
                "label-colors": self.label_colors,
                "label-margin": self.label_margin,
                "value-labels-format": self.value_labels_format,
                "value-label-colors": self.value_label_colors,
                # Tooltips
                "show-tooltips": self.show_tooltips,
                "tooltip-x-format": self.tooltip_x_format,
                "tooltip-number-format": self.tooltip_number_format,
                # Appearance
                "plotHeightMode": self.plot_height_mode,
                "plotHeightFixed": self.plot_height_fixed,
                "plotHeightRatio": self.plot_height_ratio,
                # Initialize empty structures
                "lines": {},
                "custom-area-fills": {},
                "text-annotations": self._serialize_annotations(
                    self.text_annotations, TextAnnotation
                ),
                "range-annotations": self._serialize_annotations(
                    self.range_annotations, RangeAnnotation
                ),
            }
        )

        # Add line configurations
        for line_obj in self.lines:
            if isinstance(line_obj, dict):
                line_config = Line.model_validate(line_obj)
            elif isinstance(line_obj, Line):
                line_config = line_obj
            else:
                raise ValueError("Lines must be Line objects or dicts")

            # Get the column name from the line config
            line_name = line_config.column

            # Serialize the line configuration
            line_dict = {
                "title": line_config.title,
                "interpolation": line_config.interpolation,
                "width": line_config.width,
                "colorKey": line_config.color_key,
                "directLabel": line_config.direct_label,
                "bgStroke": line_config.outline,
                "connectMissingPoints": line_config.connect_missing_points,
            }

            # Add dash if set
            if line_config.dash is not None:
                line_dict["dash"] = line_config.dash

            # Add symbols configuration
            line_dict["symbols"] = {
                "enabled": line_config.symbols.enabled,
                "shape": line_config.symbols.shape,
                "style": line_config.symbols.style,
                "on": line_config.symbols.on,
                "size": line_config.symbols.size,
                "opacity": line_config.symbols.opacity,
            }

            # Add value labels configuration
            line_dict["valueLabels"] = {
                "enabled": line_config.value_labels.enabled,
                "last": line_config.value_labels.last,
                "first": line_config.value_labels.first,
                "showCircles": line_config.value_labels.show_circles,
                "maxInnerLabels": line_config.value_labels.max_inner_labels,
            }

            model["metadata"]["visualize"]["lines"][line_name] = line_dict

        # Add area fills
        for fill_obj in self.area_fills:
            if isinstance(fill_obj, dict):
                fill_config = AreaFill.model_validate(fill_obj)
            elif isinstance(fill_obj, AreaFill):
                fill_config = fill_obj
            else:
                raise ValueError("Area fills must be AreaFill objects or dicts")

            # Generate a unique ID for the fill
            import uuid

            fill_id = str(uuid.uuid4()).replace("-", "")[:10]

            model["metadata"]["visualize"]["custom-area-fills"][fill_id] = {
                "from": fill_config.from_column,
                "to": fill_config.to_column,
                "color": fill_config.color,
                "opacity": fill_config.opacity,
                "useMixedColors": fill_config.use_mixed_colors,
                "colorNegative": fill_config.color_negative,
                "interpolation": fill_config.interpolation,
            }

        # Return the serialized data
        return model

    @classmethod
    def deserialize_model(cls, api_response: dict[str, Any]) -> dict[str, Any]:
        """Parse Datawrapper API response including line chart specific fields.

        Args:
            api_response: The JSON response from the chart metadata endpoint
            chart_data: The CSV data from the chart data endpoint

        Returns:
            Dictionary that can be used to initialize the LineChart model
        """
        # Call parent to get base fields
        init_data = super().deserialize_model(api_response)

        # Extract line-specific sections
        metadata = api_response.get("metadata", {})
        visualize = metadata.get("visualize", {})

        # Horizontal axis (X-axis)
        init_data["custom_range_x"] = visualize.get("custom-range-x", ["", ""])
        init_data["custom_ticks_x"] = CustomTicks.deserialize(
            visualize.get("custom-ticks-x", "")
        )
        init_data["x_grid_format"] = visualize.get("x-grid-format", "auto")
        init_data["x_grid"] = visualize.get("x-grid", "off")

        # Vertical axis (Y-axis)
        init_data["custom_range_y"] = visualize.get("custom-range-y", ["", ""])
        init_data["custom_ticks_y"] = CustomTicks.deserialize(
            visualize.get("custom-ticks-y", "")
        )

        init_data["y_grid_format"] = visualize.get("y-grid-format", "")
        init_data["y_grid"] = visualize.get("y-grid", "on")
        init_data["y_grid_labels"] = visualize.get("y-grid-labels", "auto")
        init_data["y_grid_label_align"] = visualize.get("y-grid-label-align", "left")
        init_data["scale_y"] = visualize.get("scale-y", "linear")
        init_data["y_grid_subdivide"] = visualize.get("y-grid-subdivide", True)

        # Customize lines
        init_data["base_color"] = visualize.get("base-color", "#4682b4")
        init_data["interpolation"] = visualize.get("interpolation", "linear")
        init_data["connector_lines"] = visualize.get("connector-lines", False)

        # Parse color-category
        color_category_obj = visualize.get("color-category", {})
        if isinstance(color_category_obj, dict):
            init_data["color_category"] = color_category_obj.get("map", {})
        else:
            init_data["color_category"] = {}

        # Parse lines configuration
        lines_obj = visualize.get("lines", {})
        init_data["lines"] = []
        if isinstance(lines_obj, dict):
            for line_name, line_config in lines_obj.items():
                if isinstance(line_config, dict):
                    # Parse symbols
                    symbols_obj = line_config.get("symbols", {})
                    symbols = {
                        "enabled": symbols_obj.get("enabled", False),
                        "shape": symbols_obj.get("shape", "circle"),
                        "style": symbols_obj.get("style", "fill"),
                        "on": symbols_obj.get("on", "last"),
                        "size": symbols_obj.get("size", 6),
                        "opacity": symbols_obj.get("opacity", 1.0),
                    }

                    # Parse value labels
                    value_labels_obj = line_config.get("valueLabels", {})
                    value_labels = {
                        "enabled": value_labels_obj.get("enabled", False),
                        "last": value_labels_obj.get("last", False),
                        "first": value_labels_obj.get("first", False),
                        "show_circles": value_labels_obj.get("showCircles", False),
                        "max_inner_labels": value_labels_obj.get("maxInnerLabels", 0),
                    }

                    init_data["lines"].append(
                        {
                            "column": line_name,  # Add the column name from the dict key
                            "title": line_config.get("title", ""),
                            "interpolation": line_config.get("interpolation", "linear"),
                            "width": line_config.get("width", "style1"),
                            "dash": line_config.get("dash"),
                            "color_key": line_config.get("colorKey", False),
                            "direct_label": line_config.get("directLabel", False),
                            "outline": line_config.get("bgStroke", False),
                            "symbols": symbols,
                            "value_labels": value_labels,
                            "connect_missing_points": line_config.get(
                                "connectMissingPoints", False
                            ),
                        }
                    )

        # Parse area fills
        area_fills_obj = visualize.get("custom-area-fills", {})
        init_data["area_fills"] = []
        if isinstance(area_fills_obj, dict):
            for _fill_id, fill_config in area_fills_obj.items():
                if isinstance(fill_config, dict):
                    init_data["area_fills"].append(
                        {
                            "from_column": fill_config.get("from", ""),
                            "to_column": fill_config.get("to", ""),
                            "color": fill_config.get("color", "#4682b4"),
                            "opacity": fill_config.get("opacity", 0.15),
                            "use_mixed_colors": fill_config.get(
                                "useMixedColors", False
                            ),
                            "color_negative": fill_config.get(
                                "colorNegative", "#E31A1C"
                            ),
                            "interpolation": fill_config.get("interpolation", "linear"),
                        }
                    )

        # Labels
        init_data["stack_color_legend"] = visualize.get("stack-color-legend", False)
        init_data["label_colors"] = visualize.get("label-colors", False)
        init_data["label_margin"] = visualize.get("label-margin", 0)
        init_data["value_labels_format"] = visualize.get("value-labels-format", "")
        init_data["value_label_colors"] = visualize.get("value-label-colors", False)

        # Tooltips
        init_data["show_tooltips"] = visualize.get("show-tooltips", True)
        init_data["tooltip_x_format"] = visualize.get("tooltip-x-format", "")
        init_data["tooltip_number_format"] = visualize.get("tooltip-number-format", "")

        # Appearance
        init_data["plot_height_mode"] = visualize.get("plotHeightMode", "fixed")
        init_data["plot_height_fixed"] = visualize.get("plotHeightFixed", 300)
        init_data["plot_height_ratio"] = visualize.get("plotHeightRatio", 0.5)

        # Annotations - use helper method for deserialization
        init_data["text_annotations"] = cls._deserialize_annotations(
            visualize.get("text-annotations"), TextAnnotation
        )
        init_data["range_annotations"] = cls._deserialize_annotations(
            visualize.get("range-annotations"), RangeAnnotation
        )

        return init_data

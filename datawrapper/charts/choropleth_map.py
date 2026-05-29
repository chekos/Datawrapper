from typing import Any, Literal

import pandas as pd
from pydantic import BaseModel, ConfigDict, Field, model_serializer

from .base import BaseChart
from .enums import BasemapProjection, ColorMode, ColorScale, DateFormat, NumberFormat
from .models import AnnotationsMixin


class Tooltip(BaseModel):
    """Configure tooltips for a Datawrapper choropleth map."""

    model_config = ConfigDict(populate_by_name=True, strict=True)

    #: The tooltip body template
    body: str = Field(
        default="",
        description="The tooltip body template",
    )

    #: The tooltip title template
    title: str = Field(
        default="",
        description="The tooltip title template",
    )

    #: Mapping of field names to custom labels
    fields: dict[str, str] = Field(
        default_factory=dict,
        description="Mapping of field names to custom labels for tooltip display",
    )


class ChoroplethMap(AnnotationsMixin, BaseChart):
    """A base class for the Datawrapper API's choropleth map.

    Choropleth maps visualize data across geographic regions by coloring areas
    based on data values. This class provides a Pythonic interface to create
    and configure choropleth maps using the Datawrapper API.
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
                    "chart-type": "d3-maps-choropleth",
                    "title": "Population by Country",
                    "source_name": "UN Population Division",
                    "data": pd.DataFrame(
                        {
                            "country": ["USA", "CAN", "MEX"],
                            "population": [331000000, 38000000, 128000000],
                        }
                    ),
                    "keys_column": "country",
                    "values_column": "population",
                    "basemap": "world",
                    "map_key_attr": "iso-a3",
                }
            ]
        },
    )

    #: The type of datawrapper chart to create
    chart_type: Literal["d3-maps-choropleth"] = Field(
        default="d3-maps-choropleth",
        alias="chart-type",
        description="The type of datawrapper chart to create",
    )

    #
    # Data Mapping (axes section in API)
    #

    #: The column containing map keys (region identifiers)
    keys_column: str | None = Field(
        default=None,
        alias="keys",
        description="The column containing map keys (e.g., country codes, region names)",
    )

    #: The column containing values to visualize
    values_column: str | None = Field(
        default=None,
        alias="values",
        description="The column containing values to visualize on the map",
    )

    #: The type of the keys column (text or number)
    key_column_type: Literal["text", "number"] | None = Field(
        default=None,
        description="The data type of the keys column. Use 'text' for keys with leading zeros (e.g., postal codes, region IDs)",
    )

    #
    # Basemap Configuration
    #

    #: The basemap ID to use (or "custom_upload" for custom basemaps)
    basemap: str = Field(
        default="",
        description="The basemap ID (e.g., 'world', 'usa-counties') or 'custom_upload' for custom TopoJSON",
    )

    #: The map key attribute to match against your data
    map_key_attr: str = Field(
        default="",
        alias="map-key-attr",
        description="The attribute in the basemap to match against your keys column (e.g., 'iso-a3', 'fips', 'ags)",
    )

    #: The projection for custom basemaps
    basemap_projection: BasemapProjection | str = Field(
        default="geoAzimuthalEqualArea",
        alias="basemapProjection",
        description="The projection to use for custom basemaps",
    )

    #: The topology object name in custom basemaps
    basemap_regions: str = Field(
        default="regions",
        alias="basemapRegions",
        description="The name of the topology object in custom TopoJSON basemaps",
    )

    #
    # Tooltips
    #

    #: Tooltip configuration
    tooltip: Tooltip | dict[str, Any] | None = Field(
        default=None,
        description="Tooltip configuration (body, title, field mappings)",
    )

    #: The format for tooltip values (use DateFormat or NumberFormat enum or custom format strings)
    tooltip_number_format: DateFormat | NumberFormat | str = Field(
        default="",
        alias="tooltip-number-format",
        description="The format for tooltip values. Use DateFormat for temporal data, NumberFormat for numeric data, or custom format strings.",
    )

    #
    # Appearance
    #

    #: Whether to show tooltips on hover
    show_tooltips: bool = Field(
        default=True,
        alias="show-tooltips",
        description="Whether to show tooltips when hovering over regions",
    )

    #
    # Map Interaction & Display
    #

    #: Whether the map is zoomable
    zoomable: bool = Field(
        default=False,
        description="Whether users can zoom and pan the map",
    )

    #: Whether to hide regions without data
    hide_empty_regions: bool = Field(
        default=False,
        alias="hide-empty-regions",
        description="Whether to hide regions that don't have data values",
    )

    #: Whether to hide region borders
    hide_borders: bool = Field(
        default=False,
        alias="hide-borders",
        description="Whether to hide the borders between regions on the map",
    )

    #
    # Color Configuration
    #

    #: Color mode (gradient or buckets)
    color_mode: ColorMode | str | None = Field(
        default=None,
        alias="color-mode",
        description="Color mode: 'gradient' for continuous colors or 'buckets' for discrete intervals",
    )

    #: Number of color buckets/steps
    color_steps: int | None = Field(
        default=None,
        alias="color-steps",
        description="Number of color buckets or steps (typically 3-9)",
    )

    #: Color palette/scheme
    color_palette: str | None = Field(
        default=None,
        alias="color-palette",
        description="Color palette name (e.g., 'Blues', 'RdYlGn', 'Viridis')",
    )

    #: Color scale type
    color_scale: ColorScale | str | None = Field(
        default=None,
        alias="color-scale",
        description="Color scale type: 'linear', 'log', 'sqrt', 'quantile', or 'jenks'",
    )

    #: Minimum color (start of gradient)
    color_from: str | None = Field(
        default=None,
        alias="color-from",
        description="Start color of the gradient (hex color code, e.g., '#ffffff')",
    )

    #: Maximum color (end of gradient)
    color_to: str | None = Field(
        default=None,
        alias="color-to",
        description="End color of the gradient (hex color code, e.g., '#ff0000')",
    )

    #
    # Serialization methods for preparing data for API upload
    #

    @model_serializer
    def serialize_model(self) -> dict:
        """Serialize the model to a dictionary."""
        # Call the parent class's serialize_model method
        model = super().serialize_model()

        # Build the axes section for data mapping
        axes_data = {}
        if self.keys_column is not None:
            axes_data["keys"] = self.keys_column
        if self.values_column is not None:
            axes_data["values"] = self.values_column

        # Only add axes if we have keys or values
        if axes_data:
            model["metadata"]["axes"] = axes_data

        # Handle key_column_type by adding to metadata.data.column-format
        if self.key_column_type is not None and self.keys_column is not None:
            # Ensure data section exists
            if "data" not in model["metadata"]:
                model["metadata"]["data"] = {}

            # Get existing column-format or initialize empty dict
            column_format = model["metadata"]["data"].get("column-format", {})

            # Set the type for the keys column
            if self.keys_column not in column_format:
                column_format[self.keys_column] = {}

            column_format[self.keys_column]["type"] = self.key_column_type

            model["metadata"]["data"]["column-format"] = column_format

        # Build visualize section
        visualize_data: dict[str, Any] = {
            "show-tooltips": self.show_tooltips,
            "tooltip-number-format": self.tooltip_number_format,
            "zoomable": self.zoomable,
            "hide-empty-regions": self.hide_empty_regions,
            "hide-borders": self.hide_borders,
        }

        # Add color configuration
        if self.color_mode is not None:
            visualize_data["color-mode"] = self.color_mode
        if self.color_steps is not None:
            visualize_data["color-steps"] = self.color_steps
        if self.color_palette is not None:
            visualize_data["color-palette"] = self.color_palette
        if self.color_scale is not None:
            visualize_data["color-scale"] = self.color_scale
        if self.color_from is not None:
            visualize_data["color-from"] = self.color_from
        if self.color_to is not None:
            visualize_data["color-to"] = self.color_to

        # Add colorscale object if color configuration is present
        # This is necessary for Datawrapper to actually apply the colors
        if self.color_from is not None and self.color_to is not None:
            # Determine interpolation type based on color_scale
            interpolation = "equidistant"
            if self.color_scale == "quantile":
                interpolation = "equidistant"
            elif self.color_scale == "jenks":
                interpolation = "jenks"

            # Build the colorscale configuration
            colorscale_config: dict[str, Any] = {
                "interpolation": interpolation,
                "stops": "equidistant",
            }

            # IMPORTANT: Set the mode field to match color_mode
            # This is what Datawrapper uses to determine continuous vs buckets display
            if self.color_mode is not None:
                # Map our color_mode enum to Datawrapper's colorscale.mode
                if self.color_mode == ColorMode.BUCKETS or self.color_mode == "buckets":
                    colorscale_config["mode"] = "discrete"
                else:  # gradient
                    colorscale_config["mode"] = "continuous"

            # Add stopCount if color_steps is specified
            if self.color_steps is not None:
                colorscale_config["stopCount"] = self.color_steps

            # Set the start and end colors
            # Datawrapper will interpolate the colors in between
            colorscale_config["colors"] = [
                {"color": self.color_from, "position": 0},
                {"color": self.color_to, "position": 1},
            ]

            visualize_data["colorscale"] = colorscale_config

        # Add basemap configuration
        if self.basemap:
            visualize_data["basemap"] = self.basemap

        if self.map_key_attr:
            visualize_data["map-key-attr"] = self.map_key_attr

        # Add custom basemap settings if using custom upload
        if self.basemap == "custom_upload":
            visualize_data["basemapProjection"] = self.basemap_projection
            visualize_data["basemapRegions"] = self.basemap_regions

        # Add tooltip configuration
        if self.tooltip is not None:
            tooltip_obj = (
                self.tooltip
                if isinstance(self.tooltip, Tooltip)
                else Tooltip.model_validate(self.tooltip)
            )
            tooltip_dict: dict[str, Any] = {
                "body": tooltip_obj.body,
                "title": tooltip_obj.title,
            }
            # Add fields if present
            if tooltip_obj.fields:
                tooltip_dict["fields"] = tooltip_obj.fields
            visualize_data["tooltip"] = tooltip_dict

        # Update the visualize section
        model["metadata"]["visualize"].update(visualize_data)
        model["metadata"]["visualize"].update(self._serialize_annotations())

        return model

    @classmethod
    def deserialize_model(cls, api_response: dict[str, Any]) -> dict[str, Any]:
        """Parse Datawrapper API response including choropleth map specific fields.

        Args:
            api_response: The JSON response from the chart metadata endpoint

        Returns:
            Dictionary that can be used to initialize the ChoroplethMap model
        """
        # Call parent to get base fields
        init_data = super().deserialize_model(api_response)

        # Extract map-specific sections
        metadata = api_response.get("metadata", {})
        axes = metadata.get("axes", {})
        visualize = metadata.get("visualize", {})

        # Data mapping
        if "keys" in axes:
            init_data["keys_column"] = axes["keys"]
        if "values" in axes:
            init_data["values_column"] = axes["values"]

        # Extract key_column_type from metadata.data.column-format
        data_section = metadata.get("data", {})
        column_format = data_section.get("column-format", {})
        # Check if keys_column exists and has a type defined
        if "keys_column" in init_data:
            keys_col = init_data["keys_column"]
            if keys_col in column_format and "type" in column_format[keys_col]:
                col_type = column_format[keys_col]["type"]
                # Only set if it's text or number (not auto)
                if col_type in ["text", "number"]:
                    init_data["key_column_type"] = col_type

        # Basemap configuration
        if "basemap" in visualize:
            init_data["basemap"] = visualize["basemap"]
        if "map-key-attr" in visualize:
            init_data["map_key_attr"] = visualize["map-key-attr"]
        if "basemapProjection" in visualize:
            init_data["basemap_projection"] = visualize["basemapProjection"]
        if "basemapRegions" in visualize:
            init_data["basemap_regions"] = visualize["basemapRegions"]

        # Tooltips
        if "tooltip" in visualize:
            tooltip_data = visualize["tooltip"]
            init_data["tooltip"] = Tooltip.model_validate(tooltip_data)
        if "tooltip-number-format" in visualize:
            init_data["tooltip_number_format"] = visualize["tooltip-number-format"]
        if "show-tooltips" in visualize:
            init_data["show_tooltips"] = visualize["show-tooltips"]

        # Map interaction and display
        if "zoomable" in visualize:
            init_data["zoomable"] = visualize["zoomable"]
        if "hide-empty-regions" in visualize:
            init_data["hide_empty_regions"] = visualize["hide-empty-regions"]
        if "hide-borders" in visualize:
            init_data["hide_borders"] = visualize["hide-borders"]

        # Color configuration
        if "color-mode" in visualize:
            init_data["color_mode"] = visualize["color-mode"]
        if "color-steps" in visualize:
            init_data["color_steps"] = visualize["color-steps"]
        if "color-palette" in visualize:
            init_data["color_palette"] = visualize["color-palette"]
        if "color-scale" in visualize:
            init_data["color_scale"] = visualize["color-scale"]
        if "color-from" in visualize:
            init_data["color_from"] = visualize["color-from"]
        if "color-to" in visualize:
            init_data["color_to"] = visualize["color-to"]

        # Annotations
        init_data.update(cls._deserialize_annotations(visualize))

        return init_data

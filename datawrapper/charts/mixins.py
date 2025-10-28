"""Mixin classes for shared chart visualization patterns."""

from typing import Any

from pydantic import Field

from .enums import DateFormat, GridDisplay, NumberFormat
from .serializers import CustomRange, CustomTicks


class GridDisplayMixin:
    """Mixin for charts that support grid display configuration.

    Provides x_grid and y_grid fields for controlling grid line visibility,
    along with serialization/deserialization methods.

    Default values:
    - x_grid: "off" (no vertical grid lines by default)
    - y_grid: "on" (horizontal grid lines shown by default)

    Supports backwards compatibility with boolean values:
    - True → "on" during serialization
    - False → "off" during serialization
    - API "on" → True during deserialization
    - API "off" → False during deserialization
    """

    x_grid: GridDisplay | str | bool | None = Field(
        default="off",
        description="X-axis grid display setting. Controls vertical grid lines.",
    )
    y_grid: GridDisplay | str | bool | None = Field(
        default="on",
        description="Y-axis grid display setting. Controls horizontal grid lines.",
    )

    def _serialize_grid_config(self) -> dict:
        """Serialize grid configuration to API format.

        Handles conversion of boolean values to "on"/"off" strings for backwards compatibility.

        Returns:
            dict: Grid configuration in API format with keys:
                - x-grid: X-axis grid display setting
                - y-grid: Y-axis grid display setting
        """
        result = {}
        if self.x_grid is not None:
            # Handle boolean values for backwards compatibility
            if isinstance(self.x_grid, bool):
                result["x-grid"] = "on" if self.x_grid else "off"
            elif isinstance(self.x_grid, GridDisplay):
                result["x-grid"] = self.x_grid.value
            else:
                result["x-grid"] = self.x_grid
        if self.y_grid is not None:
            # Handle boolean values for backwards compatibility
            if isinstance(self.y_grid, bool):
                result["y-grid"] = "on" if self.y_grid else "off"
            elif isinstance(self.y_grid, GridDisplay):
                result["y-grid"] = self.y_grid.value
            else:
                result["y-grid"] = self.y_grid
        return result

    @classmethod
    def _deserialize_grid_config(cls, visualize: dict) -> dict:
        """Deserialize grid configuration from API format.

        Preserves original API values without conversion.

        Args:
            visualize: The visualize section from API response

        Returns:
            dict: Grid configuration in Python format with keys:
                - x_grid: X-axis grid display setting (preserves API type)
                - y_grid: Y-axis grid display setting (preserves API type)
        """
        result = {}
        if "x-grid" in visualize:
            result["x_grid"] = visualize["x-grid"]
        if "y-grid" in visualize:
            result["y_grid"] = visualize["y-grid"]
        return result


class GridFormatMixin:
    """Mixin for charts that support grid label formatting.

    Provides x_grid_format and y_grid_format fields for controlling how grid labels
    are displayed, along with serialization/deserialization methods.

    Used by: LineChart, AreaChart, ColumnChart, MultipleColumnChart, ScatterPlot
    """

    x_grid_format: DateFormat | NumberFormat | str | None = Field(
        default=None,
        description="Format string for X-axis grid labels. Supports date and number formats.",
    )
    y_grid_format: NumberFormat | str | None = Field(
        default=None,
        description="Format string for Y-axis grid labels. Supports number formats.",
    )

    def _serialize_grid_format(self) -> dict:
        """Serialize grid format configuration to API format.

        Returns:
            dict: Grid format configuration in API format with keys:
                - x-grid-format: X-axis grid label format
                - y-grid-format: Y-axis grid label format
        """
        result = {}
        if self.x_grid_format is not None:
            result["x-grid-format"] = (
                self.x_grid_format.value
                if isinstance(self.x_grid_format, (DateFormat, NumberFormat))
                else self.x_grid_format
            )
        if self.y_grid_format is not None:
            result["y-grid-format"] = (
                self.y_grid_format.value
                if isinstance(self.y_grid_format, NumberFormat)
                else self.y_grid_format
            )
        return result

    @classmethod
    def _deserialize_grid_format(cls, visualize: dict) -> dict:
        """Deserialize grid format configuration from API format.

        Args:
            visualize: The visualize section from API response

        Returns:
            dict: Grid format configuration in Python format with keys:
                - x_grid_format: X-axis grid label format
                - y_grid_format: Y-axis grid label format
        """
        result = {}
        if "x-grid-format" in visualize:
            result["x_grid_format"] = visualize["x-grid-format"]
        if "y-grid-format" in visualize:
            result["y_grid_format"] = visualize["y-grid-format"]
        return result


class CustomRangeMixin:
    """Mixin for charts that support custom axis ranges.

    Provides custom_range_x and custom_range_y fields for setting explicit min/max
    values for axes, along with serialization/deserialization methods.
    """

    custom_range_x: list[Any] | tuple[Any, Any] | None = Field(
        default=None,
        description="Custom range for X-axis as [min, max]. Overrides automatic range calculation.",
    )
    custom_range_y: list[Any] | tuple[Any, Any] | None = Field(
        default=None,
        description="Custom range for Y-axis as [min, max]. Overrides automatic range calculation.",
    )

    def _serialize_custom_range(self) -> dict:
        """Serialize custom range configuration to API format.

        Returns:
            dict: Custom range configuration in API format with keys:
                - custom-range-x: X-axis custom range [min, max]
                - custom-range-y: Y-axis custom range [min, max]
        """
        result = {}
        if self.custom_range_x is not None:
            result["custom-range-x"] = CustomRange.serialize(self.custom_range_x)
        if self.custom_range_y is not None:
            result["custom-range-y"] = CustomRange.serialize(self.custom_range_y)
        return result

    @classmethod
    def _deserialize_custom_range(cls, visualize: dict) -> dict:
        """Deserialize custom range configuration from API format.

        Args:
            visualize: The visualize section from API response

        Returns:
            dict: Custom range configuration in Python format with keys:
                - custom_range_x: X-axis custom range [min, max]
                - custom_range_y: Y-axis custom range [min, max]
        """
        result = {}
        if "custom-range-x" in visualize:
            result["custom_range_x"] = CustomRange.deserialize(
                visualize["custom-range-x"]
            )
        if "custom-range-y" in visualize:
            result["custom_range_y"] = CustomRange.deserialize(
                visualize["custom-range-y"]
            )
        return result


class CustomTicksMixin:
    """Mixin for charts that support custom tick marks.

    Provides custom_ticks_x and custom_ticks_y fields for setting explicit tick mark
    positions on axes, along with serialization/deserialization methods.
    """

    custom_ticks_x: list[Any] | None = Field(
        default=None,
        description="Custom tick mark positions for X-axis. List of values where ticks should appear.",
    )
    custom_ticks_y: list[Any] | None = Field(
        default=None,
        description="Custom tick mark positions for Y-axis. List of values where ticks should appear.",
    )

    def _serialize_custom_ticks(self) -> dict:
        """Serialize custom ticks configuration to API format.

        Returns:
            dict: Custom ticks configuration in API format with keys:
                - custom-ticks-x: X-axis custom tick positions
                - custom-ticks-y: Y-axis custom tick positions
        """
        result = {}
        if self.custom_ticks_x is not None:
            result["custom-ticks-x"] = CustomTicks.serialize(self.custom_ticks_x)
        if self.custom_ticks_y is not None:
            result["custom-ticks-y"] = CustomTicks.serialize(self.custom_ticks_y)
        return result

    @classmethod
    def _deserialize_custom_ticks(cls, visualize: dict) -> dict:
        """Deserialize custom ticks configuration from API format.

        Args:
            visualize: The visualize section from API response

        Returns:
            dict: Custom ticks configuration in Python format with keys:
                - custom_ticks_x: X-axis custom tick positions
                - custom_ticks_y: Y-axis custom tick positions
        """
        result = {}
        if "custom-ticks-x" in visualize:
            result["custom_ticks_x"] = CustomTicks.deserialize(
                visualize["custom-ticks-x"]
            )
        if "custom-ticks-y" in visualize:
            result["custom_ticks_y"] = CustomTicks.deserialize(
                visualize["custom-ticks-y"]
            )
        return result

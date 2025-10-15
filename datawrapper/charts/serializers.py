"""Serialization utilities for converting between Python objects and Datawrapper API formats."""

from typing import Any


class CustomTicks:
    """Utility class for serializing and deserializing custom tick marks."""

    @staticmethod
    def serialize(ticks: list[Any]) -> str:
        """Convert list of ticks to comma-separated string for API.

        Args:
            ticks: List of tick values (can be numbers, strings, or mixed)

        Returns:
            Comma-separated string representation of ticks

        Example:
            >>> CustomTicks.serialize([0, 10, 20, 30])
            '0,10,20,30'
            >>> CustomTicks.serialize(["2020", "2021", "2022"])
            '2020,2021,2022'
        """
        return ",".join(str(tick) for tick in ticks)

    @staticmethod
    def deserialize(ticks_str: str) -> list[Any]:
        """Parse comma-separated string to list of ticks from API.

        Attempts to convert each tick to a float if possible, otherwise
        keeps it as a string.

        Args:
            ticks_str: Comma-separated string of tick values

        Returns:
            List of tick values (floats or strings)

        Example:
            >>> CustomTicks.deserialize("0,10,20,30")
            [0.0, 10.0, 20.0, 30.0]
            >>> CustomTicks.deserialize("2020,2021,2022")
            ['2020', '2021', '2022']
            >>> CustomTicks.deserialize("")
            []
        """
        if not ticks_str:
            return []

        result: list[Any] = []
        for x in ticks_str.split(","):
            x = x.strip()
            if not x:
                result.append(x)
                continue
            try:
                # Try to convert to float
                num = float(x)
                # If it's a whole number, convert to int
                if num.is_integer():
                    result.append(int(num))
                else:
                    result.append(num)
            except ValueError:
                # Keep as string if conversion fails
                result.append(x)
        return result


class CustomRange:
    """Utility class for serializing and deserializing custom axis ranges."""

    @staticmethod
    def serialize(range_values: list[Any] | tuple[Any, Any]) -> list[Any]:
        """Convert range values to API format.

        Args:
            range_values: List or tuple of [min, max] values

        Returns:
            List of two values for the API

        Example:
            >>> CustomRange.serialize([0, 100])
            [0, 100]
            >>> CustomRange.serialize(["", ""])
            ['', '']
            >>> CustomRange.serialize([0, ""])
            [0, '']
        """
        if not range_values or len(range_values) != 2:
            return ["", ""]

        result = []
        for value in range_values:
            # Keep empty strings as-is
            if value == "":
                result.append("")
            else:
                result.append(value)

        return result

    @staticmethod
    def deserialize(range_values: list[Any] | None) -> list[Any]:
        """Parse range values from API format.

        Attempts to convert numeric strings to numbers, while preserving
        empty strings and non-numeric values.

        Args:
            range_values: List from API response

        Returns:
            List of (min, max) values with proper types

        Example:
            >>> CustomRange.deserialize([0, 100])
            [0, 100]
            >>> CustomRange.deserialize(["0", "100"])
            [0, 100]
            >>> CustomRange.deserialize(["", ""])
            ['', '']
            >>> CustomRange.deserialize([0, ""])
            [0, '']
            >>> CustomRange.deserialize(None)
            ['', '']
        """
        if not range_values or len(range_values) == 0:
            return ["", ""]

        result: list[Any] = []
        for value in range_values:
            # Keep empty strings as-is
            if value == "":
                result.append("")
            # Try to convert strings to numbers
            elif isinstance(value, str):
                try:
                    num = float(value)
                    # If it's a whole number, convert to int
                    if num.is_integer():
                        result.append(int(num))
                    else:
                        result.append(num)
                except ValueError:
                    # Keep as string if conversion fails
                    result.append(value)
            else:
                # Keep numbers and other types as-is
                result.append(value)

        # Pad with empty strings if we have fewer than 2 values
        while len(result) < 2:
            result.append("")

        return result[:2]  # Return only first 2 values


class ColorCategory:
    """Utility class for serializing and deserializing color category structures."""

    @staticmethod
    def serialize(
        color_map: dict[str, str],
        category_labels: dict[str, str] | None = None,
        category_order: list[str] | None = None,
        exclude_from_key: list[str] | None = None,
    ) -> dict[str, Any]:
        """Convert color category data to API format.

        Args:
            color_map: Mapping of layer names to colors
            category_labels: Optional mapping of category names to display labels
            category_order: Optional list defining category order in chart and legend
            exclude_from_key: Optional list of columns to exclude from color key

        Returns:
            Dictionary in API format with 'map' and optional additional fields

        Example:
            >>> ColorCategory.serialize({"A": "#ff0000", "B": "#00ff00"})
            {'map': {'A': '#ff0000', 'B': '#00ff00'}}
            >>> ColorCategory.serialize(
            ...     {"A": "#ff0000"},
            ...     category_labels={"A": "Category A"},
            ...     category_order=["A", "B"],
            ...     exclude_from_key=[],
            ... )
            {'map': {'A': '#ff0000'}, 'excludeFromKey': [], 'categoryLabels': {'A': 'Category A'}, 'categoryOrder': ['A', 'B']}
        """
        result: dict[str, Any] = {"map": color_map}

        # Only include excludeFromKey if explicitly provided (not None)
        if exclude_from_key is not None:
            result["excludeFromKey"] = exclude_from_key

        # Only include category_labels and category_order if they're non-empty
        if category_labels:
            result["categoryLabels"] = category_labels
        if category_order:
            result["categoryOrder"] = category_order

        return result

    @staticmethod
    def deserialize(color_category_obj: dict[str, Any] | None) -> dict[str, Any]:
        """Parse color category data from API format.

        Args:
            color_category_obj: The color-category object from API response

        Returns:
            Dictionary with keys: color_category, category_labels, category_order, exclude_from_color_key

        Example:
            >>> ColorCategory.deserialize({"map": {"A": "#ff0000"}})
            {'color_category': {'A': '#ff0000'}, 'category_labels': {}, 'category_order': [], 'exclude_from_color_key': []}
            >>> ColorCategory.deserialize(None)
            {'color_category': {}, 'category_labels': {}, 'category_order': [], 'exclude_from_color_key': []}
        """
        if not isinstance(color_category_obj, dict):
            return {
                "color_category": {},
                "category_labels": {},
                "category_order": [],
                "exclude_from_color_key": [],
            }

        return {
            "color_category": color_category_obj.get("map", {}),
            "category_labels": color_category_obj.get("categoryLabels", {}),
            "category_order": color_category_obj.get("categoryOrder", []),
            "exclude_from_color_key": color_category_obj.get("excludeFromKey", []),
        }


class ReplaceFlags:
    """Utility class for serializing and deserializing replace-flags configuration.

    The Datawrapper API uses a nested object format for the replace-flags field:
    {
        "enabled": bool,
        "style": str  # "4x3", "1x1", "circle", or ""
    }

    But in our Python models, we use a simpler string format:
    "off", "4x3", "1x1", "circle"

    This utility handles the conversion between these formats.
    """

    @staticmethod
    def serialize(flag_type: str) -> dict[str, Any]:
        """Convert simple string format to API nested object format.

        Args:
            flag_type: The flag type ("off", "4x3", "1x1", "circle")

        Returns:
            Dictionary with "enabled" and "style" keys for the API

        Example:
            >>> ReplaceFlags.serialize("4x3")
            {'enabled': True, 'style': '4x3'}
            >>> ReplaceFlags.serialize("off")
            {'enabled': False, 'style': ''}
        """
        return {
            "enabled": flag_type != "off",
            "style": flag_type if flag_type != "off" else "",
        }

    @staticmethod
    def deserialize(api_obj: dict[str, Any] | None) -> str:
        """Convert API nested object format to simple string format.

        Args:
            api_obj: The API object with "enabled" and "style" keys, or None

        Returns:
            String flag type ("off", "4x3", "1x1", "circle")

        Example:
            >>> ReplaceFlags.deserialize({"enabled": True, "style": "4x3"})
            '4x3'
            >>> ReplaceFlags.deserialize({"enabled": False, "style": ""})
            'off'
            >>> ReplaceFlags.deserialize(None)
            'off'
        """
        if not isinstance(api_obj, dict):
            return "off"

        enabled = api_obj.get("enabled", False)
        flag_type = api_obj.get("style", "")

        # If enabled is False or style is empty, return "off"
        if not enabled or not flag_type:
            return "off"

        return flag_type


class PlotHeight:
    """Utility class for serializing and deserializing plot height configuration.

    The Datawrapper API uses three separate fields for plot height:
    - plotHeightMode: "ratio" or "fixed"
    - plotHeightFixed: numeric value for fixed height
    - plotHeightRatio: numeric value for ratio height

    This utility provides convenience methods to serialize and deserialize
    these related fields together.
    """

    @staticmethod
    def serialize(mode: str, fixed: int | float, ratio: float) -> dict[str, Any]:
        """Convert plot height fields to API format.

        Args:
            mode: The height mode ("ratio" or "fixed")
            fixed: The fixed height value
            ratio: The ratio height value

        Returns:
            Dictionary with plotHeightMode, plotHeightFixed, and plotHeightRatio keys

        Example:
            >>> PlotHeight.serialize("fixed", 400, 0.5)
            {'plotHeightMode': 'fixed', 'plotHeightFixed': 400, 'plotHeightRatio': 0.5}
            >>> PlotHeight.serialize("ratio", 300, 0.75)
            {'plotHeightMode': 'ratio', 'plotHeightFixed': 300, 'plotHeightRatio': 0.75}
        """
        return {
            "plotHeightMode": mode,
            "plotHeightFixed": fixed,
            "plotHeightRatio": ratio,
        }

    @staticmethod
    def deserialize(visualize: dict[str, Any]) -> dict[str, Any]:
        """Extract plot height fields from API response.

        Args:
            visualize: The visualize section of the API response

        Returns:
            Dictionary with plot_height_mode, plot_height_fixed, and plot_height_ratio keys
            (only includes keys that are present in the API response)

        Example:
            >>> PlotHeight.deserialize(
            ...     {"plotHeightMode": "fixed", "plotHeightFixed": 400}
            ... )
            {'plot_height_mode': 'fixed', 'plot_height_fixed': 400}
            >>> PlotHeight.deserialize({})
            {}
        """
        result: dict[str, Any] = {}

        if "plotHeightMode" in visualize:
            result["plot_height_mode"] = visualize["plotHeightMode"]
        if "plotHeightFixed" in visualize:
            result["plot_height_fixed"] = visualize["plotHeightFixed"]
        if "plotHeightRatio" in visualize:
            result["plot_height_ratio"] = visualize["plotHeightRatio"]

        return result


class ModelListSerializer:
    """Utility class for serializing lists of model objects to API format."""

    @staticmethod
    def serialize(
        items: list[Any],
        model_class: type[Any],
    ) -> list[dict[str, Any]]:
        """Serialize a list of model objects to API format.

        This utility handles converting a list of model objects (or dicts) into
        the list of dictionaries format expected by the Datawrapper API.

        Args:
            items: List of model objects or dicts
            model_class: The model class (e.g., TextAnnotation, RangeAnnotation, AreaFill)

        Returns:
            List of serialized dictionaries

        Example:
            >>> from datawrapper.charts.annos import TextAnnotation
            >>> annotations = [
            ...     TextAnnotation(x=0, y=0, text="Label 1"),
            ...     {"x": 1, "y": 1, "text": "Label 2"},
            ... ]
            >>> ModelListSerializer.serialize(annotations, TextAnnotation)
            [{'x': 0, 'y': 0, 'text': 'Label 1', ...}, {'x': 1, 'y': 1, 'text': 'Label 2', ...}]
        """
        result: list[Any] = []
        for item in items:
            # Convert to model object if needed
            if isinstance(item, dict):
                obj = model_class.model_validate(item)
            else:
                obj = item

            # Serialize the object using its serialize_model method
            result.append(obj.serialize_model())

        return result

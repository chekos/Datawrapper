from typing import Any


class NegativeColor:
    """Utility class for serializing and deserializing negative color configuration.

    The Datawrapper API uses a nested object format for the negativeColor field:
    {
        "enabled": bool,
        "value": str  # hex color code like "#E31A1C"
    }

    But in our Python models, we use a simpler optional string format:
    - None = disabled
    - "#E31A1C" or any color string = enabled with that color

    This utility handles the conversion between these formats.
    """

    @staticmethod
    def serialize(color: str | None) -> dict[str, Any]:
        """Convert optional color string to API nested object format.

        Args:
            color: The color value (None for disabled, color string for enabled)

        Returns:
            Dictionary with "enabled" and "value" keys for the API

        Example:
            >>> NegativeColor.serialize("#FF0000")
            {'enabled': True, 'value': '#FF0000'}
            >>> NegativeColor.serialize(None)
            {'enabled': False, 'value': ''}
        """
        return {
            "value": color if color else "",
            "enabled": color is not None,
        }

    @staticmethod
    def deserialize(api_obj: dict[str, Any] | None) -> str | None:
        """Convert API nested object format to optional color string.

        Args:
            api_obj: The API object with "enabled" and "value" keys, or None

        Returns:
            Color string if enabled, None if disabled

        Example:
            >>> NegativeColor.deserialize({"enabled": True, "value": "#FF0000"})
            '#FF0000'
            >>> NegativeColor.deserialize({"enabled": False, "value": "#E31A1C"})
            None
            >>> NegativeColor.deserialize(None)
            None
        """
        if not isinstance(api_obj, dict):
            return None

        enabled = api_obj.get("enabled", False)
        color_value = api_obj.get("value", "")

        return color_value if enabled else None

from typing import Any


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

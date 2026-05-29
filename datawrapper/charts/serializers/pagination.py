from typing import Any

from .base import BaseSerializer


class Pagination(BaseSerializer):
    """Utility class for serializing and deserializing pagination configuration.

    The Datawrapper API uses a nested object format for the pagination field:
    {
        "enabled": bool,
        "position": str  # "top", "bottom", "both"
    }

    But in our Python models, we use a simpler string format:
    "off", "top", "bottom", "both", or ""

    This utility handles the conversion between these formats.
    """

    @staticmethod
    def serialize(pagination_type: str) -> dict[str, Any]:
        """Convert simple string format to API nested object format.

        Args:
            pagination_type: The pagination type ("off", "top", "bottom", "both")

        Returns:
            Dictionary with "enabled" and "position" keys for the API

        Example:
            >>> Pagination.serialize("top")
            {'enabled': True, 'position': 'top'}
            >>> Pagination.serialize("off")
            {'enabled': False, 'position': ''}
        """
        return {
            "enabled": pagination_type != "off",
            "position": pagination_type if pagination_type != "off" else "",
        }

    @staticmethod
    def deserialize(api_obj: dict[str, Any] | None) -> str:
        """Convert API nested object format to simple string format.

        Args:
            api_obj: The API object with "enabled" and "position" keys, or None

        Returns:
            String pagination type ("off", "top", "bottom", "both")

        Example:
            >>> Pagination.deserialize({"enabled": True, "position": "top"})
            'top'
            >>> Pagination.deserialize({"enabled": False, "position": ""})
            'off'
            >>> Pagination.deserialize(None)
            'off'
        """
        if not isinstance(api_obj, dict):
            return "off"

        enabled = api_obj.get("enabled", False)
        pagination_type = api_obj.get("position", "")

        # If enabled is False or position is empty, return "off"
        if not enabled or not pagination_type:
            return "off"

        return pagination_type

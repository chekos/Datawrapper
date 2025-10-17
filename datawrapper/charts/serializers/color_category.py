from typing import Any


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

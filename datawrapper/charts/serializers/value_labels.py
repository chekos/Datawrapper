from typing import Any


class ValueLabels:
    """Utility class for serializing and deserializing value label configuration.

    Different chart types use different API formats for value labels:
    - BarChart: Flat structure with show-value-labels (bool), value-label-format, value-label-alignment
    - ColumnChart/MultipleColumnChart: Nested valueLabels object with show, format, enabled, placement
    - LineChart/ArrowChart/StackedBarChart: Simple value-labels-format or value-label-format field

    This utility provides a consistent interface for handling these variations.
    """

    @staticmethod
    def serialize(
        show: str | bool,
        format_str: str = "",
        placement: str | None = None,
        alignment: str | None = None,
        always: bool | None = None,
        chart_type: str = "column",
    ) -> dict[str, Any]:
        """Convert Python value label config to API format.

        Args:
            show: Whether to show labels ("hover", "always", "off") or bool
            format_str: Number format string
            placement: Where to place labels ("inside", "outside", "below") - for column charts
            alignment: Label alignment ("left", "right") - for bar charts
            always: Whether labels are always shown (value-labels-always field) - for column charts
                   If None, will be derived from show parameter for column charts
            chart_type: Type of chart ("column", "multiple-column", "bar", "line", "arrow", "stacked-bar")

        Returns:
            Dictionary in appropriate API format for the chart type (with None values filtered out)

        Example:
            >>> ValueLabels.serialize(
            ...     "hover", "", placement="outside", always=False, chart_type="column"
            ... )
            {'valueLabels': {'show': 'hover', 'format': '', 'enabled': True, 'placement': 'outside'}}
            >>> ValueLabels.serialize(
            ...     "always",
            ...     "0.0a",
            ...     placement="outside",
            ...     always=True,
            ...     chart_type="column",
            ... )
            {'valueLabels': {'show': 'always', 'format': '0.0a', 'enabled': True, 'placement': 'outside'}, 'value-label-format': '0.0a', 'value-labels-always': True}
            >>> ValueLabels.serialize(True, "0.0a", alignment="left", chart_type="bar")
            {'show-value-labels': True, 'value-label-format': '0.0a', 'value-label-alignment': 'left'}
        """
        result: dict[str, Any]

        if chart_type == "bar":
            # BarChart uses flat structure
            result = {
                "show-value-labels": show if isinstance(show, bool) else show != "off",
                "value-label-format": format_str,
                "value-label-alignment": alignment or "left",
            }
        elif chart_type in ["column", "multiple-column"]:
            # Column charts use nested valueLabels object PLUS optional top-level fields
            # The enabled field in valueLabels controls on/off (True for hover or always, False for off)
            # The separate value-labels-always field controls hover vs always behavior

            # Derive always from show if not explicitly provided
            if always is None:
                always = show == "always"

            result = {
                "valueLabels": {
                    "show": show if show != "off" else "",
                    "format": format_str,
                    "enabled": show != "off",  # True for hover or always, False for off
                    "placement": placement or "outside",
                }
            }

            # Only include optional top-level fields when they have meaningful values
            # Note: We check for truthiness, not just None, to exclude empty strings
            if format_str:
                result["value-label-format"] = format_str
            # Include value-labels-always only when it's True (derived or explicit)
            if always is True:
                result["value-labels-always"] = always
        else:
            # Line, Arrow, StackedBar use simple format field
            result = {
                "value-label-format": format_str,
            }

        # Filter out None and empty string values from top-level only
        # Keep nested objects (like valueLabels) intact
        return {
            k: v
            for k, v in result.items()
            if v is not None and (isinstance(v, dict) or v != "")
        }

    @staticmethod
    def deserialize(
        api_obj: dict[str, Any], chart_type: str = "column"
    ) -> dict[str, Any]:
        """Convert API value label config to Python format.

        Args:
            api_obj: The API response object containing value label config
            chart_type: Type of chart being deserialized

        Returns:
            Dictionary with standardized Python field names

        Example:
            >>> ValueLabels.deserialize(
            ...     {
            ...         "valueLabels": {
            ...             "show": "always",
            ...             "format": "0.0a",
            ...             "enabled": True,
            ...             "placement": "outside",
            ...         }
            ...     },
            ...     chart_type="column",
            ... )
            {'show_value_labels': 'always', 'value_labels_format': '0.0a', 'value_labels_placement': 'outside', 'value_labels_always': True}
        """
        result: dict[str, Any] = {}

        if chart_type == "bar":
            # BarChart flat structure
            if "show-value-labels" in api_obj:
                result["show_value_labels"] = api_obj["show-value-labels"]
            if "value-label-format" in api_obj:
                result["value_labels_format"] = api_obj["value-label-format"]
            if "value-label-alignment" in api_obj:
                result["value_labels_alignment"] = api_obj["value-label-alignment"]

        elif chart_type in ["column", "multiple-column"]:
            # Column charts nested structure
            value_labels_obj = api_obj.get("valueLabels", {})

            # The "enabled" field is the master on/off switch - if it's false, labels are off
            # regardless of what "show" says
            enabled = (
                value_labels_obj.get("enabled", True)
                if isinstance(value_labels_obj, dict)
                else True
            )

            if not enabled:
                show = "off"
            elif isinstance(value_labels_obj, dict) and "show" in value_labels_obj:
                # The "show" field is the source of truth when enabled is true
                # It can be "always", "hover", or "" (empty string for off)
                api_show = value_labels_obj.get("show", "")
                if api_show == "always":
                    show = "always"
                elif api_show == "hover":
                    show = "hover"
                else:
                    # Empty string or any other value means off
                    show = "off"
            else:
                # Fallback: derive from value-labels-always field
                always = api_obj.get("value-labels-always", False)

                if always:
                    show = "always"
                else:
                    show = "hover"

            result["show_value_labels"] = show

            # Always include format and placement
            if isinstance(value_labels_obj, dict):
                result["value_labels_format"] = value_labels_obj.get("format", "")
                result["value_labels_placement"] = value_labels_obj.get(
                    "placement", "outside"
                )
            else:
                result["value_labels_format"] = ""
                result["value_labels_placement"] = "outside"

            # Derive value_labels_always from show mode
            result["value_labels_always"] = show == "always"

        else:
            # Simple format field (line, arrow, stacked-bar)
            if "value-label-format" in api_obj:
                result["value_labels_format"] = api_obj["value-label-format"]
            elif "value-labels-format" in api_obj:
                result["value_labels_format"] = api_obj["value-labels-format"]

        return result

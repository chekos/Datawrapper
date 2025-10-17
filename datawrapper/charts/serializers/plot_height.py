from typing import Any


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

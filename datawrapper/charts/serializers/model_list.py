from typing import Any


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

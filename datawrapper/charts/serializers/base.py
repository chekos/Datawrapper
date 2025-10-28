"""Base serializer class for all serialization utilities."""

from abc import ABC, abstractmethod
from typing import Any


class BaseSerializer(ABC):
    """Abstract base class for serialization utilities.

    This class defines the standard interface that all serializer utilities
    should implement. It provides a consistent pattern for converting between
    Python objects and Datawrapper API JSON formats.

    All serializer classes should inherit from this base class and implement
    the serialize() and deserialize() methods.

    Example:
        >>> class CustomRange(BaseSerializer):
        ...     @staticmethod
        ...     def serialize(range_values: list[Any] | tuple[Any, Any]) -> list[Any]:
        ...         # Implementation here
        ...         pass
        ...
        ...     @staticmethod
        ...     def deserialize(range_list: list[Any] | None) -> list[Any] | None:
        ...         # Implementation here
        ...         pass
    """

    @staticmethod
    @abstractmethod
    def serialize(*args: Any, **kwargs: Any) -> Any:
        """Convert Python objects to Datawrapper API format.

        This method should be implemented by subclasses to handle the
        conversion from Python objects to the format expected by the
        Datawrapper API.

        Args:
            *args: Positional arguments specific to the serializer
            **kwargs: Keyword arguments specific to the serializer

        Returns:
            Any: The serialized data in API format

        Raises:
            NotImplementedError: If not implemented by subclass
        """
        raise NotImplementedError("Subclasses must implement serialize()")

    @staticmethod
    @abstractmethod
    def deserialize(*args: Any, **kwargs: Any) -> Any:
        """Convert Datawrapper API format to Python objects.

        This method should be implemented by subclasses to handle the
        conversion from the Datawrapper API format to Python objects.

        Args:
            *args: Positional arguments specific to the serializer
            **kwargs: Keyword arguments specific to the serializer

        Returns:
            Any: The deserialized data as Python objects

        Raises:
            NotImplementedError: If not implemented by subclass
        """
        raise NotImplementedError("Subclasses must implement deserialize()")

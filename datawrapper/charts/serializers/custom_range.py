from typing import Any


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

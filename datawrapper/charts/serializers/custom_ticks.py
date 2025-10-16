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

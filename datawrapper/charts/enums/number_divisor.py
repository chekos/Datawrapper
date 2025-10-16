from enum import Enum


class NumberDivisor(str, Enum):
    """Number divisor options for formatting numbers in charts.

    These values control how numbers are scaled in chart displays:
    - Positive values divide the number (e.g., 3 = divide by 1000)
    - Negative values multiply the number (e.g., -2 = multiply by 100)
    - "0" or 0 means no change
    - "auto" lets Datawrapper auto-detect the best divisor

    Examples:
        >>> # Using enum (recommended - more readable)
        >>> ColumnFormat(column="sales", number_divisor=NumberDivisor.DIVIDE_BY_MILLION)

        >>> # Using raw API values (also supported)
        >>> ColumnFormat(column="sales", number_divisor=6)
        >>> ColumnFormat(column="sales", number_divisor="auto")
    """

    NO_CHANGE = "0"
    AUTO_DETECT = "auto"
    DIVIDE_BY_THOUSAND = "3"
    DIVIDE_BY_MILLION = "6"
    DIVIDE_BY_BILLION = "9"
    MULTIPLY_BY_HUNDRED = "-2"
    MULTIPLY_BY_THOUSAND = "-3"
    MULTIPLY_BY_MILLION = "-6"
    MULTIPLY_BY_BILLION = "-9"
    MULTIPLY_BY_TRILLION = "-12"

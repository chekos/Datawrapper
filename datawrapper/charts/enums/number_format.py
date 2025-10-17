from enum import Enum


class NumberFormat(str, Enum):
    """Number format options for displaying values in charts.

    These values control how numbers are formatted in chart displays, following
    the Datawrapper number format patterns. Custom formats not in this enum can
    be provided as raw strings.

    Format Pattern Guide:
    - 0 = Required digit (shows 0 if no digit)
    - [0] = Optional digit (hidden if 0)
    - , = Thousands separator
    - . = Decimal point
    - % = Percentage sign
    - a = Abbreviated (k, m, b)
    - o = Ordinal suffix (st, nd, rd, th)
    - + = Show plus sign for positive values
    - () = Show negative values in parentheses
    - | = Absolute value (remove minus sign)
    - $ = Currency symbol (locale-dependent)
    - e+0 = Scientific notation

    Examples:
        >>> # Using enum (recommended - more readable)
        >>> chart.y_grid_format = NumberFormat.THOUSANDS_SEPARATOR
        >>> chart.value_labels_format = NumberFormat.PERCENT_TWO_DECIMALS

        >>> # Advanced formats for percent changes
        >>> chart.value_labels_format = (
        ...     NumberFormat.PLUS_SIGN_PERCENT
        ... )  # Shows "+7%" or "-7%"

        >>> # Currency with abbreviation
        >>> chart.y_grid_format = NumberFormat.CURRENCY_ABBREVIATED  # Shows "$1.3m"

        >>> # Using raw format strings (also supported for custom formats)
        >>> chart.y_grid_format = "0,0.00"
        >>> chart.value_labels_format = "$0.[00]a"

    Note:
        The $ currency symbol is locale-dependent. For example, it becomes £ for
        en-UK locale or € for de-DE locale. Use custom prepend/append in
        ColumnFormat for specific currency symbols.

    See: https://academy.datawrapper.de/article/207-custom-number-formats-that-you-can-display-in-datawrapper
    """

    # Basic formats
    AUTO = "auto"
    THOUSANDS_WITH_OPTIONAL_DECIMALS = "0,0.[00]"
    INTEGER = "0"
    ONE_DECIMAL = "0.0"
    TWO_DECIMALS = "0.00"
    THREE_DECIMALS = "0.000"
    UP_TO_ONE_DECIMAL = "0.[0]"
    UP_TO_TWO_DECIMALS = "0.[00]"

    # Percentage formats
    PERCENT_INTEGER = "0%"
    PERCENT_ONE_DECIMAL = "0.0%"
    PERCENT_TWO_DECIMALS = "0.00%"
    PERCENT_UP_TO_ONE_DECIMAL = "0.[0]%"
    PERCENT_UP_TO_TWO_DECIMALS = "0.[00]%"

    # Thousands separator and special formats
    THOUSANDS_SEPARATOR = "0,0"
    ORDINAL = "0o"

    # Abbreviated formats
    ABBREVIATED = "0a"
    ABBREVIATED_ONE_DECIMAL = "0.[0]a"
    ABBREVIATED_TWO_DECIMALS = "0.[00]a"
    ABBREVIATED_THREE_DECIMALS = "0.[000] a"

    # Sign display formats
    PLUS_SIGN = "+0"
    PLUS_SIGN_PERCENT = "+0%"

    # Currency formats (locale-dependent $ symbol)
    CURRENCY_ABBREVIATED_WITH_PLUS = "+$0.[00]a"
    CURRENCY_ABBREVIATED = "$0.[00]a"
    CURRENCY_OPTIONAL_DECIMALS = "$0.[00]"

    # Special formatting
    ZERO_PADDED = "0000"
    PARENTHESES_FOR_NEGATIVES = "(0,0.00)"
    LEADING_DECIMAL = ".000"

    # Scientific notation
    SCIENTIFIC_NOTATION = "0,0e+0"
    SCIENTIFIC_NOTATION_DECIMALS = "0.[00]e+0"

    # Absolute value
    ABSOLUTE_VALUE = "|0.0|"

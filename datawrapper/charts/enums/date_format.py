from enum import Enum


class DateFormat(str, Enum):
    """Date format options for displaying dates in charts.

    These values control how dates are formatted in chart displays, following
    the Datawrapper date format patterns. Custom formats not in this enum can
    be provided as raw strings.

    Format Token Reference:

    **Year Tokens:**
    - YYYY = Full year (2015, 2016, 2024)
    - YY = Two-digit year (15, 16, 24)
    - 'YY = Abbreviated year with apostrophe ('15, '16, '24)

    **Quarter Tokens:**
    - Q = Quarter number (1, 2, 3, 4)
    - [Q] = Literal "Q" text (use with Q for "Q1", "Q2", etc.)

    **Month Tokens:**
    - MMMM = Full month name (January, February, March)
    - MMM = Abbreviated month name (Jan, Feb, Mar)
    - MM = Month number with leading zero (01, 02, 03, ..., 12)
    - M = Month number (1, 2, 3, ..., 12)

    **Week Tokens:**
    - ww = Week of year with leading zero (01, 02, ..., 52)
    - w = Week of year (1, 2, ..., 52)
    - wo = Week of year ordinal (1st, 2nd, ..., 52nd)

    **Day of Month Tokens:**
    - DD = Day with leading zero (01, 02, ..., 31)
    - D = Day (1, 2, ..., 31)
    - Do = Day ordinal (1st, 2nd, 3rd, ..., 31st)

    **Day of Week Tokens:**
    - dddd = Full day name (Sunday, Monday, Tuesday)
    - ddd = Short day name (Sun, Mon, Tue)
    - dd = Abbreviated day name (Su, Mo, Tu)
    - d = Day of week number (0=Sunday, 1=Monday, ..., 6=Saturday)

    **Time Tokens:**
    - HH = Hour 0-23 with leading zero (00, 01, ..., 23)
    - H = Hour 0-23 (0, 1, ..., 23)
    - hh = Hour 1-12 with leading zero (01, 02, ..., 12)
    - h = Hour 1-12 (1, 2, ..., 12)
    - kk = Hour 1-24 with leading zero (01, 02, ..., 24)
    - k = Hour 1-24 (1, 2, ..., 24)
    - mm = Minute with leading zero (00, 01, ..., 59)
    - m = Minute (0, 1, ..., 59)
    - ss = Second with leading zero (00, 01, ..., 59)
    - s = Second (0, 1, ..., 59)
    - SSS = Millisecond (000, 001, ..., 999)
    - A = AM/PM uppercase (AM, PM)
    - a = am/pm lowercase (am, pm)

    **Timezone Tokens:**
    - Z = Timezone offset with colon (-07:00, +05:30)
    - ZZ = Timezone offset without colon (-0700, +0530)

    **Unix Timestamp Tokens:**
    - X = Unix timestamp in seconds (1234567890)
    - x = Unix timestamp in milliseconds (1234567890123)

    **Special Syntax:**
    - ~~ = Different format for first tick (e.g., "YYYY~~'YY" shows "2015, '16, '17")
    - | = Multi-line separator (text after | on line 1, before | on line 2)
    - B = Sport season abbreviated ('15-'16, '16-'17)
    - BB = Sport season full (2015-16, 2016-17)

    **Locale-Dependent Tokens:**
    - L = Short date (1/30/2024 in en-US, 30.1.2024 in de-DE)
    - LL = Long date (January 30, 2024 in en-US, 30. Januar 2024 in de-DE)
    - LLL = Short datetime with time
    - LLLL = Long datetime with time
    - LT = Time (8:30 AM in en-US, 08:30 in de-DE)

    Examples:
        >>> # Using enum (recommended - more readable)
        >>> chart.x_grid_format = DateFormat.YEAR_FULL  # "2024"
        >>> chart.x_grid_format = DateFormat.MONTH_ABBREVIATED_WITH_YEAR  # "Jan '24"
        >>> chart.x_grid_format = DateFormat.DAY_PADDED  # "01", "02", "03"

        >>> # Building block tokens for custom combinations
        >>> chart.x_grid_format = DateFormat.MONTH_NUMBER_PADDED  # "01", "02", "12"
        >>> chart.x_grid_format = DateFormat.DAY_OF_WEEK_FULL  # "Monday", "Tuesday"
        >>> chart.x_grid_format = DateFormat.HOUR_24_PADDED  # "00", "01", "23"

        >>> # Multi-line formats
        >>> chart.x_grid_format = (
        ...     DateFormat.YEAR_MONTH_MULTILINE
        ... )  # "2024" on line 2, "Jan" on line 1

        >>> # First tick different
        >>> chart.x_grid_format = DateFormat.YEAR_ABBREVIATED_FIRST  # "2024, '25, '26"

        >>> # Using raw format strings for custom combinations
        >>> chart.x_grid_format = "YYYY-MM-DD"  # "2024-01-30"
        >>> chart.x_grid_format = "MMM D, YYYY"  # "Jan 30, 2024"
        >>> chart.x_grid_format = "dddd, MMMM D"  # "Monday, January 30"
        >>> chart.x_grid_format = "HH:mm:ss"  # "14:30:45"

    Note:
        Locale-dependent formats (L, LL, LLL, LLLL, LT) change based on the
        chart's output locale setting. The $ currency symbol in NumberFormat
        also changes based on locale.

    See: https://academy.datawrapper.de/article/199-custom-date-formats-that-you-can-display-in-datawrapper
    """

    # Basic/Auto
    AUTO = "auto"

    # Year formats
    YEAR_FULL = "YYYY"
    YEAR_TWO_DIGIT = "YY"
    YEAR_ABBREVIATED = "'YY"
    YEAR_ABBREVIATED_FIRST = "YYYY~~'YY"

    # Quarter formats
    QUARTER = "Q"
    YEAR_QUARTER = "YYYY [Q]Q"
    YEAR_QUARTER_MULTILINE = "YYYY|[Q]Q"

    # Month formats
    MONTH_FULL = "MMMM"
    MONTH_ABBREVIATED = "MMM"
    MONTH_NUMBER_PADDED = "MM"
    MONTH_NUMBER = "M"
    MONTH_ABBREVIATED_WITH_YEAR = "MMM 'YY"
    YEAR_MONTH_MULTILINE = "YYYY|MMM"

    # Week formats
    WEEK_OF_YEAR_PADDED = "ww"
    WEEK_OF_YEAR = "w"
    WEEK_OF_YEAR_ORDINAL = "wo"

    # Day of month formats
    DAY_PADDED = "DD"
    DAY = "D"
    DAY_ORDINAL = "Do"
    MONTH_DAY_MULTILINE = "MMM|DD"
    MONTH_DAY_YEAR_FULL = "MMMM D, YYYY"

    # Day of week formats
    DAY_OF_WEEK_FULL = "dddd"
    DAY_OF_WEEK_SHORT = "ddd"
    DAY_OF_WEEK_MIN = "dd"
    DAY_OF_WEEK_NUMBER = "d"

    # Sport season formats
    SPORT_SEASON_FULL = "BB"
    SPORT_SEASON_ABBREVIATED = "B"

    # Time formats
    HOUR_24_PADDED = "HH"
    HOUR_24 = "H"
    HOUR_12_PADDED = "hh"
    HOUR_12 = "h"
    HOUR_24_ALT_PADDED = "kk"
    HOUR_24_ALT = "k"
    MINUTE_PADDED = "mm"
    MINUTE = "m"
    SECOND_PADDED = "ss"
    SECOND = "s"
    MILLISECOND = "SSS"
    AM_PM_UPPER = "A"
    AM_PM_LOWER = "a"

    # Timezone formats
    TIMEZONE_OFFSET = "Z"
    TIMEZONE_OFFSET_NO_COLON = "ZZ"

    # Unix timestamp formats
    UNIX_TIMESTAMP_SECONDS = "X"
    UNIX_TIMESTAMP_MILLISECONDS = "x"

    # Localized formats (change based on output locale)
    LOCALE_DATE_SHORT = "L"
    LOCALE_DATE_LONG = "LL"
    LOCALE_DATETIME_SHORT = "LLL"
    LOCALE_DATETIME_LONG = "LLLL"
    LOCALE_TIME = "LT"

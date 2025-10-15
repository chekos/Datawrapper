"""Pydantic models for Datawrapper API metadata structures."""

from enum import Enum
from typing import Any, Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_serializer,
    model_validator,
)


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


class LineWidth(str, Enum):
    """Line width options for line charts.

    These values control the stroke width of lines in charts:
    - THINNEST (style0) = 1px stroke width
    - THIN (style1) = 2px stroke width (default)
    - MEDIUM (style2) = 3px stroke width
    - THICK (style3) = 4px stroke width
    - INVISIBLE = hidden line

    Examples:
        >>> # Using enum (recommended - more readable)
        >>> Line(column="sales", width=LineWidth.THICK)

        >>> # Using raw API values (also supported for backwards compatibility)
        >>> Line(column="sales", width="style3")
    """

    THINNEST = "style0"
    THIN = "style1"
    MEDIUM = "style2"
    THICK = "style3"
    INVISIBLE = "invisible"


class LineDash(str, Enum):
    """Line dash pattern options for line charts.

    These values control the dash pattern of lines in charts:
    - SOLID (style1) = No dashes (default)
    - SHORT_DASH (style2) = Short dashes (2.3,2 pattern)
    - MEDIUM_DASH (style3) = Medium dashes (5,3 pattern)
    - LONG_DASH (style4) = Long dashes (7.5,3 pattern)

    Examples:
        >>> # Using enum (recommended - more readable)
        >>> Line(column="sales", dash=LineDash.MEDIUM_DASH)

        >>> # Using raw API values (also supported for backwards compatibility)
        >>> Line(column="sales", dash="style3")
    """

    SOLID = "style1"
    SHORT_DASH = "style2"
    MEDIUM_DASH = "style3"
    LONG_DASH = "style4"


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
        >>> chart.value_labels_format = NumberFormat.PLUS_SIGN_PERCENT  # Shows "+7%" or "-7%"

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
        >>> chart.x_grid_format = DateFormat.YEAR_MONTH_MULTILINE  # "2024" on line 2, "Jan" on line 1

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


class Annotate(BaseModel):
    """A data class for the Datawrapper API's 'annotate' attribute."""

    model_config = ConfigDict(
        populate_by_name=True,
        strict=True,
        json_schema_extra={"examples": [{"notes": "Example note"}]},
    )

    #: The footnotes that appear below the chart
    notes: str = Field(
        default="",
        description="The footnotes that appear below the chart",
    )


class Sharing(BaseModel):
    """A data class for the Datawrapper API's 'sharing' attribute."""

    model_config = ConfigDict(
        populate_by_name=True,
        strict=True,
    )

    #: Whether to show social media share buttons
    enabled: bool = Field(
        default=False,
        description="Whether to show social media share buttons",
    )

    #: What URL to share
    url: str = Field(
        default="",
        description="What URL to share",
    )

    #: Auto-sharing setting
    auto: bool = Field(
        default=False,
        description="Auto-sharing setting",
    )


class Visualize(BaseModel):
    """A data class for the Datawrapper API's 'visualize' attribute."""

    model_config = ConfigDict(
        populate_by_name=True,
        strict=True,
    )

    #: Whether to invert colors in dark mode
    dark_mode_invert: bool = Field(
        default=True,
        alias="dark-mode-invert",
        description="Whether to invert colors in dark mode",
    )

    #: Sharing settings
    sharing: Sharing = Field(
        default_factory=Sharing,
        description="Sharing settings",
    )


class Logo(BaseModel):
    """A data class for the Datawrapper API's 'logo' attribute."""

    model_config = ConfigDict(
        populate_by_name=True,
        strict=True,
    )

    #: The id of the logo to show
    id: str = Field(
        default="",
        description="The id of the logo to show",
    )

    #: Whether to show a logo
    enabled: bool = Field(
        default=False,
        description="Whether to show a logo",
    )


class PublishBlocks(BaseModel):
    """A data class for the Datawrapper API's 'publish blocks' attribute."""

    model_config = ConfigDict(
        populate_by_name=True,
        strict=True,
    )

    #: Whether to allow data downloads
    get_the_data: bool = Field(
        default=False,
        alias="get-the-data",
        description="Whether to allow data downloads",
    )

    #: Whether to allow PNG download
    download_image: bool = Field(
        default=False,
        alias="download-image",
        description="Whether to allow PNG download",
    )

    #: Whether to allow PDF download
    download_pdf: bool = Field(
        default=False,
        alias="download-pdf",
        description="Whether to allow PDF download",
    )

    #: Whether to allow SVG download
    download_svg: bool = Field(
        default=False,
        alias="download-svg",
        description="Whether to allow SVG download",
    )

    #: Whether to allow embedding
    embed: bool = Field(
        default=False,
        description="Whether to allow embedding",
    )

    #: Logo settings
    logo: Logo = Field(
        default_factory=Logo,
        description="Logo settings",
    )


class Publish(BaseModel):
    """A data class for the Datawrapper API's 'publish' attribute."""

    model_config = ConfigDict(
        populate_by_name=True,
        strict=True,
    )

    #: Whether the chart should automatically flip to dark mode
    auto_dark_mode: bool = Field(
        default=False,
        alias="autoDarkMode",
        description="Whether the chart should automatically flip to dark mode",
    )

    #: Whether to attribute the chart to datawrapper
    force_attribution: bool = Field(
        default=False,
        alias="force-attribution",
        description="Whether to attribute the chart to datawrapper",
    )

    #: Publish block settings
    blocks: PublishBlocks = Field(
        default_factory=PublishBlocks,
        description="Publish block settings",
    )


class ColumnFormat(BaseModel):
    """A data class for the Datawrapper API's 'column_format' attribute."""

    model_config = ConfigDict(
        populate_by_name=True,
        strict=True,
        json_schema_extra={
            "examples": [
                {
                    "column": "sales",
                    "type": "number",
                    "ignore": False,
                    "number-prepend": "$",
                    "number-append": "",
                }
            ]
        },
    )

    #: "The name of the data column for the line"
    column: str = Field(
        description="The name of the data column for the line",
        min_length=1,
    )

    #: The data type of the column
    type: Literal["auto", "text", "number", "date"] = Field(
        default="auto", description="The data type of the column"
    )

    #: Whether to ignore the column
    ignore: bool = Field(default=False, description="Whether to ignore the column")

    #: What to prepend before the number
    number_prepend: str = Field(
        default="",
        alias="number-prepend",
        description="What to prepend before the number",
    )

    #: What to append after the number
    number_append: str = Field(
        default="", alias="number-append", description="What to append after the number"
    )

    #: Number divisor for scaling values (use NumberDivisor enum or raw API values)
    number_divisor: NumberDivisor | int | str = Field(
        default=0,
        alias="number-divisor",
        description="Number divisor for scaling values. Use NumberDivisor enum for readability or raw API values (0, 'auto', 3, 6, 9, -2, -3, -6, -9, -12).",
    )

    #: Number/date format for the column (use DateFormat or NumberFormat enum or raw format strings)
    number_format: DateFormat | NumberFormat | str = Field(
        default="-",
        alias="number-format",
        description="Number or date format for the column. Use DateFormat for temporal data, NumberFormat for numeric data, or provide custom format strings.",
    )

    @field_validator("number_divisor")
    @classmethod
    def validate_number_divisor(
        cls, v: NumberDivisor | int | str
    ) -> NumberDivisor | int | str:
        """Validate number_divisor is a valid value.

        Accepts NumberDivisor enum values or raw API values (int or str).
        """
        # If it's already a NumberDivisor enum, it's valid
        if isinstance(v, NumberDivisor):
            return v

        # Define valid raw values (both int and string representations)
        valid_values = {
            0,
            "0",
            "auto",
            3,
            "3",
            6,
            "6",
            9,
            "9",
            -2,
            "-2",
            -3,
            "-3",
            -6,
            "-6",
            -9,
            "-9",
            -12,
            "-12",
        }

        if v not in valid_values:
            raise ValueError(
                f"Invalid number_divisor: {v}. Use NumberDivisor enum or valid API values: "
                f"0, 'auto', 3, 6, 9, -2, -3, -6, -9, -12"
            )
        return v


class ColumnFormatList(BaseModel):
    """A wrapper for a list of ColumnFormat objects that handles API serialization.

    The Datawrapper API expects column-format as a dictionary where column names
    are keys and format configs are values. This model handles the conversion
    between the user-friendly list format and the API's dict format.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "examples": [
                {
                    "formats": [
                        {"column": "sales", "type": "number", "number-prepend": "$"},
                        {"column": "date", "type": "date"},
                    ]
                }
            ]
        },
    )

    #: The list of column format configurations
    formats: list[ColumnFormat] = Field(
        default_factory=list,
        description="The list of column format configurations",
    )

    @model_validator(mode="before")
    @classmethod
    def convert_from_dict_or_list(cls, data: Any) -> dict[str, Any]:
        """Convert dict format (from API) or list format to internal structure.

        Handles three input formats:
        1. Dict with 'formats' key (already in correct format)
        2. Dict without 'formats' key (API format - column names as keys)
        3. List of ColumnFormat objects or dicts (direct list format)
        """
        # If it's already a dict with 'formats', use it as-is
        if isinstance(data, dict) and "formats" in data:
            formats = data["formats"]
            # Ensure all items are ColumnFormat objects
            if isinstance(formats, list):
                data["formats"] = [
                    item
                    if isinstance(item, ColumnFormat)
                    else ColumnFormat.model_validate(item)
                    for item in formats
                ]
            return data

        # If it's a dict without 'formats', assume it's API format (column names as keys)
        if isinstance(data, dict):
            formats_list = []
            for col_name, col_config in data.items():
                if not isinstance(col_config, dict):
                    raise ValueError(
                        f"column_format values must be dictionaries, got {type(col_config).__name__} for column '{col_name}'"
                    )
                formats_list.append({"column": col_name, **col_config})
            return {"formats": formats_list}

        # If it's a list, wrap it in the formats key
        if isinstance(data, list):
            return {"formats": data}

        # For any other type, return as-is and let Pydantic validation handle it
        return data

    @model_serializer
    def serialize_to_dict(self) -> dict[str, dict[str, Any]]:
        """Serialize to API format (dict with column names as keys).

        Converts the internal list format to the dictionary format expected
        by the Datawrapper API, filtering out default values.
        """
        if not self.formats:
            return {}

        result: dict[str, dict[str, Any]] = {}
        for col_format in self.formats:
            # Extract column name as key
            col_name = col_format.column

            # Serialize the format config (excluding the column field)
            col_config = col_format.model_dump(by_alias=True, exclude={"column"})

            # Only include non-default values to match API expectations
            filtered_config = {}
            for key, value in col_config.items():
                # Include if not a default value
                if key == "type" and value != "auto":
                    filtered_config[key] = value
                elif key == "ignore" and value is not False:
                    filtered_config[key] = value
                elif key in ("number-prepend", "number-append") and value != "":
                    filtered_config[key] = value
                elif key == "number-divisor" and value not in (0, "0"):
                    # Convert NumberDivisor enum to its value for API
                    if isinstance(value, NumberDivisor):
                        filtered_config[key] = value.value
                    else:
                        filtered_config[key] = value

            result[col_name] = filtered_config

        return result

    def __iter__(self):
        """Allow iteration over the formats list."""
        return iter(self.formats)

    def __len__(self):
        """Return the number of formats."""
        return len(self.formats)

    def __getitem__(self, index):
        """Allow indexing into the formats list."""
        return self.formats[index]


class Transform(BaseModel):
    """A model for the Datawrapper API's 'data' metadata attribute."""

    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "examples": [
                {
                    "transpose": False,
                    "vertical-header": True,
                    "horizontal-header": True,
                    "column-order": [0, 1, 2],
                    "column-format": [
                        {"column": "sales", "type": "number", "number-prepend": "$"}
                    ],
                    "external-data": "",
                    "use-datawrapper-cdn": True,
                    "upload-method": "copy",
                }
            ]
        },
    )

    #: Whether to transpose the data
    transpose: bool = Field(default=False, description="Whether to transpose the data")

    #: I don't know what this does
    vertical_header: bool = Field(
        default=True, alias="vertical-header", description="I don't know what this does"
    )

    #: I don't know what this does
    horizontal_header: bool = Field(
        default=True,
        alias="horizontal-header",
        description="I don't know what this does",
    )

    # The order of the columns
    column_order: list[int] = Field(
        default_factory=list,
        alias="column-order",
        description="The order of the columns",
    )

    # Use ColumnFormatList wrapper for column-format
    column_format: ColumnFormatList = Field(
        default_factory=ColumnFormatList,
        alias="column-format",
        description="The formatting options for the data columns",
    )

    #: An external data source URL
    external_data: str = Field(
        default="", alias="external-data", description="An external data source URL"
    )

    #: Whether or not the external data URL should use the datawrapper CDN
    use_datawrapper_cdn: bool = Field(
        default=True,
        alias="use-datawrapper-cdn",
        description="Whether or not the external data URL should use the datawrapper CDN",
    )

    #: The uploading method for the data
    upload_method: Literal["copy", "upload", "google-spreadsheet", "external-data"] = (
        Field(
            default="copy",
            alias="upload-method",
            description="The uploading method for the data",
        )
    )


class Describe(BaseModel):
    """A model for the Datawrapper API's 'describe' attribute."""

    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "examples": [
                {
                    "intro": "Chart introduction text",
                    "byline": "Created by Data Team",
                    "source-name": "Example Data Source",
                    "source-url": "https://example.com/data",
                    "aria-description": "This chart shows trends over time",
                    "hide-title": False,
                    "number-format": "-",
                    "number-divisor": 0,
                    "number-prepend": "$",
                    "number-append": "M",
                }
            ]
        },
    )

    #: The intro text that appears above the chart
    intro: str = Field(
        default="", description="The intro text that appears above the chart"
    )

    #: The byline that appears below the chart
    byline: str = Field(
        default="", description="The byline that appears below the chart"
    )

    #: The source name that appears below the chart
    source_name: str = Field(
        default="",
        alias="source-name",
        description="The source name that appears below the chart",
    )

    #: The source URL that appears below the chart
    source_url: str = Field(
        default="",
        alias="source-url",
        description="The source URL that appears below the chart",
    )

    #: The alternative text for screen readers
    aria_description: str = Field(
        default="",
        alias="aria-description",
        description="The alternative text for screen readers",
    )

    #: Whether to hide the title
    hide_title: bool = Field(
        default=False, alias="hide-title", description="Whether to hide the title"
    )

    #: The number format for data columns in the chart (use NumberFormat enum or raw format strings)
    number_format: NumberFormat | str = Field(
        default="-",
        alias="number-format",
        description="The number format for data columns in the chart. Use NumberFormat enum for common formats or provide custom format strings.",
    )

    #: The number divisor for data columns in the chart
    number_divisor: int = Field(
        default=0,
        alias="number-divisor",
        description="The number divisor for data columns in the chart",
    )

    #: The string to prepend to the number
    number_prepend: str = Field(
        default="",
        alias="number-prepend",
        description="The string to prepend to the number",
    )

    #: The string to append to the number
    number_append: str = Field(
        default="",
        alias="number-append",
        description="The string to append to the number",
    )

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


class ColorCategory:
    """Utility class for serializing and deserializing color category structures."""

    @staticmethod
    def serialize(
        color_map: dict[str, str],
        category_labels: dict[str, str] | None = None,
        category_order: list[str] | None = None,
        exclude_from_key: list[str] | None = None,
    ) -> dict[str, Any]:
        """Convert color category data to API format.

        Args:
            color_map: Mapping of layer names to colors
            category_labels: Optional mapping of category names to display labels
            category_order: Optional list defining category order in chart and legend
            exclude_from_key: Optional list of columns to exclude from color key

        Returns:
            Dictionary in API format with 'map' and optional additional fields

        Example:
            >>> ColorCategory.serialize({"A": "#ff0000", "B": "#00ff00"})
            {'map': {'A': '#ff0000', 'B': '#00ff00'}}
            >>> ColorCategory.serialize(
            ...     {"A": "#ff0000"},
            ...     category_labels={"A": "Category A"},
            ...     category_order=["A", "B"],
            ...     exclude_from_key=[],
            ... )
            {'map': {'A': '#ff0000'}, 'excludeFromKey': [], 'categoryLabels': {'A': 'Category A'}, 'categoryOrder': ['A', 'B']}
        """
        result: dict[str, Any] = {"map": color_map}

        # Only include excludeFromKey if explicitly provided (not None)
        if exclude_from_key is not None:
            result["excludeFromKey"] = exclude_from_key

        # Only include category_labels and category_order if they're non-empty
        if category_labels:
            result["categoryLabels"] = category_labels
        if category_order:
            result["categoryOrder"] = category_order

        return result

    @staticmethod
    def deserialize(color_category_obj: dict[str, Any] | None) -> dict[str, Any]:
        """Parse color category data from API format.

        Args:
            color_category_obj: The color-category object from API response

        Returns:
            Dictionary with keys: color_category, category_labels, category_order, exclude_from_color_key

        Example:
            >>> ColorCategory.deserialize({"map": {"A": "#ff0000"}})
            {'color_category': {'A': '#ff0000'}, 'category_labels': {}, 'category_order': [], 'exclude_from_color_key': []}
            >>> ColorCategory.deserialize(None)
            {'color_category': {}, 'category_labels': {}, 'category_order': [], 'exclude_from_color_key': []}
        """
        if not isinstance(color_category_obj, dict):
            return {
                "color_category": {},
                "category_labels": {},
                "category_order": [],
                "exclude_from_color_key": [],
            }

        return {
            "color_category": color_category_obj.get("map", {}),
            "category_labels": color_category_obj.get("categoryLabels", {}),
            "category_order": color_category_obj.get("categoryOrder", []),
            "exclude_from_color_key": color_category_obj.get("excludeFromKey", []),
        }


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

    #: The number format for data columns in the chart
    number_format: str = Field(
        default="-",
        alias="number-format",
        description="The number format for data columns in the chart",
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

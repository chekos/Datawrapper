"""Pydantic models for Datawrapper API metadata structures."""

from typing import Any, Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_serializer,
    model_validator,
)
from .enums import DateFormat, LineDash, LineWidth, NumberDivisor, NumberFormat


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

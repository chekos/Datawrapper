"""Pydantic models for Datawrapper API metadata structures."""

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


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


class Transform(BaseModel):
    """A model for the Datawrapper API's 'data' metadata attribute."""

    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "examples": [
                # Example 1: Using dictionary style for column_format
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
                },
                # Example 2: Using python attribute style to initialize column_format
                {
                    "transpose": True,
                    "vertical-header": False,
                    "horizontal-header": True,
                    "column-order": [2, 0, 1],
                    "column-format": [{"column": "date", "type": "date"}],
                    "external-data": "https://example.com/data.csv",
                    "use-datawrapper-cdn": False,
                    "upload-method": "external-data",
                },
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

    # Accept either ColumnFormat objects or dicts
    column_format: list[ColumnFormat | dict] = Field(
        default_factory=list,
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

    @model_validator(mode="before")
    @classmethod
    def convert_column_format_dicts(cls, data: dict[str, Any]) -> dict[str, Any]:
        """Convert dictionary items in column_format to ColumnFormat objects."""
        if not isinstance(data, dict):
            return data

        # Check both Python style and JSON style field names
        for field_name in ["column_format", "column-format"]:
            if field_name in data and isinstance(data[field_name], list):
                data[field_name] = [
                    item
                    if isinstance(item, ColumnFormat)
                    else ColumnFormat.model_validate(item)
                    for item in data[field_name]
                ]

        return data

    @classmethod
    def from_api_data_section(cls, api_data: dict[str, Any]) -> "Transform":
        """Create Transform from Datawrapper API's metadata.data section.

        Handles the API's dict-based column-format structure by converting it
        to the list-based structure expected by this model.

        Args:
            api_data: The 'data' section from API metadata response

        Returns:
            A validated Transform instance

        Example:
            >>> api_response = {
            ...     "data": {"column-format": {"sales": {"type": "number"}}}
            ... }
            >>> transform = Transform.from_api_data_section(api_response["data"])
        """
        # Make a copy to avoid mutating the input
        data = api_data.copy()

        # Convert column-format from dict to list if needed
        if "column-format" in data and isinstance(data["column-format"], dict):
            column_format_dict = data["column-format"]
            data["column-format"] = (
                [
                    {"column": col_name, **col_config}
                    for col_name, col_config in column_format_dict.items()
                ]
                if column_format_dict
                else []
            )

        return cls.model_validate(data)


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

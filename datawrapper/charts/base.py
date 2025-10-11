import os
from io import StringIO
from typing import Any, Literal

import pandas as pd
from pydantic import BaseModel, ConfigDict, Field, model_serializer, model_validator

from datawrapper.__main__ import Datawrapper


class Annotate(BaseModel):
    """A data class for the Datawrapper API's 'annotate' attribute."""

    model_config = ConfigDict(
        populate_by_name=True,
        strict=True,
        json_schema_extra={
            "examples": [{"notes": "Example note", "byline": "By John Doe"}]
        },
    )

    #: The footnotes that appear below the chart
    notes: str = Field(
        default="",
        description="The footnotes that appear below the chart",
    )

    #: The byline that appears below the chart
    byline: str = Field(
        default="",
        description="The byline that appears below the chart",
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


class BaseChart(BaseModel):
    """A base class for Datawrapper charts published via its API."""

    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "examples": [
                # Example 1: A simple chart without much configuration
                {
                    "chart_type": "d3-lines",
                    "title": "Sample Chart Title",
                    "source_name": "Reuters",
                    "language": "en-US",
                },
                # Example 2: Transform as dict
                {
                    "chart_type": "d3-lines",
                    "title": "Sample Chart Title",
                    "source_name": "Reuters",
                    "language": "en-US",
                    "transformations": {
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
                },
                # Example 3: Transform as Transform object (using aliases)
                {
                    "chart_type": "d3-lines",
                    "title": "Sample Chart Title",
                    "source_name": "Reuters",
                    "language": "en-US",
                    "transformations": {
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
                },
            ]
        },
        arbitrary_types_allowed=True,  # To allow pandas DataFrame
    )

    #: The type of datawrapper chart to create
    chart_type: Literal[
        "d3-lines",
        "d3-area",
        "d3-bars",
        "d3-scatter-plot",
        "locator-map",
        "column-chart",
    ] = Field(alias="chart-type", description="The type of datawrapper chart to create")

    #
    # Data
    #

    #: The data to use for the chart
    data: pd.DataFrame | list[dict] = Field(
        default_factory=list[dict], description="The data to use for the chart"
    )

    #: The metadata options for the data columns in the "Check and Describe" tab
    transformations: Transform | dict[str, Any] = Field(default_factory=Transform)

    #
    # Description
    #

    #: The headline that appears above the chart
    title: str = Field(
        default="", description="The headline that appears above the chart"
    )

    #: The intro text that appears above the chart
    intro: str = Field(
        default="", description="The intro text that appears above the chart"
    )

    #: The footnotes that appear below the chart
    notes: str = Field(
        default="", description="The footnotes that appear below the chart"
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

    #: The byline that appears below the chart
    byline: str = Field(
        default="", description="The byline that appears below the chart"
    )

    #: The alternative text for screen readers
    aria_description: str = Field(
        default="",
        alias="aria-description",
        description="The alternative text for screen readers",
    )

    #: Whether or not to hide the title
    hide_title: bool = Field(
        default=False,
        alias="hide-title",
        description="Whether or not to hide the title",
    )

    #
    # Layout
    #

    #: The locale of the chart, which defines decimal and thousand separators as well as translations of month and weekday names.
    language: str = Field(
        default="en-US",
        description="The locale of the chart, which defines decimal and thousand separators as well as translations of month and weekday names.",
    )

    #: The theme of the chart
    theme: str = Field(default="", description="The theme of the chart")

    #: Whether the chart should automatically flip to dark mode when the user's system is in dark mode
    auto_dark_mode: bool = Field(
        default=False,
        alias="autoDarkMode",
        description="Whether the chart should automatically flip to dark mode when the user's system is in dark mode",
    )

    #: Whether to invert colors in dark mode
    dark_mode_invert: bool = Field(
        default=True,
        alias="dark-mode-invert",
        description="Whether to invert colors in dark mode",
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
        default=False, alias="download-pdf", description="Whether to allow PDF download"
    )

    #: Whether to allow SVG download
    download_svg: bool = Field(
        default=False, alias="download-svg", description="Whether to allow SVG download"
    )

    #: Whether to allow embedding
    embed: bool = Field(default=False, description="Whether to allow embedding")

    #: Whether to attribute the chart to datawrapper
    force_attribution: bool = Field(
        default=False,
        alias="force-attribution",
        description="Whether to attribute the chart to datawrapper",
    )

    #: Whether to show social media share buttons
    share_buttons: bool = Field(
        default=False, description="Whether to show social media share buttons"
    )

    #: What URL to share
    share_url: str = Field(default="", description="What URL to share")

    #: Whether to show a logo
    logo: bool = Field(default=False, description="Whether to show a logo")

    #: The id of the logo to show
    logo_id: str = Field(default="", description="The id of the logo to show")

    #: A dictionary of custom tags to attach to the chart
    custom: dict[str, Any] = Field(
        default_factory=dict,
        description="A dictionary of custom tags to attach to the chart",
    )

    #
    # API Integration
    #

    #: The chart ID after creation (populated by create() method)
    chart_id: str | None = Field(
        default=None,
        description="The chart ID after creation (populated by create() method)",
        exclude=True,  # Don't include in serialization
    )

    def __init__(self, **data):
        """Initialize the BaseChart with private attributes."""
        super().__init__(**data)
        self._client: Datawrapper | None = None

    def _get_client(self, access_token: str | None = None) -> Datawrapper:
        """Get or create a Datawrapper client instance."""
        if self._client is not None:
            return self._client

        # Try to get access token from parameter, environment, or raise error
        token = access_token or os.getenv("DATAWRAPPER_ACCESS_TOKEN")
        if not token:
            raise ValueError(
                "No Datawrapper access token provided. "
                "Set DATAWRAPPER_ACCESS_TOKEN environment variable or pass access_token parameter."
            )

        self._client = Datawrapper(access_token=token)
        return self._client

    def create(self, access_token: str | None = None) -> str:
        """Create a new chart via the Datawrapper API.

        Args:
            access_token: Optional Datawrapper API access token.
                         If not provided, will use DATAWRAPPER_ACCESS_TOKEN environment variable.

        Returns:
            The chart ID of the created chart.

        Raises:
            ValueError: If no access token is available or API returns invalid response.
            Exception: If the API request fails.
        """
        client = self._get_client(access_token)

        # Get the serialized chart data
        chart_data = self.serialize_model()

        try:
            # Create chart using direct POST to charts endpoint
            payload = {
                "title": chart_data["title"],
                "type": chart_data["type"],
                "language": chart_data.get("language"),
                "metadata": chart_data["metadata"],
            }

            # Only include theme if it's not empty
            theme = chart_data.get("theme", "")
            if theme:
                payload["theme"] = theme

            response = client.post(
                client._CHARTS_URL,
                data=payload,
                extra_headers={"content-type": "application/json"},
            )
        except Exception as e:
            raise Exception(
                f"Failed to create chart via Datawrapper API. Error: {str(e)}"
            ) from e

        # Extract and validate the chart ID
        if isinstance(response, dict):
            chart_id = response.get("id")
        else:
            raise ValueError(f"Unexpected response type from API: {type(response)}")

        if not chart_id or not isinstance(chart_id, str):
            raise ValueError(f"Invalid chart ID received from API: {chart_id}")

        # Store the chart ID
        self.chart_id = chart_id

        # Upload data if present
        if not (
            self.data.empty
            if isinstance(self.data, pd.DataFrame)
            else not bool(self.data)
        ):
            try:
                # Convert data to CSV string
                if isinstance(self.data, pd.DataFrame):
                    csv_data = self.data.to_csv(index=False, encoding="utf-8")
                else:
                    # Convert list of dicts to DataFrame first, then to CSV
                    df = pd.DataFrame(self.data)
                    csv_data = df.to_csv(index=False, encoding="utf-8")

                # Upload data using PUT
                client.put(
                    f"{client._CHARTS_URL}/{chart_id}/data",
                    data=csv_data.encode("utf-8"),
                    extra_headers={"content-type": "text/csv"},
                    dump_data=False,  # Don't JSON encode the CSV data
                )
            except Exception as e:
                raise Exception(
                    f"Chart created successfully (ID: {chart_id}) but failed to upload data. "
                    f"Error: {str(e)}"
                ) from e

        return chart_id

    def update(self, access_token: str | None = None) -> str:
        """Update an existing chart via the Datawrapper API.

        Args:
            access_token: Optional Datawrapper API access token.
                         If not provided, will use DATAWRAPPER_ACCESS_TOKEN environment variable.

        Returns:
            The chart ID of the updated chart.

        Raises:
            ValueError: If no chart_id is set or no access token is available.
            Exception: If the API request fails.
        """
        if not self.chart_id:
            raise ValueError(
                "No chart_id set. Use create() first or set chart_id manually."
            )

        client = self._get_client(access_token)

        # Get the serialized chart data
        chart_data = self.serialize_model()

        try:
            # Update chart using direct PATCH to charts endpoint
            payload = {
                "title": chart_data["title"],
                "type": chart_data["type"],
                "language": chart_data.get("language"),
                "metadata": chart_data["metadata"],
            }

            # Only include theme if it's not empty
            theme = chart_data.get("theme", "")
            if theme:
                payload["theme"] = theme

            client.patch(
                f"{client._CHARTS_URL}/{self.chart_id}",
                data=payload,
                extra_headers={"content-type": "application/json"},
            )
        except Exception as e:
            raise Exception(
                f"Failed to update chart via Datawrapper API. Error: {str(e)}"
            ) from e

        # Upload data if present
        if not (
            self.data.empty
            if isinstance(self.data, pd.DataFrame)
            else not bool(self.data)
        ):
            try:
                # Convert data to CSV string
                if isinstance(self.data, pd.DataFrame):
                    csv_data = self.data.to_csv(index=False, encoding="utf-8")
                else:
                    # Convert list of dicts to DataFrame first, then to CSV
                    df = pd.DataFrame(self.data)
                    csv_data = df.to_csv(index=False, encoding="utf-8")

                # Upload data using PUT
                client.put(
                    f"{client._CHARTS_URL}/{self.chart_id}/data",
                    data=csv_data.encode("utf-8"),
                    extra_headers={"content-type": "text/csv"},
                    dump_data=False,  # Don't JSON encode the CSV data
                )
            except Exception as e:
                raise Exception(
                    f"Chart updated successfully (ID: {self.chart_id}) but failed to upload data. "
                    f"Error: {str(e)}"
                ) from e

        return self.chart_id

    @model_validator(mode="before")
    @classmethod
    def convert_column_format_dicts(cls, data: dict[str, Any]) -> dict[str, Any]:
        """Convert dictionary items in transformation to Transform objects."""
        if not isinstance(data, dict):
            return data

        if "transformations" in data and isinstance(data["transformations"], dict):
            data["transformations"] = Transform.model_validate(data["transformations"])

        return data

    @model_serializer
    def serialize_model(self) -> dict[str, Any]:
        # Create a dict with the bare minimum provided by the base chart class
        # This will be supplemented by subclasses tailored to individual chart types
        # Start with root-level metadata required by Datawrapper API
        dw_obj: dict[str, Any] = {
            "type": self.chart_type,  # Note: API expects "type", not "chart-type"
            "title": self.title,
            "language": self.language,
        }

        # Only include theme if it's not empty
        if self.theme:
            dw_obj["theme"] = self.theme

        # Prepare the data
        data = self.data.copy()
        if isinstance(data, pd.DataFrame):
            data = data.to_dict(orient="records")

        # Set the transformations
        if isinstance(self.transformations, Transform):
            data_section = self.transformations.model_dump(by_alias=True)
        else:
            data_section = Transform.model_validate(self.transformations).model_dump(
                by_alias=True
            )

        # Validate the Describe data
        describe = Describe.model_validate(
            {
                "intro": self.intro,
                "byline": self.byline,
                "source-name": self.source_name,
                "source-url": self.source_url,
                "aria-description": self.aria_description,
                "hide-title": self.hide_title,
            }
        )

        # Validate the Annotate data
        annotate = Annotate.model_validate(
            {
                "notes": self.notes,
                "byline": self.byline,
            }
        )

        # Create the metadata section in the proper Datawrapper order
        dw_obj["metadata"] = {
            # Data section first
            "data": data_section,
            # Describe section
            "describe": describe.model_dump(by_alias=True),
            # Visualize section
            "visualize": {
                "dark-mode-invert": self.dark_mode_invert,
                "sharing": {
                    "enabled": self.share_buttons,
                    "url": self.share_url,
                    "auto": False,
                },
            },
            # Publish section
            "publish": {
                "autoDarkMode": self.auto_dark_mode,
                "force-attribution": self.force_attribution,
                "blocks": {
                    "get-the-data": self.get_the_data,
                    "download-image": self.download_image,
                    "download-pdf": self.download_pdf,
                    "download-svg": self.download_svg,
                    "embed": self.embed,
                    "logo": {
                        "id": self.logo_id,
                        "enabled": self.logo,
                    },
                },
            },
            # Annotate section
            "annotate": annotate.model_dump(by_alias=True),
            # Custom section
            "custom": self.custom,
        }

        # Return the obj
        return dw_obj

    @classmethod
    def get(cls, chart_id: str, access_token: str | None = None) -> "BaseChart":
        """Fetch an existing chart from the Datawrapper API.

        Args:
            chart_id: The ID of the chart to fetch
            access_token: Optional Datawrapper API access token.
                        If not provided, will use DATAWRAPPER_ACCESS_TOKEN environment variable.

        Returns:
            An instance of the chart class with data populated from the API.

        Raises:
            ValueError: If no access token is available or chart type doesn't match.
            Exception: If the API request fails.
        """
        # Create a temporary instance to use _get_client
        temp_instance = cls.__new__(cls)
        temp_instance._client = None
        client = temp_instance._get_client(access_token)
        
        try:
            # Fetch chart metadata
            response = client.get(f"{client._CHARTS_URL}/{chart_id}")
            
            if not isinstance(response, dict):
                raise ValueError(f"Unexpected response type from API: {type(response)}")
            
            # Verify chart type matches if this is a subclass
            chart_type = response.get("type")
            if hasattr(cls, "model_fields") and "chart_type" in cls.model_fields:
                # Check if this subclass has a specific chart_type constraint
                field_info = cls.model_fields["chart_type"]
                if hasattr(field_info.annotation, "__args__"):
                    # This is a Literal type with specific allowed values
                    allowed_types = field_info.annotation.__args__
                    if chart_type not in allowed_types:
                        raise ValueError(
                            f"Chart type mismatch: expected one of {allowed_types}, got '{chart_type}'. "
                            f"Use BaseChart.get() or the correct chart class."
                        )
            
            # Fetch chart data
            data_response = client.get(f"{client._CHARTS_URL}/{chart_id}/data")
            
        except Exception as e:
            raise Exception(
                f"Failed to fetch chart from Datawrapper API. Error: {str(e)}"
            ) from e
        
        # Parse the response into our model
        parsed_data = cls._from_api(response, data_response)
        
        # Create instance and set chart_id and client
        instance = cls(**parsed_data)
        instance.chart_id = chart_id
        instance._client = client
        
        return instance

    @classmethod
    def _from_api(
        cls, chart_metadata: dict[str, Any], csv_data: str
    ) -> dict[str, Any]:
        """Parse Datawrapper API response into model initialization data.
        
        This base implementation handles common fields. Subclasses should override
        _parse_visualize_metadata to handle chart-specific visualize settings.
        
        Args:
            chart_metadata: The JSON response from the chart metadata endpoint
            csv_data: The CSV data from the chart data endpoint
        
        Returns:
            Dictionary that can be used to initialize the model
        """
        metadata = chart_metadata.get("metadata", {})
        
        # Parse CSV data into DataFrame
        data_df = pd.read_csv(StringIO(csv_data))
        
        # Extract common fields
        describe = metadata.get("describe", {})
        annotate = metadata.get("annotate", {})
        publish = metadata.get("publish", {})
        publish_blocks = publish.get("blocks", {})
        publish_logo = publish_blocks.get("logo", {})
        visualize = metadata.get("visualize", {})
        visualize_sharing = visualize.get("sharing", {})
        
        # Build base initialization dict
        # Handle column-format: convert dict to list
        data_metadata = metadata.get("data", {})
        if "column-format" in data_metadata and isinstance(data_metadata["column-format"], dict):
            # Convert dict format (column_name -> config) to list format
            column_format_dict = data_metadata["column-format"]
            if column_format_dict:
                data_metadata["column-format"] = [
                    {"column": col_name, **col_config}
                    for col_name, col_config in column_format_dict.items()
                ]
            else:
                data_metadata["column-format"] = []
        
        init_data = {
            # Chart type and basic info
            "chart_type": chart_metadata.get("type"),
            "title": chart_metadata.get("title", ""),
            "theme": chart_metadata.get("theme", ""),
            "language": chart_metadata.get("language", "en-US"),
            
            # Data
            "data": data_df,
            "transformations": data_metadata,
            
            # Description
            "intro": describe.get("intro", ""),
            "notes": annotate.get("notes", ""),
            "source_name": describe.get("source-name", ""),
            "source_url": describe.get("source-url", ""),
            "byline": describe.get("byline", ""),
            "aria_description": describe.get("aria-description", ""),
            "hide_title": describe.get("hide-title", False),
            
            # Layout/Publish
            "auto_dark_mode": publish.get("autoDarkMode", False),
            "dark_mode_invert": visualize.get("dark-mode-invert", True),
            "get_the_data": publish_blocks.get("get-the-data", False),
            "download_image": publish_blocks.get("download-image", False),
            "download_pdf": publish_blocks.get("download-pdf", False),
            "download_svg": publish_blocks.get("download-svg", False),
            "embed": publish_blocks.get("embed", False),
            "force_attribution": publish.get("force-attribution", False),
            "share_buttons": visualize_sharing.get("enabled", False),
            "share_url": visualize_sharing.get("url", ""),
            "logo": publish_logo.get("enabled", False),
            "logo_id": publish_logo.get("id", ""),
            
            # Custom
            "custom": metadata.get("custom", {}),
        }
        
        return init_data

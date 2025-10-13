import os
import uuid
from io import StringIO
from pathlib import Path
from typing import Any, Literal

import pandas as pd
from IPython.display import Image
from pydantic import BaseModel, ConfigDict, Field, model_serializer, model_validator

from datawrapper.__main__ import Datawrapper
from datawrapper.charts.annos import RangeAnnotation, TextAnnotation
from datawrapper.charts.models import (
    Annotate,
    Describe,
    Publish,
    Transform,
    Visualize,
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
        "column-chart",
        "d3-area",
        "d3-arrow-plot",
        "d3-bars",
        "d3-bars-stacked",
        "d3-lines",
        "d3-scatter-plot",
        "locator-map",
        "multiple-columns",
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
    # Chart Settings
    #

    #: Whether to allow other users to fork this visualization
    forkable: bool = Field(
        default=True,
        description="Whether to allow other users to fork this visualization",
    )

    #: The chart ID after creation (populated by create() method)
    chart_id: str | None = Field(
        default=None,
        description="The chart ID after creation (populated by create() method)",
        exclude=True,  # Don't include in serialization
    )

    #
    # Serialization methods for preparing data for API upload
    #

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

        # Set the transformations
        data_section = (
            self.transformations
            if isinstance(self.transformations, Transform)
            else Transform.model_validate(self.transformations)
        ).model_dump(by_alias=True)

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
            }
        )

        # Validate the Visualize data
        visualize = Visualize.model_validate(
            {
                "dark-mode-invert": self.dark_mode_invert,
                "sharing": {
                    "enabled": self.share_buttons,
                    "url": self.share_url,
                    "auto": False,
                },
            }
        )

        # Validate the Publish data
        publish = Publish.model_validate(
            {
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
            }
        )

        # Create the metadata section in the proper Datawrapper order
        dw_obj["metadata"] = {
            "data": data_section,
            "describe": describe.model_dump(by_alias=True),
            "visualize": visualize.model_dump(by_alias=True),
            "publish": publish.model_dump(by_alias=True),
            "annotate": annotate.model_dump(by_alias=True),
            "custom": self.custom,
        }

        # Return the obj
        return dw_obj

    def serialize_data(self) -> str | None:
        """Convert data to CSV string for API upload.

        Returns:
            CSV string representation of the data, or None if data is empty.
        """
        # Check if data is empty
        if isinstance(self.data, pd.DataFrame):
            if self.data.empty:
                return None
        else:
            if not bool(self.data):
                return None

        # Convert to CSV
        if isinstance(self.data, pd.DataFrame):
            return self.data.to_csv(index=False, encoding="utf-8")
        else:
            # Convert list of dicts to DataFrame first, then to CSV
            df = pd.DataFrame(self.data)
            return df.to_csv(index=False, encoding="utf-8")

    def _serialize_annotations(
        self,
        annotations: list[Any],
        annotation_class: type[TextAnnotation | RangeAnnotation],
    ) -> dict[str, Any]:
        """Serialize annotations to dict with UUID keys.

        Preserves existing UUIDs from deserialized charts to prevent duplicates.
        Generates new UUIDs for new annotations.

        Args:
            annotations: List of annotation objects or dicts
            annotation_class: The annotation class (TextAnnotation or RangeAnnotation)

        Returns:
            Dictionary mapping UUID keys to serialized annotation data
        """
        result = {}
        for anno_obj in annotations:
            # Convert to annotation object if needed
            if isinstance(anno_obj, dict):
                anno = annotation_class.model_validate(anno_obj)
            else:
                anno = anno_obj

            # Use existing ID or generate new one
            if anno.id:
                anno_id = anno.id
            else:
                anno_id = str(uuid.uuid4()).replace("-", "")[:10]

            # Serialize the annotation using the custom serialize_model method
            result[anno_id] = anno.serialize_model()

        return result

    @classmethod
    def _deserialize_annotations(
        cls,
        api_data: dict[str, dict] | list | None,
        annotation_class: type[TextAnnotation | RangeAnnotation],
    ) -> list[dict[str, Any]]:
        """Deserialize annotations from API response.

        Args:
            api_data: The annotation data from API (dict with UUID keys or list)
            annotation_class: The annotation class (TextAnnotation or RangeAnnotation)

        Returns:
            List of annotation dicts ready for model initialization
        """
        return annotation_class.deserialize_model(api_data)

    #
    # Deserialization methods for parsing API responses and input data
    #

    @model_validator(mode="before")
    @classmethod
    def convert_column_format_dicts(cls, data: dict[str, Any]) -> dict[str, Any]:
        """Convert dictionary items in transformation to Transform objects."""
        if not isinstance(data, dict):
            return data

        if "transformations" in data and isinstance(data["transformations"], dict):
            data["transformations"] = Transform.model_validate(data["transformations"])

        return data

    @classmethod
    def deserialize_data(cls, csv_data: str) -> pd.DataFrame:
        """Parse CSV string from Datawrapper API into DataFrame.

        Args:
            csv_data: The CSV data from the chart data endpoint

        Returns:
            DataFrame containing the parsed CSV data
        """
        # Use sep=None with engine='python' to auto-detect delimiter (comma or tab)
        return pd.read_csv(StringIO(csv_data), sep=None, engine="python")

    @classmethod
    def deserialize_model(cls, api_response: dict[str, Any]) -> dict[str, Any]:
        """Parse Datawrapper API response into model initialization data.

        This base implementation handles common fields. Subclasses should override
        to handle chart-specific visualize settings.

        Args:
            api_response: The JSON response from the chart metadata endpoint

        Returns:
            Dictionary that can be used to initialize the model (without data)
        """
        metadata = api_response.get("metadata", {})

        # Extract common fields
        describe = metadata.get("describe", {})
        annotate = metadata.get("annotate", {})
        publish = metadata.get("publish", {})
        publish_blocks = publish.get("blocks", {})
        publish_logo = publish_blocks.get("logo", {})
        visualize = metadata.get("visualize", {})
        visualize_sharing = visualize.get("sharing", {})

        # Build base initialization dict without hardcoded defaults
        # Pydantic will apply model field defaults for any missing values
        result = {
            # Chart type and basic info
            "chart_type": api_response.get("type"),
            "title": api_response.get("title"),
            "theme": api_response.get("theme"),
            "language": api_response.get("language"),
            "forkable": api_response.get("forkable"),
            # Data transformations (but not the data itself)
            "transformations": Transform.from_api_data_section(
                metadata.get("data", {})
            ),
            # Description
            "intro": describe.get("intro"),
            "notes": annotate.get("notes"),
            "source_name": describe.get("source-name"),
            "source_url": describe.get("source-url"),
            "byline": describe.get("byline"),
            "aria_description": describe.get("aria-description"),
            "hide_title": describe.get("hide-title"),
            # Layout/Publish
            "auto_dark_mode": publish.get("autoDarkMode"),
            "dark_mode_invert": visualize.get("dark-mode-invert"),
            "get_the_data": publish_blocks.get("get-the-data"),
            "download_image": publish_blocks.get("download-image"),
            "download_pdf": publish_blocks.get("download-pdf"),
            "download_svg": publish_blocks.get("download-svg"),
            "embed": publish_blocks.get("embed"),
            "force_attribution": publish.get("force-attribution"),
            "share_buttons": visualize_sharing.get("enabled"),
            "share_url": visualize_sharing.get("url"),
            "logo": publish_logo.get("enabled"),
            "logo_id": publish_logo.get("id"),
            # Custom
            "custom": metadata.get("custom"),
        }

        # Remove None values to let Pydantic apply model defaults
        return {k: v for k, v in result.items() if v is not None}

    #
    # CRUD methods for Datawrapper API
    #

    def __init__(self, **data):
        """Initialize the BaseChart with private attributes."""
        super().__init__(**data)
        self._client = None

    def _get_client(self, access_token: str | None = None) -> Datawrapper:
        """Get or create a Datawrapper client instance.

        Args:
            access_token: Optional Datawrapper API access token.
                           If not provided, will use DATAWRAPPER_ACCESS_TOKEN environment variable.

        Returns:
            An instance of the Datawrapper client.
        """
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

    @classmethod
    def _validate_chart_type(cls, chart_type: str) -> None:
        """Validate that the chart type matches the class's allowed types.

        Args:
            chart_type: The chart type from the API response

        Raises:
            ValueError: If chart type doesn't match the class's constraints
        """
        if hasattr(cls, "model_fields") and "chart_type" in cls.model_fields:
            field_info = cls.model_fields["chart_type"]
            if hasattr(field_info.annotation, "__args__"):
                assert field_info.annotation
                allowed_types = field_info.annotation.__args__
                if chart_type not in allowed_types:
                    raise ValueError(
                        f"Chart type mismatch: expected one of {allowed_types}, "
                        f"got '{chart_type}'. Use BaseChart.get() or the correct chart class."
                    )

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
        # Get token from parameter or environment
        token = access_token or os.getenv("DATAWRAPPER_ACCESS_TOKEN")
        if not token:
            raise ValueError(
                "No Datawrapper access token provided. "
                "Set DATAWRAPPER_ACCESS_TOKEN environment variable or pass access_token parameter."
            )

        # Create a Datawrapper client instance
        client = Datawrapper(access_token=token)

        try:
            # Fetch chart metadata
            metadata_response = client.get(f"{client._CHARTS_URL}/{chart_id}")

            if not isinstance(metadata_response, dict):
                raise ValueError(
                    f"Unexpected response type from API: {type(metadata_response)}"
                )
        except Exception as e:
            raise Exception(
                f"Failed to fetch chart from Datawrapper API. Error: {str(e)}"
            ) from e

        # Verify chart type matches if this is a subclass
        chart_type = metadata_response.get("type")
        assert chart_type is not None, "API response missing 'type' field"
        cls._validate_chart_type(chart_type)

        try:
            # Fetch chart data
            data_response = client.get(f"{client._CHARTS_URL}/{chart_id}/data")
        except Exception as e:
            raise Exception(
                f"Failed to fetch chart data from Datawrapper API. Error: {str(e)}"
            ) from e

        # Parse metadata and data separately
        metadata_dict = cls.deserialize_model(metadata_response)
        data_df = cls.deserialize_data(data_response)

        # Merge them
        parsed_data = {**metadata_dict, "data": data_df}

        # Create instance and set chart_id and client
        instance = cls(**parsed_data)
        instance.chart_id = chart_id
        instance._client = client

        # Return the instance
        return instance

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
        # Get the client
        client = self._get_client(access_token)

        # Get the serialized chart metadata
        metadata = self.serialize_model()

        # Use the convenience method from the client to create the chart
        response = client.create_chart(
            title=metadata["title"],
            chart_type=metadata["type"],
            theme=metadata.get("theme") or None,
            data=self.serialize_data(),
            forkable=self.forkable,
            language=metadata.get("language"),
            metadata=metadata["metadata"],
        )

        # Extract and validate the chart ID
        if not isinstance(response, dict):
            raise ValueError(f"Unexpected response type from API: {type(response)}")
        chart_id = response.get("id")
        if not chart_id or not isinstance(chart_id, str):
            raise ValueError(f"Invalid chart ID received from API: {chart_id}")

        # Store and return the chart ID
        self.chart_id = chart_id
        return self.chart_id

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

        # Get the client
        client = self._get_client(access_token)

        # Get the serialized chart metadata
        metadata = self.serialize_model()

        # Use the convenience method from the client to update the chart
        client.update_chart(
            chart_id=self.chart_id,
            title=metadata["title"],
            chart_type=metadata["type"],
            theme=metadata.get("theme") or None,
            data=self.serialize_data(),
            language=metadata.get("language"),
            metadata=metadata["metadata"],
        )

        # Return the chart ID
        return self.chart_id

    def export(
        self,
        unit: str = "px",
        mode: str = "rgb",
        width: int = 400,
        height: int | str | None = None,
        plain: bool = False,
        zoom: int = 2,
        scale: int = 1,
        border_width: int = 20,
        border_color: str | None = None,
        transparent: bool = False,
        download: bool = False,
        full_vector: bool = False,
        ligatures: bool = True,
        logo: str = "auto",
        logo_id: str | None = None,
        dark: bool = False,
        output: str = "png",
        filepath: str = "./image.png",
        display: bool = False,
        access_token: str | None = None,
    ) -> Path | Image:
        """Export the chart to an image file.

        Args:
            unit: One of px, mm, inch. Defines the unit in which the borderwidth, height,
                and width will be measured in, by default "px"
            mode: One of rgb or cmyk. Which color mode the output should be in,
                by default "rgb"
            width: Width of visualization. If not specified, it takes the chart width,
                by default 400
            height: Height of visualization. Can be a number or "auto", by default None
            plain: Defines if only the visualization should be exported (True), or if it should
                include header and footer as well (False), by default False
            zoom: Defines the multiplier for the png size, by default 2
            scale: Defines the multiplier for the pdf size, by default 1
            border_width: Margin around the visualization, by default 20
            border_color: Color of the border around the visualization, by default None
            transparent: Set to True to export your visualization with a transparent background,
                by default False
            download: Whether to trigger a download, by default False
            full_vector: Export as full vector graphic (for supported formats), by default False
            ligatures: Enable typographic ligatures, by default True
            logo: Logo display setting. One of "auto", "on", or "off", by default "auto"
            logo_id: Custom logo ID to use, by default None
            dark: Export in dark mode, by default False
            output: One of png, pdf, or svg, by default "png"
            filepath: Name/filepath to save output in, by default "./image.png"
            display: Whether to display the exported image as output in the notebook cell,
                by default False
            access_token: Optional Datawrapper API access token.
                If not provided, will use DATAWRAPPER_ACCESS_TOKEN environment variable.

        Returns:
            The file path to the exported image or an Image object displaying the image.

        Raises:
            ValueError: If no chart_id is set or no access token is available.
            Exception: If the API request fails.
        """
        if not self.chart_id:
            raise ValueError(
                "No chart_id set. Use create() first or set chart_id manually."
            )

        # Get the client
        client = self._get_client(access_token)

        # Call the export_chart method from the client
        return client.export_chart(
            chart_id=self.chart_id,
            unit=unit,
            mode=mode,
            width=width,
            height=height,
            plain=plain,
            zoom=zoom,
            scale=scale,
            border_width=border_width,
            border_color=border_color,
            transparent=transparent,
            download=download,
            full_vector=full_vector,
            ligatures=ligatures,
            logo=logo,
            logo_id=logo_id,
            dark=dark,
            output=output,
            filepath=filepath,
            display=display,
        )

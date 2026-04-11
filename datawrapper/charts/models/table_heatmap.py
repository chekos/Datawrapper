import warnings
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from ..enums import NumberFormat


class ColorStop(BaseModel):
    """Represents a single color stop in a heatmap gradient"""

    color: str
    position: float


class Legend(BaseModel):
    """The legend for a Table heatmap"""

    model_config = ConfigDict(
        populate_by_name=True,
        strict=True,
        extra="ignore",
        json_schema_extra={
            "legend": {
                "size": 170,
                "title": "",
                "labels": "ranges",
                "enabled": True,
                "reverse": False,
                "labelMax": "high",
                "labelMin": "low",
                "position": "above",
                "hideItems": [],
                "interactive": False,
                "labelCenter": "medium",
                "labelFormat": "0,0.[00]",
                "customLabels": [],
            }
        },
    )

    position: Literal["above", "below"] = Field(
        default="above",
        alias="position",
        description="Whether the legend should sit above or below the table",
    )

    title: str | None = Field(
        default=None, alias="title", description="The title of the legend"
    )
    enabled: bool = Field(
        default=True,
        alias="enabled",
        description="Whether the legend should be enabled",
    )
    size: int = Field(
        default=150,
        ge=70,
        le=300,
        description="The size of the legend, which must be between 70 and 300",
    )
    reverse: bool = Field(
        default=False,
        alias="reverse",
        description="Whether to reverse the legend item order",
    )
    label_format: NumberFormat = Field(
        default=NumberFormat.THOUSANDS_WITH_OPTIONAL_DECIMALS,
        alias="labelFormat",
        description="Format of the labels to show in the legend",
    )

    def serialize_model(self):
        model = {
            "enabled": self.enabled,
            "size": self.size,
            "reverse": self.reverse,
            "position": self.position,
            "labelFormat": self.label_format,
        }
        if self.title:
            model["title"] = (self.title,)
            model["titleEnabled"] = True
        return model

    @classmethod
    def deserialize_model(cls, api_data: dict):
        result = {}
        if api_data.get("titleEnabled"):
            result["title"] = api_data["title"]
        if "enabled" in api_data:
            result["enabled"] = api_data["enabled"]
        if "size" in api_data:
            result["size"] = api_data["size"]
        if "reverse" in api_data:
            result["reverse"] = api_data["reverse"]
        if "position" in api_data:
            result["position"] = api_data["position"]
        if "labelFormat" in api_data:
            result["label_format"] = api_data["labelFormat"]
        return result


class LegendContinuous(Legend):
    """The type of legend used with a HeatmapContinuous"""

    labels: Literal["ranges", "custom"] = Field(
        default="ranges",
        alias="labels",
        description="The type of labels to show on the legend",
    )
    label_max: str | None = Field(
        default=None,
        alias="labelMax",
        description="The maximum label to show on the legend",
    )
    label_min: str | None = Field(
        default=None,
        alias="labelMin",
        description="The minimum label to show on the legend",
    )

    def serialize_model(self):
        model = super().serialize_model()
        model["labels"] = self.labels
        if self.label_max is not None:
            model["labelMax"] = self.label_max
        if self.label_min is not None:
            model["labelMin"] = self.label_min
        return model

    @classmethod
    def deserialize_model(cls, api_data):
        result = super().deserialize_model(api_data)
        if "labels" in api_data:
            result["labels"] = api_data["labels"]
        if "labelMin" in api_data:
            result["label_min"] = api_data["labelMin"]
        if "labelMax" in api_data:
            result["label_max"] = api_data["labelMax"]
        return result


class LegendSteps(Legend):
    """The type of legend used with a HeatmapSteps"""

    labels: Literal["ruler", "ranges", "custom"] = Field(
        default="ruler",
        alias="labels",
        description="The type of label to show on the legend",
    )

    custom_labels: list[str] | None = Field(
        default=None,
        alias="customLabels",
        description="Custom labels to show in the legend when custom labels is chosen",
    )

    def serialize_model(self):
        model = super().serialize_model()
        model["labels"] = self.labels
        if self.custom_labels is not None:
            model["customLabels"] = self.custom_labels
        return model

    @classmethod
    def deserialize_model(cls, api_data):
        result = super().deserialize_model(api_data)
        if "labels" in api_data:
            result["labels"] = api_data["labels"]
        if "customLabels" in api_data:
            result["custom_labels"] = api_data["customLabels"]
        return result


class HeatMap(BaseModel):
    """A base class for the Datawrapper API 'heatmap' attribute."""

    model_config = ConfigDict(
        populate_by_name=True,
        strict=True,
        extra="ignore",
        json_schema_extra={
            "heatmap": {
                "map": {},
                "mode": "continuous",
                "stops": "equidistant",
                "colors": [
                    {"color": "#f0f9e8", "position": 0},
                    {"color": "#b6e3bb", "position": 0.166666666666667},
                    {"color": "#75c8c5", "position": 0.333333333333333},
                    {"color": "#4ba8c9", "position": 0.5},
                    {"color": "#2989bd", "position": 0.666666666666667},
                    {"color": "#0a6aad", "position": 0.833333333333333},
                    {"color": "#254b8c", "position": 1},
                ],
                "palette": 0,
                "rangeMax": "",
                "rangeMin": "",
                "stopCount": 5,
                "hideValues": False,
                "customStops": [None, None, 40.8, 60.2, 79.6, None, None, 90, None],
                "rangeCenter": "",
                "categoryOrder": [],
                "interpolation": "equidistant",
                "categoryLabels": {},
            }
        },
    )
    colors: list[ColorStop] | None = Field(
        default=None,
        alias="colors",
        description="List of color stops for the heatmap gradient",
    )
    hide_values: bool | None = Field(
        default=False, alias="hideValues", description="Whether to hide the cell values"
    )
    range_min: str | None = Field(
        default=None,
        alias="rangeMin",
        description="Fix the minimum value for 'fixing' the color palette to certain minimum",
    )
    range_max: str | None = Field(
        default=None,
        alias="rangeMax",
        description="Fix the maximum value for 'fixing' the color palette to certain maximum",
    )

    @field_validator("colors", mode="before")
    @classmethod
    def validate_colors(cls, value):
        if value is None:
            default_hex = [
                "#f0f9e8",
                "#b6e3bb",
                "#75c8c5",
                "#4ba8c9",
                "#2989bd",
                "#2989bd",
                "#2989bd",
            ]
            n = len(default_hex)
            return [
                ColorStop(color=default_hex[i], position=i / (n - 1)) for i in range(n)
            ]

        # User passed list of strings → convert to ColorStop
        if all(isinstance(v, str) for v in value):
            n = len(value)
            if n == 1:
                # single colour → set white as 0 and the single color as 1
                return [
                    ColorStop(color="#ffffff", position=0),
                    ColorStop(color=value[0], position=1),
                ]
            return [ColorStop(color=value[i], position=i / (n - 1)) for i in range(n)]

        # User passed list of dicts → convert to ColorStop
        if all(isinstance(v, dict) for v in value):
            return [ColorStop.model_validate(v) for v in value]

        # User passed list of ColorStop → accept as-is
        if all(isinstance(v, ColorStop) for v in value):
            return value

        # Anything else → invalid
        raise TypeError("colors must be a list of hex strings or ColorStop objects")

    @model_validator(mode="after")
    def warn_unused_fields(self):
        # Warn if custom_stops is provided but stops != "custom" on steps heatmap
        if isinstance(self, HeatMapSteps):
            if self.custom_stops is not None and self.stops != "custom":
                warnings.warn(
                    "`custom_stops` was provided but will be ignored because "
                    "`stops` is not set to 'custom'.",
                    UserWarning,
                    stacklevel=2,
                )

        return self

    @classmethod
    def deserialize_model(cls, api_data: dict | None, legend_api_data: dict):
        if api_data is None:
            return {}
        enabled = api_data.get("enabled")
        if not enabled:
            return {"enabled": False}

        result = {
            "hide_values": api_data.get("hideValues"),
            "colors": api_data.get("colors"),
            "range_min": api_data.get("rangeMin"),
            "range_max": api_data.get("rangeMax"),
        }
        mode = api_data.get("mode")
        legend_enabled = legend_api_data.get("enabled")

        # Mode determines which kind of Legend to create
        if mode == "continuous":
            result["interpolation"] = api_data.get("interpolation")
            if legend_enabled is True:
                result["legend"] = LegendContinuous.deserialize_model(legend_api_data)
            else:
                result["legend"] = False

        elif mode == "discrete":
            result["stops"] = api_data.get("stops")
            result["stop_count"] = api_data.get("stopCount")
            result["custom_stops"] = api_data.get("customStops")
            if legend_enabled is True:
                result["legend"] = LegendSteps.deserialize_model(legend_api_data)
            else:
                result["legend"] = False

        else:
            raise ValueError(f"Unknown heatmap mode: {mode}")

        return result


class HeatMapContinuous(HeatMap):
    interpolation: (
        Literal[
            "equidistant", "quantiles-5", "quantiles-6", "quantiles-11", "natural-9"
        ]
        | None
    ) = Field(
        # in the editor equidistant=linear, quantiles-5=quartiles, quantiles-6=quintiles, quantiles-11=deciles, natural-9=natural
        default="equidistant",
        alias="interpolation",
        description="The type of interpolation",
    )
    legend: LegendContinuous | bool = Field(
        default_factory=LegendContinuous, alias="legend"
    )

    range_center: str | None = Field(
        default=None,
        alias="rangeCenter",
        description="Set the center value for 'fixing' the color palette",
    )

    def serialize_model(self):
        mode = "continuous"
        heatmap_json = {
            "enabled": True,
            "mode": mode,
            "interpolation": self.interpolation,
            "hideValues": self.hide_values,
            "colors": [
                {"color": cs.color, "position": cs.position} for cs in self.colors
            ]
            if self.colors
            else None,
        }
        if self.range_min is not None:
            heatmap_json["rangeMin"] = self.range_min
        if self.range_max is not None:
            heatmap_json["rangeMax"] = self.range_max
        if self.range_center is not None:
            heatmap_json["rangeCenter"] = self.range_center

        if self.legend is False:
            legend_json = {"enabled": False}

        else:
            self.legend = LegendContinuous()
            legend_json = self.legend.serialize_model()

        return heatmap_json, legend_json


class HeatMapSteps(HeatMap):
    stops: Literal["equidistant", "quantiles", "pretty", "natural", "custom"] | None = (
        Field(
            # in the editor equidistant=linear(equi-distant), quantiles=Quantile(equal count), pretty=rounded values, natural=Natural breaks (Jenks), custom=Custom
            default="equidistant",
            alias="stops",
            description="The type of interpolation",
        )
    )
    stop_count: int = Field(
        default=5, alias="stopCount", description="How many step categories"
    )
    legend: LegendSteps | bool = Field(default_factory=LegendSteps, alias="legend")

    custom_stops: list[str | float | None] | None = Field(
        default=None,
        alias="customStops",
        description="List of limits to be used when stops type is Custom",
    )

    def serialize_model(self):
        mode = "discrete"
        heatmap_json = {
            "enabled": True,
            "mode": mode,
            "stops": self.stops,
            "stopCount": self.stop_count,
            "hideValues": self.hide_values,
            "colors": [
                {"color": cs.color, "position": cs.position} for cs in self.colors
            ]
            if self.colors
            else None,
        }

        if self.range_min is not None:
            heatmap_json["rangeMin"] = self.range_min
        if self.range_max is not None:
            heatmap_json["rangeMax"] = self.range_max
        if self.custom_stops is not None:
            heatmap_json["customStops"] = self.custom_stops

        if self.legend is False:
            legend_json = {"enabled": False}
        else:
            legend_obj = (
                self.legend
                if isinstance(self.legend, LegendSteps)
                else LegendSteps()  # handles True
            )
            legend_json = legend_obj.serialize_model()

        return heatmap_json, legend_json

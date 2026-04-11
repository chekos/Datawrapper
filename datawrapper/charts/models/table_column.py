from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from ..enums import BorderWidth, NumberFormat, ReplaceFlagsType
from .table_text_style import TableTextStyle


class TableColumn(BaseModel):
    """Represents a column in a table"""

    model_config = ConfigDict(
        populate_by_name=True,
        strict=True,
        json_schema_extra={
            "style": {
                "bold": False,
                "color": False,
                "italic": False,
                "fontSize": 1,
                "underline": False,
                "background": False,
            },
            "width": 0.2,
            "append": "",
            "format": "0,0",
            "heatmap": {"enabled": False},
            "prepend": "",
            "barColor": 0,
            "barStyle": "normal",
            "minWidth": 30,
            "sortable": True,
            "alignment": "auto",
            "flagStyle": "1x1",
            "showAsBar": False,
            "sparkline": {
                "area": False,
                "type": "line",
                "color": 0,
                "title": "",
                "format": "0.[0]a",
                "height": 20,
                "stroke": 2,
                "dotLast": True,
                "enabled": False,
                "colorNeg": 0,
                "dotFirst": True,
                "rangeMax": "",
                "rangeMin": "",
                "labelDiff": False,
            },
            "borderLeft": "none",
            "fixedWidth": False,
            "barRangeMax": "",
            "barRangeMin": "",
            "borderRight": "none",
            "compactMode": False,
            "customColor": False,
            "replaceFlags": False,
            "showOnMobile": True,
            "showOnDesktop": True,
            "customBarColor": False,
            "barNoBackground": False,
            "borderLeftColor": "#333333",
            "customColorText": {},
            "barColorNegative": False,
            "alignmentVertical": "middle",
            "customColorBackground": {},
            "customColorBarBackground": {},
        },
    )

    name: str = Field(
        alias="name", description="The name of the column the styles should apply to"
    )
    style: TableTextStyle = Field(
        default_factory=TableTextStyle, alias="style", description="The text styles"
    )
    sortable: bool = Field(
        default=True,
        alias="sortable",
        description="Whether the column should be sortable",
    )
    show_on_mobile: bool = Field(
        default=True,
        alias="showOnMobile",
        description="Whether to show the column on mobile",
    )
    show_on_desktop: bool = Field(
        default=True,
        alias="showOnDesktop",
        description="Whether to show the column on desktop",
    )
    heatmap: bool | None = Field(
        default=None,
        alias="heatmap",
        description="Whether the column should be a heatmap",
    )
    format: NumberFormat | str | None = Field(
        default=None, alias="format", description="The number format for the column"
    )
    alignment: Literal["auto", "left", "center", "right"] = Field(
        default="auto",
        alias="alignment",
        description="How the text should be horizontally aligned in its cell",
    )
    alignment_vertical: Literal["middle", "top", "bottom"] = Field(
        default="middle",
        alias="alignmentVertical",
        description="How the text should be vertically aligned in its cell",
    )
    fixed_width: bool = Field(
        default=False,
        alias="fixedWidth",
        description="Whether the column should have a fixed width",
    )
    width: float | None = Field(
        default=None,
        ge=0,
        le=1,
        alias="width",
        description="The width of the column as a ratio of the table width",
    )
    min_width: int = Field(
        default=30,
        alias="minWidth",
        description="The minimum width of the column in px",
    )
    flag_style: ReplaceFlagsType | str | None = Field(
        default=None,
        alias="flagStyle",
        description="The style of flag to be used in the column if replace_flags is True",
    )
    replace_flags: bool = Field(
        default=False,
        alias="replaceFlags",
        description="If codes should be replaced with flags",
    )
    border_left: BorderWidth | str = Field(
        default=BorderWidth.NONE,
        alias="borderLeft",
        description="How thick the left column border should be",
    )
    border_left_color: str = Field(
        default="#333333",
        alias="borderLeftColor",
        description="The color of the left border",
    )

    # only appears if custom_color is true
    custom_color_by: str | None = Field(
        default=None,
        alias="customColorBy",
        description="The column name holding the categories with which to customise the colour of the text or background",
    )
    custom_color: bool | None = Field(
        default=None,
        alias="customColor",
        description="Define the background or text color in the cells of your selected column based on categories defined in the same or another column.",
    )
    custom_color_background: dict[str, str] | None = Field(
        default=None,
        alias="customColorBackground",
        description="Pairs of category names and the hex string for the background color that should be used.",
    )
    custom_color_text: dict[str, str] | None = Field(
        default=None,
        alias="customColorText",
        description="Pairs of category names and the hex string for the text color that should be used.",
    )
    show_as_bar: bool = Field(
        default=False,
        alias="showAsBar",
        description="Whether to show the column value as a bar chart",
    )
    bar_color_negative: bool | int | str = Field(
        default=False,
        alias="barColorNegative",
        description="Whether to use a different bar color for negative values",
    )
    bar_no_background: bool = Field(
        default=False,
        alias="barNoBackground",
        description="Whether to hide the background color on the bar",
    )
    bar_color: str | int | None = Field(
        default=None,
        alias="barColor",
        description="A reference to a color in the datawrapper palette or a hex string for the color of the bars",
    )
    bar_style: Literal["normal", "slim"] = Field(
        default="normal",
        alias="barStyle",
        description="Whether the bars should be normal or slim",
    )
    bar_range_min: str | None = Field(
        default=None,
        alias="barRangeMin",
        description="The minimum range for the bar chart, if enabled",
    )
    bar_range_max: str | None = Field(
        default=None,
        alias="barRangeMax",
        description="The maximum range for the bar chart, if enabled",
    )
    custom_bar_color: bool | None = Field(
        default=None,
        alias="customBarColor",
        description="Whether to color the bars based on a category",
    )
    # only appears if customBarColor is True
    custom_bar_color_by: str | None = Field(
        default=None,
        alias="customBarColorBy",
        description="The column name holding the categories with which to customise the bar colors",
    )
    custom_color_bar_background: dict[str, str] | None = Field(
        default=None,
        alias="customColorBarBackground",
        description="Pairs of category names and the hex string for the bar color that should be used.",
    )

    @field_validator("flag_style", mode="before")
    def convert_flag_style(cls, v):  # noqa: N805
        if v is None:
            return None
        if isinstance(v, ReplaceFlagsType):
            return v
        if isinstance(v, str):
            return ReplaceFlagsType(v)  # convert string → enum
        raise TypeError("flag_style must be a ReplaceFlagsType or valid enum string")

    def serialize_model(self) -> dict:
        model = {
            "style": self.style.model_dump(by_alias=True),
            "sortable": self.sortable,
            "showOnMobile": self.show_on_mobile,
            "showOnDesktop": self.show_on_desktop,
            "alignment": self.alignment,
            "alignmentVertical": self.alignment_vertical,
            "fixedWidth": self.fixed_width,
            "borderLeft": self.border_left,
            "borderLeftColor": self.border_left_color,
            "showAsBar": self.show_as_bar,
        }
        if self.flag_style is not None:
            model["flagStyle"] = self.flag_style
            self.replace_flags = True
            model["replaceFlags"] = self.replace_flags

        if self.heatmap is not None:
            model["heatmap"] = {"enabled": self.heatmap}

        if self.width is not None:
            model["width"] = self.width
            self._fixed_width = True
            model["fixedWidth"] = self._fixed_width

        if self.min_width is not None:
            model["minWidth"] = self.min_width
        if self.format is not None:
            model["format"] = self.format

        # handle custom colors
        if self.custom_color is not None:
            model["customColor"] = self.custom_color
            # if the column to colour by isn't specified, make it this column
            if self.custom_color_by is None:
                model["customColorBy"] = self.name
            else:
                model["customColorBy"] = self.custom_color_by
        # if the column to color by has been set, assume that customColor should be true
        if self.custom_color_by is not None and self.custom_color is None:
            model["customColorBy"] = self.custom_color_by
            model["customColor"] = True

        if self.custom_color_background is not None:
            model["customColorBackground"] = self.custom_color_background
        if self.custom_color_text is not None:
            model["customColorText"] = self.custom_color_text
        # handle column bar chart settings
        if self.show_as_bar is True:
            model["barNoBackground"] = self.bar_no_background
            model["barStyle"] = self.bar_style
            if self.bar_range_min is not None:
                model["barRangeMin"] = self.bar_range_min
            if self.bar_range_max is not None:
                model["barRangeMax"] = self.bar_range_max
            if self.bar_color is not None:
                model["barColor"] = self.bar_color
            if self.bar_color_negative is not False:
                if self.bar_color_negative is True:
                    model["barColorNegative"] = 7  # datawrapper red
                else:
                    model["barColorNegative"] = self.bar_color_negative
            # settings for coloring the bar based on category
            if self.custom_bar_color is not None and self.custom_bar_color is True:
                model["customBarColor"] = self.custom_bar_color
                if self.custom_bar_color_by is None:
                    model["customBarColorBy"] = self.name
                else:
                    model["customBarColorBy"] = self.custom_bar_color_by
            # if the category to color the bar chart is specified, assumt customBarColor should be true
            if self.custom_bar_color_by is not None and self.custom_bar_color is None:
                model["customBarColorBy"] = self.custom_bar_color_by
                model["customBarColor"] = True
            if self.custom_color_bar_background is not None:
                model["customColorBarBackground"] = self.custom_color_bar_background

        return model

    @classmethod
    def clean_mapping(cls, raw: dict | None) -> dict[str, str] | None:
        """
        Datawrapper sometimes returns dicts that contain a mix of:
        - real mappings (e.g. "Asia": "#EF9278")
        - placeholder entries (e.g. "__object": True)

        This function keeps only entries where the value is a string.
        Returns None if no valid entries remain.
        """
        if not isinstance(raw, dict):
            return None

        cleaned = {k: v for k, v in raw.items() if isinstance(v, str)}

        return cleaned or None

    @classmethod
    def deserialize_model(
        cls, column_name: str, data: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Convert a serialized Datawrapper column dict into kwargs
        suitable for initializing a TableColumn.
        """

        result: dict[str, Any] = {"name": column_name}

        if "style" in data:
            result["style"] = data["style"]
        if "sortable" in data:
            result["sortable"] = data["sortable"]
        if "showOnMobile" in data:
            result["show_on_mobile"] = data["showOnMobile"]
        if "showOnDesktop" in data:
            result["show_on_desktop"] = data["showOnDesktop"]
        if "alignment" in data:
            result["alignment"] = data["alignment"]
        if "alignmentVertical" in data:
            result["alignment_vertical"] = data["alignmentVertical"]
        if "fixedWidth" in data:
            result["fixed_width"] = data["fixedWidth"]
        if "width" in data:
            result["width"] = data["width"]
        if "minWidth" in data:
            result["min_width"] = data["minWidth"]
        if "replaceFlags" in data:
            if data["replaceFlags"] is True:
                if "flagStyle" in data:
                    result["flag_style"] = ReplaceFlagsType(data["flagStyle"])
                    result["replace_flags"] = data["replaceFlags"]
        if "borderLeft" in data:
            result["border_left"] = data["borderLeft"]
        if "borderLeftColor" in data:
            result["border_left_color"] = data["borderLeftColor"]
        if "format" in data:
            result["format"] = data["format"]

        # if there is a heatmap property, check if it is a dictionary containing an enabled key. If yes, take the enabled value
        if "heatmap" in data:
            hm = data["heatmap"]
            if isinstance(hm, dict) and "enabled" in hm:
                result["heatmap"] = hm["enabled"]

        if "customColor" in data:
            result["custom_color"] = data["customColor"]
            if data["customColor"] is True:
                result["custom_color_by"] = data["customColorBy"]
                if "customColorBackground" in data:
                    cleaned = cls.clean_mapping(data["customColorBackground"])
                    if cleaned is not None:
                        result["custom_color_background"] = cleaned

                if "customColorText" in data:
                    cleaned = cls.clean_mapping(data["customColorText"])
                    if cleaned is not None:
                        result["custom_color_background"] = cleaned

        if "showAsBar" in data:
            result["show_as_bar"] = data["showAsBar"]
            if data["showAsBar"] is True:
                if "barColor" in data:
                    result["bar_color"] = data["barColor"]
                if "barStyle" in data:
                    result["bar_style"] = data["barStyle"]
                if "customBarColor" in data:
                    result["custom_bar_color"] = data["customBarColor"]
                    if data["customBarColor"] is True:
                        if "customBarColorBy" in data:
                            result["custom_bar_color_by"] = data["customBarColorBy"]
                if "customColorBarBackground" in data:
                    result["custom_color_bar_background"] = data[
                        "customColorBarBackground"
                    ]
                if "barColorNegative" in data:
                    result["bar_color_negative"] = data["barColorNegative"]
                if "barNoBackground" in data:
                    result["bar_no_background"] = data["barNoBackground"]
                if "barRangeMin" in data:
                    result["bar_range_min"] = data["barRangeMin"]
                if "barRangeMax" in data:
                    result["bar_range_max"] = data["barRangeMax"]

        return result

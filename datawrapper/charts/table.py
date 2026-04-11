from typing import Any, Literal

import pandas as pd
from pydantic import ConfigDict, Field, field_validator

from .base import BaseChart
from .enums import PaginationType
from .models import (
    ColumnFormat,
    ColumnFormatList,
    HeatMap,
    HeatMapContinuous,
    HeatMapSteps,
    MiniColumn,
    MiniLine,
    TableBodyRow,
    TableColumn,
    TableMiniChart,
    TableRow,
)
from .serializers import Pagination


class Table(BaseChart):
    """A base class for the Datawrapper API's column chart."""

    model_config = ConfigDict(
        populate_by_name=True,
        strict=True,
        validate_assignment=True,
        validate_default=True,
        use_enum_values=True,
        json_schema_extra={
            "examples": [
                {
                    "chart-type": "tables",
                    "title": "Unemployment Rate Over Time",
                    "source_name": "Bureau of Labor Statistics",
                    "data": pd.DataFrame(
                        {
                            "date": ["2020/01", "2020/02", "2020/03"],
                            "Value": [4.0, 3.8, 4.5],
                        }
                    ),
                }
            ]
        },
    )

    #: The type of datawrapper chart to create
    chart_type: Literal["tables"] = Field(
        default="tables",
        alias="chart-type",
        description="The type of datawrapper chart to create",
    )
    #
    # chart-specific fields
    #
    searchable: bool = Field(
        default=False, alias="searchable", description="Whether to add a search bar"
    )
    striped: bool = Field(
        default=False, alias="striped", description="Whether to fill alternating rows"
    )
    show_ranks: bool = Field(
        default=False,
        alias="showRank",
        description="Whether to show a rank next to the table's rows",
    )
    sticky_first_column: bool = Field(
        default=False,
        alias="firstColumnIsSticky",
        description="Whether the first column should be sticky",
    )
    mobile_fallback: bool = Field(
        default=False,
        alias="mobileFallback",
        description="Whether the table should switch to card design on devices smaller than 450px",
    )
    compact_layout: bool = Field(
        default=False,
        alias="compactMode",
        description="Whether to reduce row height height",
    )
    parse_markdown: bool = Field(
        default=False,
        alias="markdown",
        description="Whether to show markdown formatting in the table",
    )
    merge_empty_cells: bool = Field(
        default=False,
        alias="mergeEmptyCells",
        description="Whether to combine cell with empty one to its right",
    )
    rows_per_page: str | int = Field(
        default=20, alias="perPage", description="The number of rows to show per page"
    )
    pagination: PaginationType | str = Field(
        default="top",
        alias="pagination",
        description="Wherre to show the pagination for the table",
    )

    sort_table: bool = Field(
        default=False,
        alias="sortTable",
        description="Whether the table should be sorted",
    )
    sort_direction: Literal["desc", "asc"] = Field(
        default="desc",
        alias="sortDirection",
        description="Which way the table should be sorted",
    )
    sort_by: None | str = Field(
        default=None,
        alias="sortBy",
        description="The name of the column to sort the table by",
    )
    heatmap: HeatMapContinuous | HeatMapSteps | None = Field(
        default=None,
        alias="heatmap",
        description="What kind of heatmap should be enabled, if any",
    )

    show_header: bool = Field(
        default=True, alias="showHeader", description="Whether to show the table header"
    )
    first_row_header: bool = Field(
        default=False,
        alias="firstRowIsHeader",
        description="Whether the first row of the table should be added to the table header",
    )
    header_style: TableRow | None = Field(
        default=None, alias="header", description="Styling options for the table header"
    )
    column_styles: list[TableColumn] | None = Field(
        default=None,
        alias="column_styles",
        description="Styles to apply to particular columns",
    )
    row_styles: list[TableBodyRow] | None = Field(
        default=None,
        alias="row_styles",
        description="Styles to apply to particular rows",
    )
    mini_charts: list[MiniColumn] | list[MiniLine] | None = Field(
        default=None,
        alias="mini_charts",
        description="The mini charts that should be in the table",
    )
    column_format: list[ColumnFormat] | None = Field(
        default=None,
        alias="column-format",
        description="Formatting rules for chart data columns, specifically number append, number prepend or number divisor",
    )

    @field_validator("pagination")
    @classmethod
    def validate_pagination(cls, v: PaginationType | str) -> PaginationType | str:
        """Validate that pagination is a valid PaginationType value."""
        if isinstance(v, str):
            valid_values = [e.value for e in PaginationType]
            if v not in valid_values:
                raise ValueError(
                    f"Invalid pagination: {v}. Must be one of {valid_values}"
                )
        return v

    def serialize_model(self) -> dict:
        """Serialize the model to a dictionary."""
        # Call the parent class's serialize_model method
        model = super().serialize_model()

        # Add table specific properties
        visualize_data = {
            "searchable": self.searchable,
            "striped": self.striped,
            "showRank": self.show_ranks,
            "firstColumnIsSticky": self.sticky_first_column,
            "mobileFallback": self.mobile_fallback,
            "compactMode": self.mobile_fallback,
            "markdown": self.parse_markdown,
            "mergeEmptyCells": self.merge_empty_cells,
            "pagination": Pagination.serialize(self.pagination),
            "perPage": self.rows_per_page,
            "sortTable": self.sort_table,
            "sortDirection": self.sort_direction,
        }
        # Get the data columns in case they need to be formatted
        if isinstance(self.data, pd.DataFrame):
            data_columns = list(self.data.columns)
            data_length = len(self.data.index)
        elif isinstance(self.data, list) and self.data:
            data_columns = list(self.data[0].keys())
            data_length = len(self.data)
        else:
            data_columns = []
            data_length = 0

        if self.sort_by is not None:
            visualize_data["sortBy"] = self.sort_by

        if self.header_style is not None:
            visualize_data["header"] = self.header_style.model_dump(
                by_alias=True, exclude_none=True
            )

        column_json = {}
        if self.heatmap is not None:
            # Heatmap is enabled for the whole table even though it will only apply to numerical columns. It can be disabled for specific columns.
            heatmap_json, legend_json = self.heatmap.serialize_model()
            visualize_data["heatmap"] = heatmap_json
            if legend_json:
                visualize_data["legend"] = legend_json

            if len(data_columns) > 0:
                for col in data_columns:
                    column_json[col] = {"heatmap": {"enabled": True}}

        if self.column_styles is not None:
            for col in self.column_styles:
                col_name = col.name
                col_data = col.serialize_model()
                # Ensure the column exists in the dict
                column_json.setdefault(col_name, {})

                # Handle heatmap override explicitly
                if col.heatmap is not None:
                    column_json[col_name]["heatmap"] = {"enabled": col.heatmap}

                # Merge all other fields
                for key, value in col_data.items():
                    if key == "heatmap":
                        continue  # handled above
                    column_json[col_name][key] = value

        if self.mini_charts is not None:
            for chart in self.mini_charts:
                for column in chart.columns:
                    if column_json.get(column):
                        column_json[column]["sparkline"] = chart.serialize_model()
                    else:
                        column_json[column] = {"sparkline": chart.serialize_model()}

        # Only include columns if non-empty
        if column_json is not None:
            visualize_data["columns"] = column_json

        row_json = {}
        if self.row_styles is not None:
            for row in self.row_styles:
                row_index = row.row_index
                if row_index < data_length:
                    row_json[f"row-{row_index}"] = row.serialize_model()
        if row_json is not None:
            visualize_data["rows"] = row_json

        model["metadata"]["visualize"].update(visualize_data)

        if self.column_format:
            format_list = ColumnFormatList(formats=self.column_format)
            model["metadata"]["data"]["column-format"] = format_list.serialize_to_dict()

        # Return the serialized data
        return model

    @classmethod
    def deserialize_model(cls, api_response: dict[str, Any]) -> dict[str, Any]:
        """Parse Datawrapper API response including table chart specific fields.

        Args:
            api_response: The JSON response from the chart metadata endpoint

        Returns:
            Dictionary that can be used to initialize the model
        """
        # Call parent to get base fields
        init_data = super().deserialize_model(api_response)

        # Extract table-specific sections
        metadata = api_response.get("metadata", {})

        data_section = metadata.get("data", {})

        if "column-format" in data_section:
            init_data["column_format"] = ColumnFormatList.model_validate(
                data_section["column-format"]
            ).formats

        visualize = metadata.get("visualize", {})

        if "searchable" in visualize:
            init_data["searchable"] = visualize["searchable"]
        if "striped" in visualize:
            init_data["striped"] = visualize["striped"]
        if "showRank" in visualize:
            init_data["show_ranks"] = visualize["showRank"]
        if "firstColumnIsSticky" in visualize:
            init_data["sticky_first_column"] = visualize["firstColumnIsSticky"]
        if "mobileFallback" in visualize:
            init_data["mobile_fallback"] = visualize["mobileFallback"]
        if "compactMode" in visualize:
            init_data["compact_mode"] = visualize["compactMode"]
        if "markdown" in visualize:
            init_data["markdown"] = visualize["markdown"]
        if "mergeEmptyCells" in visualize:
            init_data["merge_empty_cells"] = visualize["mergeEmptyCells"]
        if "pagination" in visualize:
            init_data["pagination"] = Pagination.deserialize(visualize["pagination"])
        if "perPage" in visualize:
            init_data["rows_per_page"] = visualize["perPage"]
        if "sortTable" in visualize:
            init_data["sort_table"] = visualize["sortTable"]
        if "sortDirection" in visualize:
            init_data["sort_direction"] = visualize["sortDirection"]
        if "sortBy" in visualize:
            init_data["sort_by"] = visualize["sortBy"]
        if "showHeader" in visualize:
            init_data["show_header"] = visualize["showHeader"]
        if "firstRowIsHeader" in visualize:
            init_data["first_row_header"] = visualize["firstRowIsHeader"]
        if "header" in visualize:
            init_data["header_style"] = visualize["header"]

        if "heatmap" in visualize:
            legend_data = visualize.get("legend")
            init_data["heatmap"] = HeatMap.deserialize_model(
                visualize["heatmap"], legend_data
            )

        if "columns" in visualize:
            column_styles = []
            mini_charts: list[TableMiniChart] = []

            for col_name, col_data in visualize["columns"].items():
                col_kwargs = TableColumn.deserialize_model(col_name, col_data)
                column_styles.append(col_kwargs)
                if "sparkline" in col_data:
                    if col_data["sparkline"]["enabled"]:
                        sparkline = col_data["sparkline"]
                        sparkline_title = sparkline.get("title")
                        sparkline_type = sparkline.get("type")
                        print(f"title is {sparkline_title}, type is {sparkline_type}")
                        match = next(
                            (
                                chart
                                for chart in mini_charts
                                if chart.title == sparkline_title
                                and chart.type == sparkline_type
                            ),
                            None,
                        )
                        if match is not None:
                            match.columns.append(col_name)
                        else:
                            sparkline_with_cols = sparkline.copy()
                            sparkline_with_cols["columns"] = [col_name]
                            clean_sparkline_with_cols = TableMiniChart.deserialize(
                                sparkline_with_cols
                            )

                            type = sparkline["type"]
                            if type == "line":
                                mini_charts.append(
                                    MiniLine(**clean_sparkline_with_cols)
                                )
                            else:
                                mini_charts.append(
                                    MiniColumn(**clean_sparkline_with_cols)
                                )
            if len(mini_charts) > 0:
                init_data["mini_charts"] = mini_charts

            init_data["column_styles"] = column_styles
        if "rows" in visualize:
            row_styles = []
            for row_name, row_data in visualize["rows"].items():
                row_index = TableBodyRow.extract_row_index(row_name)
                row_kwargs = TableBodyRow.deserialize_model(row_index, row_data)
                row_styles.append(row_kwargs)
            init_data["row_styles"] = row_styles

        return init_data
